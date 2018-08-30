import numpy as np


def overlap(min1, max1, min2, max2):
    return max(0, min(max1, max2) - max(min1, min2))


def shifted_modified_hy_estimator(x, y, t_x, t_y, k, normalize=False):  # contrast function
    hy_cov = 0.0
    if normalize:
        norm_x = 0.0
        for ii in zip(t_x, t_x[1:]):
            norm_x += (x[ii[1]] - x[ii[0]]) ** 2
        norm_x = np.sqrt(norm_x)
        norm_y = 0.0
        for jj in zip(t_y, t_y[1:]):
            norm_y += (y[jj[1]] - y[jj[0]]) ** 2
        norm_y = np.sqrt(norm_y)
    else:
        norm_x = 1.0
        norm_y = 1.0
    for ii in zip(t_x, t_x[1:]):
        for jj in zip(t_y, t_y[1:]):
            increments_mul = (x[ii[1]] - x[ii[0]]) * (y[jj[1]] - y[jj[0]])
            overlap_term = overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0
            hy_cov += increments_mul * overlap_term
    hy_cov /= (norm_x * norm_y)
    return np.abs(hy_cov)
