import numpy as np
import pandas as pd


def read_small_data(small_filename: str, precision_in_seconds: float = 1):
    if precision_in_seconds not in {1, 0.1, 0.01, 0.001}:
        raise Exception('Precision should be either 1 (1000ms), 0.1 (100ms), 0.01 (10 ms) or 0.001 (1ms).')
    print(f'Read: {small_filename}.')
    d = pd.read_csv(small_filename, parse_dates=True, index_col=0)
    exponents = dict({1: 9, 0.1: 8, 0.01: 7, 0.001: 6})
    d['timestamp'] = d.index.values.astype(np.int64) // 10 ** exponents[precision_in_seconds]
    return d


def bitcoin_data(exchange_1_small_data_file: str, exchange_2_small_data_file: str, precision_in_seconds=1):
    exchange_1 = read_small_data(exchange_1_small_data_file, precision_in_seconds)
    exchange_2 = read_small_data(exchange_2_small_data_file, precision_in_seconds)
    return exchange_1[['timestamp', 'last']].values, exchange_2[['timestamp', 'last']].values
