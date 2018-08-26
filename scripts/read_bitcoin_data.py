import warnings

warnings.filterwarnings('ignore', message='numpy.dtype size changed')
warnings.filterwarnings('ignore', message='numpy.ufunc size changed')

import numpy as np
import pandas as pd


def bitcoin_data(exchange_1_small_data_file, exchange_2_small_data_file):
    def read_small_data(small_filename):
        print(f'Reading {small_filename}')
        d = pd.read_csv(small_filename, parse_dates=True, index_col=0)
        d['timestamp'] = d.index.values.astype(np.int64) // 10 ** 9
        return d

    exchange_1 = read_small_data(exchange_1_small_data_file)
    exchange_2 = read_small_data(exchange_2_small_data_file)

    exchange_1_arr = exchange_1[['timestamp', 'last']].values
    exchange_2_arr = exchange_2[['timestamp', 'last']].values

    # exchange_2_arr[:, 0] = np.round(exchange_2_arr[:, 0] / 100).astype(np.int)
    # exchange_1_arr[:, 0] = np.round(exchange_1_arr[:, 0] / 100).astype(np.int)

    time_origin = min(exchange_2_arr[0, 0], exchange_1_arr[0, 0])
    exchange_1_arr[:, 0] -= time_origin
    exchange_2_arr[:, 0] -= time_origin
    time_end = int(max(exchange_2_arr[-1, 0], exchange_1_arr[-1, 0]))

    exchange_1_values = np.zeros(shape=time_end + 1) * np.nan
    exchange_1_t = []
    for element_slice in exchange_1_arr:
        exchange_1_values[int(element_slice[0])] = element_slice[1]
        exchange_1_t.append(int(element_slice[0]))

    exchange_2_values = np.zeros(shape=time_end + 1) * np.nan
    exchange_2_t = []
    for element_slice in exchange_2_arr:
        exchange_2_values[int(element_slice[0])] = element_slice[1]
        exchange_2_t.append(int(element_slice[0]))

    return exchange_1_values, exchange_2_values, exchange_1_t, exchange_2_t
