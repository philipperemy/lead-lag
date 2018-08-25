import warnings

warnings.filterwarnings('ignore', message='numpy.dtype size changed')
warnings.filterwarnings('ignore', message='numpy.ufunc size changed')

import datetime
import numpy as np
import os
import pandas as pd

EXCHANGE_1 = 'bitstamp'
EXCHANGE_2 = 'wex'
CURRENCY = 'USD'

prefix = os.path.join(os.path.dirname(__file__), '..', 'data2')

# http://api.bitcoincharts.com/v1/csv/ or https://github.com/philipperemy/bitcoin-market-data
exchange_2_data_raw_file = os.path.join(prefix, f'{EXCHANGE_2}{CURRENCY}.csv')
exchange_1_data_raw_file = os.path.join(prefix, f'{EXCHANGE_1}{CURRENCY}.csv')


# exchange_2_small_data_file = os.path.join(prefix, f'{EXCHANGE_2}{CURRENCY}.csv.small')
# exchange_1_small_data_file = os.path.join(prefix, f'{EXCHANGE_1}{CURRENCY}.csv.small')


def process_raw_data(input_filename, select_day_start=-4,
                     select_day_end=-2):  # -2 => select yesterday. Today will be incomplete.

    def unix_to_datetime(d):
        return datetime.datetime.fromtimestamp(d)

    def to_days(df):
        return [g[1] for g in df.groupby([df.index.year, df.index.month, df.index.day])]  # DataFrame to List<Day>

    if not os.path.isfile(input_filename):
        print('Could not find the CSV file with raw data. '
              'Browse http://api.bitcoincharts.com/v1/csv/ and '
              'download one (unzip it first).')
        exit(1)
    else:
        print(f'Processing {input_filename}.')

    d = pd.read_csv(input_filename, parse_dates=False, names=['timestamp', 'last', 'volume'])
    d['date'] = d['timestamp'].apply(unix_to_datetime)
    d.set_index(d['date'], inplace=True)
    d.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
    d = d[(d['last'] - d['last'].shift(1)) != 0]
    d.drop(labels=['date', 'volume', 'timestamp'], axis=1, inplace=True)
    d_days = to_days(d)
    for d_day in d_days:
        date = str(d_day.index[0]).split(' ')[0]
        input_filename_wo_extension, extension = os.path.splitext(input_filename)
        input_filename = input_filename
        output_filename = input_filename_wo_extension + f'_{date}_small.csv'
        print(f'Writing to: {output_filename}.')
        d_day.to_csv(output_filename, index=True)
    # print(pd.concat(d_days[select_day_start:select_day_end]).head(30))
    # print(len(d_days), len(d_days[select_day_start:select_day_end]))
    # pd.concat(d_days[select_day_start:select_day_end]).to_csv(output_filename, index=True)


def bitcoin_data(exchange_1_small_data_file, exchange_2_small_data_file):
    return _build_from_small_dataset(exchange_1_small_data_file, exchange_2_small_data_file)


def _build_from_small_dataset(exchange_1_small_data_file, exchange_2_small_data_file):
    def read_small_data(small_filename):
        print(small_filename)
        d = pd.read_csv(small_filename, parse_dates=True, index_col=0)
        d['timestamp'] = d.index.values.astype(np.int64) // 10 ** 9
        # print(d.head())
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


# def build_and_plot():
#     exchange_1_values, exchange_2_values, _, _ = _build_from_small_dataset()
#     import matplotlib.pyplot as plt
#
#     x_axis = range(len(exchange_1_values))
#     plt.title('Bitcoin prices (JPY)')
#     plt.xlabel('Time (Seconds)')
#     plt.ylabel('Price (JPY)')
#     plt.plot(x_axis, exchange_1_values)
#     plt.plot(x_axis, exchange_2_values)
#     plt.legend([EXCHANGE_1, EXCHANGE_2])
#     plt.show()


if __name__ == '__main__':
    process_raw_data(exchange_2_data_raw_file)
    process_raw_data(exchange_1_data_raw_file)
    # build_and_plot()
