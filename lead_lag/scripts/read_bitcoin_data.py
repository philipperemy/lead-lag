import numpy as np
import pandas as pd


def read_small_data(small_filename):
    print(f'Reading {small_filename}')
    d = pd.read_csv(small_filename, parse_dates=True, index_col=0)
    d['timestamp'] = d.index.values.astype(np.int64) // 10 ** 9
    return d


def bitcoin_data(exchange_1_small_data_file, exchange_2_small_data_file):
    exchange_1 = read_small_data(exchange_1_small_data_file)
    exchange_2 = read_small_data(exchange_2_small_data_file)

    return exchange_1[['timestamp', 'last']].values, exchange_2[['timestamp', 'last']].values
