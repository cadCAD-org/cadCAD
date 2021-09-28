```
                  ___________    ____
  ________ __ ___/ / ____/   |  / __ \
 / ___/ __` / __  / /   / /| | / / / /
/ /__/ /_/ / /_/ / /___/ ___ |/ /_/ /
\___/\__,_/\__,_/\____/_/  |_/_____/
by cadCAD                  ver. 0.4.28
======================================
       Complex Adaptive Dynamics       
       o       i        e
       m       d        s
       p       e        i
       u       d        g
       t                n
       e
       r
```
***cadCAD*** is a Python package that assists in the processes of designing, testing and validating complex systems 
through simulation, with support for Monte Carlo methods, A/B testing and parameter sweeping. 

# Getting Started

#### Change Log: [ver. 0.4.28](CHANGELOG.md)

[Previous Stable Release (No Longer Supported)](https://github.com/cadCAD-org/cadCAD/tree/b9cc6b2e4af15d6361d60d6ec059246ab8fbf6da)

## 0. Pre-installation Virtual Environments with [`venv`](https://docs.python.org/3/library/venv.html) (Optional):
If you wish to create an easy to use virtual environment to install cadCAD within, please use python's the built in `venv` package.

***Create** a virtual environment:*
```bash
$ python3 -m venv ~/cadcad
```

***Activate** an existing virtual environment:*
```bash
$ source ~/cadcad/bin/activate
(cadcad) $
```

***Deactivate** virtual environment:*
```bash
(cadcad) $ deactivate
$
```

## 1. Installation: 
Requires [>= Python 3.6.13](https://www.python.org/downloads/) 

**Option A: Install Using **[pip](https://pypi.org/project/cadCAD/0.4.28/)** 
```bash
pip3 install cadCAD
```

**Option B:** Build From Source
```
pip3 install -r requirements.txt
python3 setup.py sdist bdist_wheel
pip3 install dist/*.whl
```

## 2. Documentation:
* [Simulation Configuration](documentation/README.md)
* [Simulation Execution](documentation/Simulation_Execution.md)
* [Policy Aggregation](documentation/Policy_Aggregation.md)
* [Parameter Sweep](documentation/System_Model_Parameter_Sweep.md)
* [Display System Model Configurations](documentation/System_Configuration.md)

## 3. Connect:
Find other cadCAD users at our [Discourse](https://community.cadcad.org/). We are a small but rapidly growing community.

## 4. [Contribute!](CONTRIBUTING.md)