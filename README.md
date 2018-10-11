# SimCad

**Dependencies:**

Install [pipenv](https://pypi.org/project/pipenv/)

**Project:**

Example Run File:
`/DiffyQ-SimCAD/test.py`

**User Interface: Simulation Configuration**

Configurations:
```bash
/DiffyQ-SimCAD/ui/config.py
```

**Build Tool & Package Import:**

Step 1. Build & Install Package locally: 
```bash
pip install .
```
* [Package Creation Tutorial](https://python-packaging.readthedocs.io/en/latest/minimal.html)

Step 2. Import Package & Run:
```python
from engine import run
run.main()
```

**Warning**:
**Do Not** publish this package / software to **Any** software repository **except** [DiffyQ-SimCAD's staging branch](https://github.com/BlockScience/DiffyQ-SimCAD/tree/staging) or its **Fork** 

**Jupyter Setup:**

Step 1. Create Virtual Environment:
```bash
cd DiffyQ-SimCAD
pipenv run python -m ipykernel install --user --name DiffyQ-SimCAD --display-name "DiffyQ-SimCAD Env"
```
Step 2. Run Jupter Notebook:
```bash
pipenv run jupyter notebook
```
Step 3. Notebook Management:

Notebook Directory:

`/DiffyQ-SimCAD/notebooks/`

Note:

Notebooks should run on the `DiffyQ-SimCAD Env` kernel.






