from setuptools import setup, find_packages

short_description = "cadCAD: tweaked version"

long_description = """
This is a tweaked version of cadCAD, use at your own peril.
"""

setup(name='cadCAD_tweaked',
      version='0.4.23',
      description=short_description,
      long_description=long_description,
      url='https://github.com/danlessa/cadCAD-tweaked',
      author='Danilo Lessa Bernardineli',
      author_email='danilo.lessa@gmail.com',
      license='LICENSE.txt',
      packages=find_packages(),
      install_requires=[
            "pandas",
            "pathos",
            "fn",
            "funcy"
      ],
      python_requires='>=3.6.8'
)
