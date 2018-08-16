import numpy as np

from contrast import CrossCorrelationHY


def run():
    # ===== DATA PART =====
    use_synthetic_data = False

    if use_synthetic_data:
        print('Using synthetic data (Bachelier).')
        from scripts.read_bachelier_data import bachelier_data
        x, y, t_x, t_y, lead_lag = bachelier_data()
    else:
        print('Using bitcoin data.')
        from scripts.read_bitcoin_data import bitcoin_data
        x, y, t_x, t_y = bitcoin_data()
        # in that case we don't know the lead lag so we can just set a big value here.
        lead_lag = 20
    # ===== DATA PART =====

    # ===== TEST PART =====
    print('Starting test phase...')
    test_lag_range = [-20, 40, 0, 10, 50, 32, 31, 83]
    contrasts_1 = CrossCorrelationHY(x, y, t_x, t_y, test_lag_range, normalize=True).fast_inference()
    contrasts_2 = CrossCorrelationHY(x, y, t_x, t_y, test_lag_range, normalize=True).slow_inference()
    np.testing.assert_almost_equal(contrasts_1, contrasts_2)
    print('Test phase completed [success]...')
    # ===== TEST PART =====

    # ===== COMPUTATION ====
    gn_max = lead_lag * 2
    print('Now computing the contrasts... The complexity is O(N^2). So be (very) patient..')
    lag_range = np.arange(-gn_max, gn_max, 1)
    contrasts = CrossCorrelationHY(x, y, t_x, t_y, lag_range, normalize=True).fast_inference()

    import matplotlib.pyplot as plt
    plt.title('Contrast = f(Lag)')
    plt.ylabel('Contrast')
    plt.xlabel('Lag')
    plt.plot(lag_range, contrasts)
    plt.show()

    # could have a better granularity.
    est_lead_lag_index = np.argmax(contrasts)
    print('Est. lead lag =', lag_range[est_lead_lag_index])
    # ===== COMPUTATION ====


if __name__ == '__main__':
    run()
