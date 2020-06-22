```
                    __________   ____
  ________ __ _____/ ____/   |  / __ \
 / ___/ __` / __  / /   / /| | / / / /
/ /__/ /_/ / /_/ / /___/ ___ |/ /_/ /
\___/\__,_/\__,_/\____/_/  |_/_____/
by BlockScience
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

#### Change Log: [ver. 0.4.15](CHANGELOG.md)
[Previous Release (No Longer Supported)](https://github.com/cadCAD-org/cadCAD/tree/b9cc6b2e4af15d6361d60d6ec059246ab8fbf6da)

## 1. Installation: 
Requires [Python 3](https://www.python.org/downloads/) 

**Option A: Install Using [pip](https://pypi.org/project/cadCAD/)** 
```bash
pip3 install cadCAD
```

**Option B:** Build From Source
```
pip3 install -r requirements.txt
python3 setup.py sdist bdist_wheel
pip3 install dist/*.whl
```

**Option C: Using [Nix](https://nixos.org/nix/)**
1. Run `curl -L https://nixos.org/nix/install | sh` or install Nix via system package manager
2. Run `nix-shell` to enter into a development environment, `nix-build` to build project from source, and `nix-env -if default.nix` to install

The above steps will enter you into a Nix development environment, with all package requirements for development of and with cadCAD.

This works with just about all Unix systems as well as MacOS, for pure reproducible builds that don't dirty your local environment.

## 2. Documentation:
* [System Model Configuration](documentation/System_Configuration.md)
* [System Simulation Execution](documentation/Simulation_Execution.md)
* [Policy Aggregation](documentation/Policy_Aggregation.md)
* [System Model Parameter Sweep](documentation/System_Model_Parameter_Sweep.md)

## 3. Connect:
Find other cadCAD users at our [Discourse](https://community.cadcad.org/). We are a small but rapidly growing community.

## 4. [Contribute!](CONTRIBUTING.md)