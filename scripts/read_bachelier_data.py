import numpy as np


def sample_from_bachelier(rho=0.8, n=1000, lag=200):
    x0, y0 = 1.0, 2.1
    s1, s2 = 1.0, 1.5

    dt = 0.1
    x = x0
    y = y0
    x_t = np.zeros(shape=n)
    y_t = np.zeros(shape=n)
    for k in range(n):
        b1 = np.random.normal(loc=0.0, scale=s1 ** 2 * dt)
        b2 = rho * b1 + np.sqrt(1 - rho ** 2) * np.random.normal(loc=0.0, scale=dt)
        x += b1
        y += b2
        x_t[k] = x
        y_t[k] = y

    y_t = np.roll(y_t, shift=lag)

    return x_t, y_t, lag


def bachelier_data():
    n = 10_000
    # only the case where the lead lag is positive is considered here.
    # to make it negative it should be pretty straightforward.
    lead_lag = 200
    np.random.seed(129)
    x, y, true_lag = sample_from_bachelier(rho=0.8, n=n, lag=lead_lag)
    t_x = sorted(np.random.choice(range(n), size=500, replace=False))
    t_y = sorted(np.random.choice(range(n), size=3_000, replace=False))

    # just for plotting purposes.
    bb_x = np.zeros(shape=n) * np.nan
    for t in t_x:
        bb_x[t] = x[t]
    bb_y = np.zeros(shape=n) * np.nan
    for t in t_y:
        bb_y[t] = y[t]

    # import matplotlib.pyplot as plt
    # plt.title('Non-synchronous data with leader / lagger relationship')
    # plt.scatter(range(true_lag, n), bb_x[true_lag:], s=0.5, color='lime')
    # plt.scatter(range(true_lag, n), bb_y[true_lag:], s=0.5, color='blue')
    # plt.legend(['Leader (driver)', 'Lagger (follower)'])
    # plt.show()
    return x, y, t_x, t_y, lead_lag