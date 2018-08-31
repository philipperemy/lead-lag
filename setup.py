from Cython.Build import cythonize
from setuptools import setup, find_packages

VERSION = '1.3'

import sys

if sys.version_info[0] < 3:
    raise Exception('Must be using Python 3.')

setup(name='lead-lag',
      version=VERSION,
      ext_modules=cythonize("lead_lag/lead_lag_impl.pyx"),
      description='Lead lag estimation with a O(n log n) complexity.',
      author='Philippe Remy',
      license='Open Source',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'pandas>=0.22.0',
          'numpy>=1.15.0',
          'tqdm>=4.19.2',
          'matplotlib>=2.2.2',
      ])
