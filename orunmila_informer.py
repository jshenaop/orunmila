# coding=utf8

import datetime
from utils import get_wrs as wrs

def get_today():
    # Get today date to work with
    today = datetime.datetime.now()
    year = today.strftime("%Y")
    day = today.timetuple()

    if len(str(day.tm_yday)) == 1:
        julian_day = '00{}'.format(day.tm_yday)
    elif len(str(day.tm_yday)) == 2:
        julian_day = '0{}'.format(day.tm_yday)

    return (year+julian_day)


def get_wrs2(latitude, longitude):
    #latitude = input('Ingrese LATITUD: ')
    #longitude = input('Ingrese LONGITUD: ')

    conv = wrs.ConvertToWRS()
    wrs_path_row = conv.get_wrs(float(latitude), float(longitude))

    path = str(wrs_path_row[0]['path'])
    row = str(wrs_path_row[0]['row'])

    if len(path) == 1:
        path = '00{}'.format(path)
    elif len(path) == 2:
        path = '0{}'.format(path)

    if len(row) == 1:
        row = '00{}'.format(row)
    elif len(row) == 2:
        row = '0{}'.format(row)

    return (path+row)
