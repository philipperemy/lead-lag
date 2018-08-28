import numpy as np

from contrast import CrossCorrelationHY


def run():
    # ===== DATA PART =====
    print('Using synthetic data (Bachelier).')
    from scripts.read_bachelier_data import bachelier_data
    x, y, t_x, t_y, true_lead_lag = bachelier_data()
    # ===== DATA PART =====

    # ===== COMPUTATION ====
    from time import time
    a = time()
    contrasts = CrossCorrelationHY(x, y, t_x, t_y, [-200, 200, 0, 60], normalize=True).slow_inference()
    print(time() - a)
    expect = np.array([0.014287344345994381, 0.6398660339145387, 0.048185364483985596, 0.1082638625479051])
    np.testing.assert_almost_equal(contrasts, expect, decimal=3)
    print(contrasts)


if __name__ == '__main__':
    run()
