from distutils.core import setup
from Cython.Build import cythonize
import numpy

# run: python3 setup.py build_ext --inplace
setup(
    ext_modules = cythonize(['vadetis/*.pyx']),
    include_dirs = [numpy.get_include()]
)