import numpy as np

from contrast import CrossCorrelationHY


def run():
    # ===== DATA PART =====
    print('Using bitcoin data.')
    from scripts.read_bitcoin_data import bitcoin_data
    x, y, t_x, t_y = bitcoin_data()
    # in that case we don't know the lead lag so we can just set a big value here.
    # ===== DATA PART =====

    # import matplotlib.pyplot as plt
    # plt.title('Non-synchronous data with leader / lagger relationship')
    # plt.scatter(range(len(x)), x, s=0.5, color='lime')
    # plt.scatter(range(len(x)), y, s=0.5, color='blue')
    # plt.legend(['Bitstamp', 'WEX'])
    # plt.show()

    # ===== COMPUTATION ====
    max_lead_lag = 160  # in seconds.
    lag_range = np.arange(-max_lead_lag, max_lead_lag, 1)
    cc = CrossCorrelationHY(x, y, t_x, t_y, lag_range, normalize=True)
    contrasts = cc.fast_inference()
    cc.write_results_to_file('out.csv', contrasts)

    # for lag, contrast in zip(lag_range, contrasts):
    #     print(lag, contrast)

    # import matplotlib.pyplot as plt
    # plt.title('Contrast = f(Lag)')
    # plt.ylabel('Contrast')
    # plt.xlabel('Lag')
    # plt.plot(lag_range, contrasts)
    # plt.show()

    # could have a better granularity.
    est_lead_lag_index = np.argmax(contrasts)
    print('Est. lead lag =', lag_range[est_lead_lag_index])
    # ===== COMPUTATION ====


if __name__ == '__main__':
    run()
