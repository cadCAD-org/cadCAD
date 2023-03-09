from setuptools import setup, find_packages

short_description = "cadCAD: tweaked version"

long_description = """
This is a tweaked version of cadCAD, use at your own peril.
"""

name = "cadCAD-legacy-devel"
version = "0.4.29"

setup(name=name,
      version=version,
      description=short_description,
      long_description=long_description,
      url='https://github.com/cadCAD-org/cadCAD-legacy-devel',
      author='Danilo Lessa Bernardineli',
      author_email='danilo.lessa@gmail.com',
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
      python_requires='>=3.10.0'
)