import warnings

warnings.filterwarnings('ignore', message='numpy.dtype size changed')
warnings.filterwarnings('ignore', message='numpy.ufunc size changed')


def visualize_contrasts(results_dir):
    from glob import glob
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    results_filenames = glob(f'{results_dir}/**.csv')
    data = []
    for results_filename in results_filenames:
        filename_wo_extension = os.path.splitext(os.path.basename(results_filename))[0]

        _, ex1, _, _, ex2, date = filename_wo_extension.split('_')

        print(date)
        d = pd.read_csv(results_filename, names=['LagRange', date], index_col=0, header=None, skiprows=1)
        data.append(d)
    data = pd.concat(data, axis=1)
    data.median(axis=1).plot()
    # data.plot()
    plt.show()


def main():
    import sys

    if len(sys.argv) != 2:
        print('Specify a result directory from main_bitcoin.py.')
        exit(1)
    results_dir = sys.argv[1]
    visualize_contrasts(results_dir)


if __name__ == '__main__':
    main()
