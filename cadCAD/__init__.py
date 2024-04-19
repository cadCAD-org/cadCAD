import os

import dill

from cadCAD.configuration import Experiment

name = "cadCAD"
version = "0.5.3"
experiment = Experiment()
configs = experiment.configs

if os.name == "nt":
    dill.settings["recurse"] = True

logo = r"""
                  ___________    ____
  ________ __ ___/ / ____/   |  / __ \
 / ___/ __` / __  / /   / /| | / / / /
/ /__/ /_/ / /_/ / /___/ ___ |/ /_/ /
\___/\__,_/\__,_/\____/_/  |_/_____/
by cadCAD
"""
