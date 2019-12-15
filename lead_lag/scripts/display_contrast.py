import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

if len(sys.argv) != 2:
    print('Specify a filename.')
    exit(1)

filename = sys.argv[1]

if not os.path.isfile(filename):
    print('Filename not found.')
    exit(1)

pd.read_csv(filename, index_col=0).plot_results()
plt.show()
