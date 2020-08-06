import os, dill

name = "cadCAD"
configs = []
global experiment_count

if os.name == 'nt':
    dill.settings['recurse'] = True

logo = r'''
                  ___________    ____
  ________ __ ___/ / ____/   |  / __ \
 / ___/ __` / __  / /   / /| | / / / /
/ /__/ /_/ / /_/ / /___/ ___ |/ /_/ /
\___/\__,_/\__,_/\____/_/  |_/_____/
by cadCAD
'''
