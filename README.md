# SimCad

**Dependencies:**
```bash
pip install pipenv fn tabulate
```

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
pip install -e .
```
* [Package Creation Tutorial](https://python-packaging.readthedocs.io/en/latest/minimal.html)

Step 2. Import Package & Run:  
```python
from engine import run
run.main()
```

Same can be run in Jupyter . 
```bash
jupyter notebook
```

Notebooks Directory:  
`/DiffyQ-SimCAD/notebooks/`


**Warning**:
**Do Not** publish this package / software to **Any** software repository **except** [DiffyQ-SimCAD's staging branch](https://github.com/BlockScience/DiffyQ-SimCAD/tree/staging) or its **Fork** 
