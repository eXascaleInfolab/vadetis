from distutils.core import setup
from Cython.Build import cythonize
import numpy

# run: python3 setup.py build_ext --inplace
setup(
    ext_modules = cythonize(['vadetisweb/anomaly_algorithms/detection/correleation/cutil/*.pyx']),
    include_dirs = [numpy.get_include()]
)