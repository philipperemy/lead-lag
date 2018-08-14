import warnings

warnings.filterwarnings('ignore', message='numpy.dtype size changed')
warnings.filterwarnings('ignore', message='numpy.ufunc size changed')

import datetime
import numpy as np
import os
import pandas as pd

prefix = os.path.join(os.path.dirname(__file__), '..', 'data')

# http://api.bitcoincharts.com/v1/csv/ or https://github.com/philipperemy/bitcoin-market-data
btcbox_data_raw_file = os.path.join(prefix, 'btcboxJPY.csv')
bitflyer_data_raw_file = os.path.join(prefix, 'bitflyerJPY.csv')

btcbox_small_data_file = os.path.join(prefix, 'btcboxJPY.csv.small')
bitflyer_small_data_file = os.path.join(prefix, 'bitflyerJPY.csv.small')


def process_raw_data(input_filename, select_day=-2):  # -2 => select yesterday. Today will be incomplete.

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
    d_day = to_days(d)
    print(d_day[select_day].head(30))
    print(len(d_day), len(d_day[select_day]))
    output_filename = input_filename + '.small'
    print(f'Writing to: {output_filename}.')
    d_day[select_day].to_csv(output_filename, index=True)


def bitcoin_data():
    return _build_from_small_dataset()


def _build_from_small_dataset():
    def read_small_data(small_filename):
        d = pd.read_csv(small_filename, parse_dates=True, index_col=0)
        d['timestamp'] = d.index.values.astype(np.int64) // 10 ** 9
        # print(d.head())
        return d

    btcbox = read_small_data(btcbox_small_data_file)
    bitflyer = read_small_data(bitflyer_small_data_file)

    btcbox_arr = btcbox[['timestamp', 'last']].values
    bitflyer_arr = bitflyer[['timestamp', 'last']].values

    # btcbox_arr[:, 0] = np.round(btcbox_arr[:, 0] / 100).astype(np.int)
    # bitflyer_arr[:, 0] = np.round(bitflyer_arr[:, 0] / 100).astype(np.int)

    time_origin = min(btcbox_arr[0, 0], bitflyer_arr[0, 0])
    btcbox_arr[:, 0] -= time_origin
    bitflyer_arr[:, 0] -= time_origin
    time_end = int(max(btcbox_arr[-1, 0], bitflyer_arr[-1, 0]))

    btcbox_values = np.zeros(shape=time_end + 1) * np.nan
    btcbox_t = []
    for element_slice in btcbox_arr:
        btcbox_values[int(element_slice[0])] = element_slice[1]
        btcbox_t.append(int(element_slice[0]))

    bitflyer_values = np.zeros(shape=time_end + 1) * np.nan
    bitflyer_t = []
    for element_slice in bitflyer_arr:
        bitflyer_values[int(element_slice[0])] = element_slice[1]
        bitflyer_t.append(int(element_slice[0]))

    return bitflyer_values, btcbox_values, bitflyer_t, btcbox_t


def build_and_plot():
    bitflyer_values, btcbox_values, _, _ = _build_from_small_dataset()
    import matplotlib.pyplot as plt

    x_axis = range(len(bitflyer_values))
    plt.title('Bitcoin prices (JPY)')
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Price (JPY)')
    plt.plot(x_axis, bitflyer_values)
    plt.plot(x_axis, btcbox_values)
    plt.legend(['Bitflyer', 'Btcbox'])
    plt.show()


if __name__ == '__main__':
    process_raw_data(bitflyer_data_raw_file)
    process_raw_data(btcbox_data_raw_file)
    build_and_plot()
