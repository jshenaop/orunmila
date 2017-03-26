# coding=utf-8

import sys
import os
from collections import OrderedDict

import termcolor
import pg_database as db
#import scene_informer as si
#import scene_downloader as sd
#import scene_processer as sp


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
    imagery_repository = 'D:\Orunmila\IMAGERY'
    analytics_repository = 'D:\Orunmila\ANALITICS'
elif (os.environ['COMPUTERNAME']) == "HELLBOY":
    imagery_repository = 'C:\Orunmila\IMAGERY'
    analytics_repository = 'C:\Orunmila\ANALITICS'
elif (os.environ['COMPUTERNAME']) == "JANEL":
    imagery_repository = 'E:\Orunmila\IMAGERY'
    analytics_repository = 'E:\Orunmila\ANALITICS'
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


# Register
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
    email = raw_input('Client email: ')
    project_code = raw_input('Add project code: ')
    latitude = raw_input('Add latitude: ')
    longitude = raw_input('Add longitude: ')
    analysis = raw_input('Add analysis: ')

    db.add_project(email=email, project_code=project_code, latitude=latitude, longitude=longitude, analysis=analysis)



# Registro Proyecto
        # Ingresar Proyecto.
        # Consultar Proyecto (Satelite).

# Operación
    # Identificar Tile.
    # Buscar imagenes correspondientes al satelite en un rango de tiempo.
    # Descargar imagenes, descomprimir y eliminar.
    # Pegarlas, Cortarlas y Clasificarlas.
        # Clasificar escoger tipo de analisis.
    # Estadistica.
    # Diagnostico

# Entrega información

# Program menu

menu = OrderedDict([
    ('r', client_register),
    ('s', client_search),
])

if __name__ == '__main__':
    menu_loop()
