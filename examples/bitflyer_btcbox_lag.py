import pandas as pd
from matplotlib import pyplot as plt

import lead_lag


def plot_time_series(bitflyer: pd.Series, btcbox: pd.Series) -> None:
    d = pd.DataFrame(data={'bitflyer': bitflyer['last'], 'btcbox': btcbox['last']}).ffill().dropna()
    slice_d = d['2018-08-12 12:05:30':'2018-08-12 12:08:25']
    slice_d['bitflyer'].plot(color='blue', linewidth=2, x_compat=True, legend='b')
    slice_d['btcbox'].plot(color='limegreen', linewidth=2, x_compat=True, legend='b')
    plt.grid(True)
    plt.title('Bitflyer vs Btcbox (2018, on 1s data)')
    plt.xlabel('Time')
    plt.ylabel('Bitcoin price (Yen)')
    plt.show()


def main():
    bitflyer = pd.read_csv('../data/bitflyerJPY_2018-08-12_small.csv', parse_dates=True, index_col=0)
    btcbox = pd.read_csv('../data/btcboxJPY_2018-08-12_small.csv', parse_dates=True, index_col=0)
    plot_time_series(bitflyer, btcbox)

    ll = lead_lag.LeadLag(
        ts1=bitflyer['last'],
        ts2=btcbox['last'],
        max_lag=30,  # [-X seconds, +X seconds]
        verbose=True,
        min_precision=0.1  # in seconds.
    )

    print('Running inference...')
    ll.run_inference()
    print(f'Estimated lag: {ll.lead_lag} seconds (bitflyer leading).')
    print(f'Positive lag means TS1 is leading. LLR: {ll.llr:.2f} (cf. paper for the definition of LLR).')
    ll.plot_results()


if __name__ == '__main__':
    main()
