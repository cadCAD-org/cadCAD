import os, dill

name = "cadCAD"
configs = []

if os.name == 'nt':
    dill.settings['recurse'] = True
