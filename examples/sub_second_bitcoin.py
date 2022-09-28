import numpy as np

import lead_lag
from lead_lag.scripts.read_bitcoin_data import bitcoin_data


def main():
    # Precision: 100ms. Valid values are 1 (1000ms), 0.1 (100ms), 0.01 (10ms), 0.001 (1ms).
    precision = 0.1
    # Range to find the lag is [-30, 30] for precision=1, [-300, 300] for precision=0.1, etc..
    max_lag = 3 * 10 ** (int(np.log10(1 / precision)) + 1)
    # Just for logging purposes.
    human_readable_precisions = {1: 'seconds', 0.1: '100ms', 0.01: '10ms', 0.001: '1ms'}

    # the data is up to the second in this example.
    bitflyer_with_ts, btcbox_with_ts = bitcoin_data(
        exchange_1_small_data_file='data/bitflyerJPY_2018-08-12_small.csv',
        exchange_2_small_data_file='data/btcboxJPY_2018-08-12_small.csv',
        precision_in_seconds=precision
    )

    ll = lead_lag.LeadLag(
        arr_1_with_ts=bitflyer_with_ts,
        arr_2_with_ts=btcbox_with_ts,
        max_absolute_lag=max_lag,
        verbose=False
    )

    ll.run_inference()
    precision_str = human_readable_precisions[precision]
    print(f'Estimated lag (with a precision of {precision_str}): {ll.lead_lag * precision} seconds.')
    print(f'Positive lag means bitflyer is leading. LLR: {ll.llr:.2f} (cf. paper for the definition of LLR).')
    ll.plot_data(legend=['Bitflyer', 'Btcbox'])
    ll.plot_results(precision=precision)


if __name__ == '__main__':
    main()
