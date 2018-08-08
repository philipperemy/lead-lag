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


def overlap(min1, max1, min2, max2):
    return max(0, min(max1, max2) - max(min1, min2))


def shifted_modified_hy_estimator(x, y, t_x, t_y, k):  # contrast function
    hy_cov = 0.0
    for ii in zip(t_x, t_x[1:]):
        for jj in zip(t_y, t_y[1:]):
            increments_mul = (x[ii[1]] - x[ii[0]]) * (y[jj[1]] - y[jj[0]])
            overlap_term = overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0
            hy_cov += increments_mul * overlap_term
    return hy_cov


def run():
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

    import matplotlib.pyplot as plt
    plt.title('Non-synchronous data with leader / lagger relationship')
    plt.scatter(range(true_lag, n), bb_x[true_lag:], s=0.5, color='lime')
    plt.scatter(range(true_lag, n), bb_y[true_lag:], s=0.5, color='blue')
    plt.legend(['Leader (driver)', 'Lagger (follower)'])
    plt.show()

    gn_max = lead_lag * 2
    contrasts = np.zeros(gn_max)
    print('Now computing the contrasts... Be patient. It might take up to one hour.')
    for lead_lag_candidate in np.arange(0, gn_max, 1):
        v = np.abs(shifted_modified_hy_estimator(x, y, t_x, t_y, lead_lag_candidate))
        print(lead_lag_candidate, v)
        contrasts[lead_lag_candidate] = v

    plt.title('Contrast = f(Lag)')
    plt.ylabel('Contrast')
    plt.xlabel('Lag')
    plt.scatter(range(len(contrasts)), contrasts, s=10)
    plt.show()

    # could have a better granularity.
    est_lead_lag = np.argmax(contrasts)
    print('Est. lead lag =', est_lead_lag)


if __name__ == '__main__':
    run()
