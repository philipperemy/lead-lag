import sys

if len(sys.argv) != 2:
    print('Specify a filename.')
    exit(1)

filename = sys.argv[1]

import os

if not os.path.isfile(filename):
    print('Filename not found.')
    exit(1)

import matplotlib.pyplot as plt

import pandas as pd

pd.read_csv(filename, index_col=0).plot()
plt.show()
