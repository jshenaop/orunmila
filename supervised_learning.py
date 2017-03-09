import csv
import os
import numpy as np
from sklearn import tree
from osgeo import gdal
#import ospybook as pb


def stack_bands(filenames):
    """Returns a 3D array containing all band data from all files."""
    bands = []
    for fn in filenames:
        ds = gdal.Open(fn)
        for i in range(1, ds.RasterCount + 1):
            bands.append(ds.GetRasterBand(i).ReadAsArray())

    return np.dstack(bands)


def make_raster(in_ds, fn, data, data_type, nodata=None):
    """Create a one-band GeoTIFF.

    in_ds     - datasource to copy projection and geotransform from
    fn        - path to the file to create
    data      - NumPy array containing data to write
    data_type - output data type
    nodata    - optional NoData value
    """
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(
        fn, in_ds.RasterXSize, in_ds.RasterYSize, 1, data_type)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    out_band = out_ds.GetRasterBand(1)
    if nodata is not None:
        out_band.SetNoDataValue(nodata)
    out_band.WriteArray(data)
    out_band.FlushCache()
    out_band.ComputeStatistics(False)
    return out_ds

def compute_overview_levels(band):
    """Return an appropriate list of overview levels."""
    max_dim = max(band.XSize, band.YSize)
    overviews = []
    level = 1
    while max_dim > 256:
        level *= 2
        overviews.append(level)
        max_dim /= 2
    return overviews


folder = r'C:\SatImagery\LANDSAT_8\007059\LC80070592017050LGN00'
raster_fns = ['LC80070592017050LGN00_B1.TIF',
              'LC80070592017050LGN00_B2.TIF',
              'LC80070592017050LGN00_B3.TIF',
              'LC80070592017050LGN00_B4.TIF',
              'LC80070592017050LGN00_B5.TIF',
              'LC80070592017050LGN00_B6.TIF',
              'LC80070592017050LGN00_B7.TIF',
              'LC80070592017050LGN00_B9.TIF']
out_fn = 'tree_prediction60.tif'
train_fn = r'C:\Users\juan\OneDrive\Proyectos\Satellite Imagery Data\orunmila\orunmila\coordinates.csv'
gap_fn = r'C:\Users\juan\OneDrive\Proyectos\Satellite Imagery Data\orunmila\orunmila\landcover60.tif'

os.chdir(folder)

# Read the coordinates and actual classification from the csv.
# This is the training data.
xys = []
classes = []
with open(train_fn) as fp:
    reader = csv.reader(fp, delimiter=' ')
    next(reader)
    for row in reader:
        xys.append([float(n) for n in row[:2]])
        classes.append(int(row[2]))

print xys
print classes

# Calculate the pixel offsets for the coordinates obtained from the csv.
ds = gdal.Open(raster_fns[0])
pixel_trans = gdal.Transformer(ds, None, [])
offset, ok = pixel_trans.TransformPoints(True, xys)
cols, rows, z = zip(*offset)

# Get the satellite data.
data = stack_bands(raster_fns)

print data[3500][3500]

# Sample the satellite data at the coordinates from the csv.
sample = data[rows, cols, :]

# Fit the classification tree.
clf = tree.DecisionTreeClassifier(max_depth=5)
clf = clf.fit(sample, classes)

# Apply the new classification tree model to the satellite data.
rows, cols, bands = data.shape
data2d = np.reshape(data, (rows * cols, bands))
prediction = clf.predict(data2d)
prediction = np.reshape(prediction, (rows, cols))

# Set the pixels with no valid satellite data to 0.
prediction[np.sum(data, 2) == 0] = 0

# Save the output.
predict_ds = make_raster(ds, out_fn, prediction, gdal.GDT_Byte, 0)
predict_ds.FlushCache()
levels = compute_overview_levels(predict_ds.GetRasterBand(1))
predict_ds.BuildOverviews('NEAREST', levels)

# Apply the color table from the SWReGAP landcover raster.
gap_ds = gdal.Open(gap_fn)
colors = gap_ds.GetRasterBand(1).GetRasterColorTable()
predict_ds.GetRasterBand(1).SetRasterColorTable(colors)

del ds
