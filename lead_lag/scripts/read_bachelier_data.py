import numpy as np


def sample_from_bachelier(rho=0.8, n=1000, lag=200):
    # s1, s2 = 1.0, 1.5
    s1 = 1.0

    dt = 0.1

    b1s = np.random.normal(loc=0.0, scale=s1 ** 2 * dt, size=n)
    b2s = rho * b1s + np.sqrt(1 - rho ** 2) * np.random.normal(loc=0.0, scale=dt, size=n)
    b2s = np.roll(b2s, shift=lag)

    x_t = np.cumsum(b1s)
    y_t = np.cumsum(b2s)

    a = np.insert(np.diff(x_t), 0, b1s[0], 0)
    b = np.insert(np.diff(y_t), 0, b2s[0], 0)
    np.testing.assert_almost_equal(a, b1s)
    np.testing.assert_almost_equal(b, b2s)
    # print(np.corrcoef(a, np.roll(b, shift=-lag)))

    return x_t, y_t, lag


def bachelier_data(rho=0.8, lead_lag=200, n=10_000, num_s1=500, num_s2=3_000):
    # only the case where the lead lag is positive is considered here.
    # to make it negative it should be pretty straightforward.
    np.random.seed(129)
    x, y, true_lag = sample_from_bachelier(rho=rho, n=n, lag=lead_lag)
    t_x = sorted(np.random.choice(range(n), size=num_s1, replace=False))
    t_y = sorted(np.random.choice(range(n), size=num_s2, replace=False))

    # # just for plotting purposes.
    # bb_x = np.zeros(shape=n) * np.nan
    # for t in t_x:
    #     bb_x[t] = x[t]
    # bb_y = np.zeros(shape=n) * np.nan
    # for t in t_y:
    #     bb_y[t] = y[t]

    # import matplotlib.pyplot as plt
    # plt.title('Non-synchronous data with leader / lagger relationship')
    # plt.scatter(range(true_lag, n), bb_x[true_lag:], s=0.5, color='lime')
    # plt.scatter(range(true_lag, n), bb_y[true_lag:], s=0.5, color='blue')
    # plt.legend(['Leader (driver)', 'Lagger (follower)'])
    # plt.show()
    return np.transpose([t_x, x[t_x]]), np.transpose([t_y, y[t_y]]), lead_lag
