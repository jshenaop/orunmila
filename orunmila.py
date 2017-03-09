# coding=utf-8

import sys
import os
from collections import OrderedDict

import termcolor
import pg_database as db
import scene_informer as si
import scene_downloader as sd
import scene_processer as sp

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