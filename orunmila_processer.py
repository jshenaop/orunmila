# coding=utf8

import sys
import os
import subprocess

import gdal
import osr
import numpy as np
from sklearn import tree
from osgeo import gdal
import utm

sys.path.append('C:/Software/Anaconda2/envs/orunmila/Scripts/')


def gdal_info(scene):
    # gdalinfo XXXXXX_B1.TIF
    raster = gdal.Open('{0}_B1.tif'.format(scene))

    ulx, xres, xskew, uly, yskew, yres = raster.GetGeoTransform()

    lrx = ulx + (raster.RasterXSize * xres)
    lry = uly + (raster.RasterYSize * yres)

    return ulx, uly, lrx, lry


def format_project(project_id):
    if len(project_id) == 1:
        project_path = '0000{}'.format(project_id)

    elif len(project_id) == 2:
        project_path = '000{}'.format(project_id)

    elif len(project_id) == 3:
        project_path = '00{}'.format(project_id)

    elif len(project_id) == 4:
        project_path = '0{}'.format(project_id)

    else:
        project_path = project_id

    return project_path


def analytics_folder_creation(analytics_repository, project_type, project_id):
    project_path = format_project(project_id)

    if not os.path.exists("{}/{}{}".format(analytics_repository, project_type, project_path)):
        os.makedirs("{}/{}{}".format(analytics_repository, project_type, project_path))


def stack_bands(imagery_repository, analytics_repository, satellite, tile, project_type, project_id, scene, band_list_db):
    band_list = str(band_list_db)
    band_list = band_list.split()

    stack_list = []

    for band in band_list:
        path_source = '{0}/{1}/{2}/{3}/{4}_B{5}.TIF'.format(imagery_repository, satellite, tile, scene, scene, band)
        stack_list.append(path_source)

    project_path = format_project(project_id)

    path_analytics = '{}/{}{}/{}.TIF'.format(analytics_repository, project_type, project_path, scene)

    # Open band 1.
    input_raster = gdal.Open(stack_list[0])
    info_band = input_raster.GetRasterBand(1)

    # Create a 3-band GeoTIFF with the same dimensions, data type, projection,
    # and georeferencing info as band 1. This will be overwritten if it exists.
    gtiff_driver = gdal.GetDriverByName('GTiff')
    output_raster = gtiff_driver.Create(path_analytics, info_band.XSize, info_band.YSize, len(band_list), info_band.DataType)

    output_raster.SetProjection(input_raster.GetProjection())
    output_raster.SetGeoTransform(input_raster.GetGeoTransform())

    for index, band in enumerate(stack_list):
        # Copy data from band i into the output image.
        info_raster = gdal.Open(band)
        input_band = info_raster.GetRasterBand(1)
        input_data = input_band.ReadAsArray()
        output_band = output_raster.GetRasterBand(index + 1)
        output_band.WriteArray(input_data)


    # Compute statistics on each output band.
    output_raster.FlushCache()
    for i in range(1, len(band_list)):
        output_raster.GetRasterBand(i).ComputeStatistics(False)

    # Build overview layers for faster display.
    output_raster.BuildOverviews('average', [2, 4, 8, 16, 32])

    # This will effectively close the file and flush data to disk.
    del output_raster


def gdal_clip(analytics_repository, image, project_type, id_format_project, latitude, longitude, kilometers):
    # gdal_translate -projwin 450000 500000 600000 400000 LC80080572015116LGN00_B1.TIF OUTPUT.TIF

    int(kilometers)

    x, y, zone_number, zone_letter = utm.from_latlon(float(latitude), float(longitude))

    xmin = x - (int(kilometers) * 1000)
    ymax = y + (int(kilometers) * 1000)
    ymin = y - (int(kilometers) * 1000)
    xmax = x + (int(kilometers) * 1000)

    path = r'{0}/{1}{2}'.format(analytics_repository, project_type, id_format_project)

    cmd_call = (
        "gdal_translate -projwin {0} {1} {2} {3} {4}/{5} {6}/{7}_CLIPPED.TIF").format(xmin, ymax, xmax, ymin, path, image, path, image)

    return os.system(cmd_call)


def main():
    pass

if __name__ == '__main__':
    main()
