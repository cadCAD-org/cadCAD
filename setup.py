from setuptools import setup, find_packages

short_description = "cadCAD: a differential games based simulation software package for research, validation, and \
        Computer Aided Design of economic systems"

long_description = """
cadCAD (complex adaptive systems computer-aided design) is a python based, unified modeling framework for stochastic 
dynamical systems and differential games for research, validation, and Computer Aided Design of economic systems created 
by BlockScience. It is capable of modeling systems at all levels of abstraction from Agent Based Modeling (ABM) to 
System Dynamics (SD), and enabling smooth integration of computational social science simulations with empirical data 
science workflows.

An economic system is treated as a state-based model and defined through a set of endogenous and exogenous state 
variables which are updated through mechanisms and environmental processes, respectively. Behavioral models, which may 
be deterministic or stochastic, provide the evolution of the system within the action space of the mechanisms. 
Mathematical formulations of these economic games treat agent utility as derived from the state rather than direct from 
an action, creating a rich, dynamic modeling framework. Simulations may be run with a range of initial conditions and 
parameters for states, behaviors, mechanisms, and environmental processes to understand and visualize network behavior 
under various conditions. Support for A/B testing policies, Monte Carlo analysis, and other common numerical methods is 
provided.
"""

name = "cadCAD"
version = "0.4.29"

setup(name=name,
      version=version,
      description=short_description,
      long_description=long_description,
      url='https://github.com/cadCAD-org/cadCAD',
      author='cadCAD-org Developers',
      author_email='info@block.science',
      license='LICENSE.txt',
      packages=find_packages(),
      install_requires=[
            "pandas",
            "funcy",
            "dill",
            "pathos",
            "numpy",
            "pytz",
            "six"
      ],
      python_requires='>=3.8.0'
)