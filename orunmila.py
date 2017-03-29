# coding=utf-8

import sys
import os
from collections import OrderedDict

import termcolor
import pg_database as db
import orunmila_informer as oi
import orunmila_downloader as od

# import scene_downloader as sd
# import scene_processer as sp


print (termcolor.colored("""
   ____                             _ _
  / __ \                           (_) |
 | |  | |_ __ _   _ _ __  _ __ ___  _| | __ _
 | |  | | '__| | | | '_ \| '_ ` _ \| | |/ _` |
 | |__| | |  | |_| | | | | | | | | | | | (_| |
  \____/|_|   \__,_|_| |_|_| |_| |_|_|_|\__,_|

""", 'green'))
# http://patorjk.com/software/taag/#p=display&v=2&c=vb&f=Crazy&t=Orunmila
print (termcolor.colored("""
  ***     Satellite Analysis Imagery     ***
""", 'blue'))

# System Variables

if (os.environ['COMPUTERNAME']) == "HENAOJ":
    imagery_repository = 'D:/Orunmila/IMAGERY'
    analytics_repository = 'D:/Orunmila/ANALITICS'
elif (os.environ['COMPUTERNAME']) == "HELLBOY":
    imagery_repository = 'C:/Orunmila/IMAGERY'
    analytics_repository = 'C:/Orunmila/ANALITICS'
elif (os.environ['COMPUTERNAME']) == "JANEL":
    imagery_repository = 'E:/Orunmila/IMAGERY'
    analytics_repository = 'E:/Orunmila/ANALITICS'
elif (os.environ['COMPUTERNAME']) == "HP40":
    imagery_repository = ''
    analytics_repository = ''


# Menu
def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = raw_input('Action: ').lower().strip()

        if choice in menu:
            menu[choice]()


def menu_loop_admin():
    """Show Admin Menu"""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu_admin.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = raw_input('Action: ').lower().strip()

        if choice in menu_admin:
            menu_admin[choice]()


def menu_loop_project():
    """Show Project Menu"""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu_project.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = raw_input('Action: ').lower().strip()

        if choice in menu_project:
            menu_project[choice]()


# Menu Admin
def client_register():
    """Client Register."""
    name = raw_input('Add client name: ')
    surname = raw_input('Add client surname: ')
    email = raw_input('Add client email: ')
    cellphone = raw_input('Add client cellphone: ')
    db.add_client(name=name, surname=surname, email=email, cellphone=cellphone)
    return None


def client_search():
    """Client Search."""
    email = raw_input('Client email for Search: ')
    info = db.search_client(email=email)
    return info.name, info.surname, info.email, info.cellphone


def project_register():
    """Project Register."""
    email = raw_input('Client email: ')
    project_type = raw_input('Add project type: ')
    latitude = raw_input('Add latitude: ')
    longitude = raw_input('Add longitude: ')
    analysis = raw_input('Add analysis: ')
    description = raw_input('Add description: ')

    tile = oi.get_wrs2(latitude, longitude)

    try:
        tile = oi.get_wrs2(latitude, longitude)
        db.add_project(email=email, project_type=project_type, latitude=latitude, longitude=longitude, tile=tile,
                       analysis=analysis, description=description)

    except:
        print "Can not save project"


def project_search():
    """Project Search."""
    pass


# Menu Project
def search_scenes():
    """Search Scenes"""
    email = raw_input('Client email: ')
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

    def get_images(project_type, from_date, tile, latitude, longitude):
        info = db.search_analysis_type(project_type)
        scenes = oi.search_scenes(info.satellite, latitude, longitude)

        scenes_available = []

        for scene in scenes:
            scenes_available.append(scene['displayId'])

        return scenes_available

    def get_scenes_downloaded(imagery_repository, satellite, tile):
        path = r'{0}\{1}\{2}'.format(imagery_repository, satellite, tile)
        downloaded_scenes = os.listdir(path)
        return downloaded_scenes

    satellite = db.search_analysis_type(project_type=project_type).satellite

    list_scenes_available = get_images(project_type=project_type, from_date=from_date, tile=tile, latitude=latitude,
                                       longitude=longitude)

    list_scenes_downloaded = get_scenes_downloaded(imagery_repository=imagery_repository, satellite=satellite,
                                                   tile=tile)

    list_scenes_waiting = []

    for scene_available in list_scenes_available:
        if scene_available not in list_scenes_downloaded:
            list_scenes_waiting.append(scene_available)

    number_scenes_waiting = len(list_scenes_waiting)
    print ('You have {0} scenes downloaded, currently the project has {1} new scenes for download.'
           .format(len(list_scenes_downloaded), number_scenes_waiting))


def download_scenes():
    """Download Scenes"""
    email = raw_input('Client email: ')
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

    def get_images(project_type, from_date, tile, latitude, longitude):
        info = db.search_analysis_type(project_type)
        scenes = oi.search_scenes(info.satellite, latitude, longitude)

        scenes_available = []

        for scene in scenes:
            scenes_available.append(scene['displayId'])

        return scenes_available

    def get_scenes_downloaded(imagery_repository, satellite, tile):
        path = r'{0}/{1}/{2}'.format(imagery_repository, satellite, tile)
        downloaded_scenes = os.listdir(path)
        return downloaded_scenes

    satellite = db.search_analysis_type(project_type=project_type).satellite

    list_scenes_available = get_images(project_type=project_type, from_date=from_date, tile=tile, latitude=latitude,
                                       longitude=longitude)

    list_scenes_downloaded = get_scenes_downloaded(imagery_repository=imagery_repository, satellite=satellite,
                                                   tile=tile)

    list_scenes_waiting = []

    for scene_available in list_scenes_available:
        if scene_available not in list_scenes_downloaded:
            list_scenes_waiting.append(scene_available)
            print list_scenes_waiting

    number_scenes_waiting = len(list_scenes_waiting)
    print ('You have {0} scenes downloaded, currently the project has {1} new scenes for download.'
           .format(len(list_scenes_downloaded), number_scenes_waiting))

    download_bool = raw_input('Do you want to download this scenes (Y/N) ')

    if download_bool.lower() == 'y':
        satellite = db.search_analysis_type(project_type=project_type).satellite
        for scene_waiting in list_scenes_waiting:

            path = r'{0}/{1}'.format(imagery_repository, satellite)
            try:
                od.connect_earthexplorer_no_proxy()
                od.prepare_dir(path, scene_waiting)
                od.download(path, scene_waiting)
                od.uncompress(path, scene_waiting)
                od.remove(path, scene_waiting)
            except:
                pass
    else:
        print ('Thanks for nothing')

    # Buscar imagenes disponibles y no descargadas correspondientes al satelite en un rango de tiempo.
    # Identificar Tile, Tipo de Proyecto, Rango de Fechas.
    # Identificar Imagenes descargadas.
    # Identificar Imagenes disponibles.
    # Comparar entre imagenes disponibles y descargadas y descargar solo las de poca nubosidad.
    # Descargar Imagenes, Descomprimir y Eliminar.



    # Pegarlas, Cortarlas y Clasificarlas.
    # Clasificar escoger tipo de analisis.
    # Estadistica.
    # Diagnostico


# Entrega información

# Program menu

menu = OrderedDict([
    ('a', menu_loop_admin),
    ('r', menu_loop_project),
])

menu_admin = OrderedDict([
    ('r', client_register),
    ('s', client_search),
    ('p', project_register),
    ('f', project_search),
])

menu_project = OrderedDict([
    ('s', search_scenes),
    ('d', download_scenes),
    # ('s', show_last_analysis),
])

if __name__ == '__main__':
    menu_loop()
