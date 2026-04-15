from setuptools import setup
from Cython.Build import cythonize
import sys
import os

sys.argv.append('build_ext')
sys.argv.append('--inplace')

setup(
    name='data_generator',
    ext_modules=cythonize(["main.py", "pages/*.py", "utils/*.py"], compiler_directives={'language_level': "3"}),
)
