from Cython.Build import cythonize
from distutils.core import setup

setup(name='lead_lag',
      ext_modules=cythonize("lead_lag.pyx"))
