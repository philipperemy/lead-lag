import numpy as np

from contrast import CrossCorrelationHY


def run():
    # ===== DATA PART =====
    print('Using synthetic data (Bachelier).')
    from scripts.read_bachelier_data import bachelier_data
    x, y, t_x, t_y, true_lead_lag = bachelier_data()
    # ===== DATA PART =====

    # ===== COMPUTATION ====
    gn_max = true_lead_lag * 2
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
    estimated_lead_lag = lag_range[est_lead_lag_index]
    print('Est. lead lag =', estimated_lead_lag)
    assert estimated_lead_lag == true_lead_lag, 'Estimation does not match the ground truth.'
    # ===== COMPUTATION ====


if __name__ == '__main__':
    run()
