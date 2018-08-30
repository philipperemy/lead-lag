import numpy as np

import lead_lag


def run():
    print('Using synthetic data (Bachelier).')
    from lead_lag.scripts.read_bachelier_data import bachelier_data
    x_with_ts, y_with_ts, true_lead_lag = bachelier_data()
    ll = lead_lag.LeadLag(x_with_ts, y_with_ts, max_absolute_lag=0, verbose=True, specific_lags=[-200, 0, 60, 200])
    ll.run_inference(multi_threading=False)
    expect = np.array([0.014287344345994381, 0.048185364483985596, 0.1082638625479051, 0.6398660339145387])
    np.testing.assert_almost_equal(ll.contrasts, expect, decimal=3)
    print('PASSED.')
    ll.plot_data()
    ll.plot_results()
    print(ll.llr)


if __name__ == '__main__':
    run()
