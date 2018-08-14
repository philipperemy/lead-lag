import datetime
import numpy as np
import pandas as pd


# 1533513601210,7030.01,7030,7030,6243.92745609

def main2():
    date = '20180802'
    print(f'Reading for date {date}.')
    gdax = read_dataset([f'gdax_{date}.ts2'])
    kucoin = read_dataset([f'kucoin_{date}.ts2'])

    kucoin_arr = kucoin[['timestamp', 'last']].values
    gdax_arr = gdax[['timestamp', 'last']].values

    kucoin_arr[:, 0] = np.round(kucoin_arr[:, 0] / 100).astype(np.int)
    gdax_arr[:, 0] = np.round(gdax_arr[:, 0] / 100).astype(np.int)

    time_origin = min(kucoin_arr[0, 0], gdax_arr[0, 0])
    kucoin_arr[:, 0] -= time_origin
    gdax_arr[:, 0] -= time_origin
    time_end = int(max(kucoin_arr[-1, 0], gdax_arr[-1, 0]))

    kucoin_values = np.zeros(shape=time_end + 1) * np.nan
    kucoin_t = []
    for element_slice in kucoin_arr:
        kucoin_values[int(element_slice[0])] = element_slice[1]
        kucoin_t.append(int(element_slice[0]))

    gdax_values = np.zeros(shape=time_end + 1) * np.nan
    gdax_t = []
    for element_slice in gdax_arr:
        gdax_values[int(element_slice[0])] = element_slice[1]
        gdax_t.append(int(element_slice[0]))

    return gdax_values, kucoin_values, gdax_t, kucoin_t


def unix_to_datetime(d):
    return datetime.datetime.fromtimestamp(d / 1000.0)


def read_dataset(filenames):
    dfs = []
    for filename in filenames:
        df = pd.read_csv(filename, parse_dates=False,
                         # 1533513601210,7030.01,7030,7030,6243.92745609
                         names=['timestamp', 'ask', 'bid', 'last', 'volume'])
        df['date'] = df['timestamp'].apply(unix_to_datetime)
        # df = df.set_index(df['date'])
        # df.drop('date', inplace=True, axis=1)
        dfs.append(df)
    result = pd.DataFrame(pd.concat(dfs))
    result = result[(result['last'] - result['last'].shift(1)) != 0]
    # result.sort_index(ascending=True, inplace=True)
    # result = result.resample('1H').mean()
    # result.fillna(inplace=True, method='ffill')
    return result


def main():
    # precise up to 0.1 second.

    date = '20180802'
    print(f'Reading for date {date}.')
    gdax = read_dataset([f'gdax_{date}.ts2'])
    kucoin = read_dataset([f'kucoin_{date}.ts2'])

    kucoin_arr = kucoin[['timestamp', 'last']].values
    gdax_arr = gdax[['timestamp', 'last']].values

    kucoin_arr[:, 0] = np.round(kucoin_arr[:, 0] / 100).astype(np.int)
    gdax_arr[:, 0] = np.round(gdax_arr[:, 0] / 100).astype(np.int)

    time_origin = min(kucoin_arr[0, 0], gdax_arr[0, 0])
    kucoin_arr[:, 0] -= time_origin
    gdax_arr[:, 0] -= time_origin
    time_end = int(max(kucoin_arr[-1, 0], gdax_arr[-1, 0]))

    kucoin_values = np.zeros(shape=time_end + 1) * np.nan
    kucoin_t = []
    for element_slice in kucoin_arr:
        kucoin_values[int(element_slice[0])] = element_slice[1]
        kucoin_t.append(int(element_slice[0]))

    gdax_values = np.zeros(shape=time_end + 1) * np.nan
    gdax_t = []
    for element_slice in gdax_arr:
        gdax_values[int(element_slice[0])] = element_slice[1]
        gdax_t.append(int(element_slice[0]))

    return gdax_values, kucoin_values, gdax_t, kucoin_t

    # import matplotlib.pyplot as plt
    # plt.scatter(range(len(gdax_values)), gdax_values, color='blue', s=0.1)
    # plt.scatter(range(len(kucoin_values)), kucoin_values, color='orange', s=0.1)
    # plt.show()


if __name__ == '__main__':
    main()
