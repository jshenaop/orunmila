# coding=utf8

import datetime
from utils import get_wrs as wrs
from usgs import api

import pg_database as db

username = 'jshenaop'
password = 'Neuralnet1985'

api.login(username, password)

today = datetime.datetime.now()

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


def search_scenes(dataset, latitud, longitud):
    # Set the Hyperion and Landsat 8 dataset
    #hyperion_dataset = 'EO1_HYP_PUB'
    #landsat8_dataset = 'LANDSAT_8'
    # Set the EarthExplorer catalog
    node = 'EE'
    # Set the scene ids
    scenes = api.search(dataset, node, lat=latitud, lng=longitud, distance=100, ll=None, ur=None, start_date='2017-02-15', end_date=today.strftime('%Y-%m-%d'), where=None, max_results=50000, starting_number=1, sort_order="DESC", extended=False, api_key=None)
    scenes_list = []
    for scene in scenes:
        scenes_list.append(scene)
    return scenes_list


def search_metadata(scene_id):
    # Set the Hyperion and Landsat 8 dataset
    hyperion_dataset = 'EO1_HYP_PUB'
    landsat8_dataset = 'LANDSAT_8'
    # Set the EarthExplorer catalog
    node = 'EE'
    # Submit requests to USGS servers
    return api.metadata(landsat8_dataset, node, [scene_id])


def project_searcher(email):
    info_projects = db.search_projects(email)
    for project in info_projects:
        print 'PROJECT ID: ', project.project_id, 'DESCRIPTION: ', project.description, \
            ' PROJECT TYPE: ', project.project_type, 'STATUS: ', project.status

    id_project_chose = int(raw_input('Project to run: '))

    for project in info_projects:
        if project.project_id == id_project_chose:
            project_type = project.project_type
            from_date = project.from_date
            tile = project.tile
            latitude = project.latitude
            longitude = project.longitude
            project_id = str(project.project_id)

    return project_type, from_date, tile, latitude, longitude, project_id