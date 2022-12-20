import os
import sys

from setuptools import setup, find_packages

VERSION = '2.3'

# Cython has to be installed before. And I could not find any other ways.
os.system('pip install cython')

# noinspection PyPackageRequirements
from Cython.Build import cythonize  # noqa: E402

if sys.version_info[0] < 3:
    raise Exception('Must be using Python 3.')

setup(
    name='lead-lag',
    version=VERSION,
    ext_modules=cythonize("lead_lag/lead_lag_impl.pyx", language_level="3"),
    description='Lead lag estimation with a O(n log n) complexity.',
    author='Philippe Remy',
    license='Open Source',
    packages=find_packages(),
    data_files=[('lead_lag', ['lead_lag/lead_lag_impl.pyx'])],
    include_package_data=True,
    install_requires=[
        'pandas>=0.22.0',
        'numpy>=1.15.0',
        'tqdm>=4.19.2',
        'matplotlib>=2.2.2',
    ]
)
