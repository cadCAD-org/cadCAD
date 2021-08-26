import os, dill

name = "cadCAD"
version = "0.4.27"

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
