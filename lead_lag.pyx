import numpy as np

"""
Used for Cython. This file will be converted to C code.
http://cython.org/
"""

def overlap(long min1, long max1, long min2, long max2):
    return max(0, min(max1, max2) - max(min1, min2))


def shifted_modified_hy_estimator(double[:] x, double[:] y,
                                  long[:] t_x, long[:] t_y,
                                  int k, normalize=False):  # contrast function
    cdef double hy_cov = 0.0
    cdef double norm_x = 0.0
    cdef double norm_y = 0.0
    cdef double increments_mul = 0.0
    cdef double overlap_term = 0.0

    if normalize:

        for ii in zip(t_x, t_x[1:]):
            norm_x += (x[ii[1]] - x[ii[0]]) ** 2
        norm_x = np.sqrt(norm_x)

        for jj in zip(t_y, t_y[1:]):
            norm_y += (y[jj[1]] - y[jj[0]]) ** 2
        norm_y = np.sqrt(norm_y)
    else:
        norm_x = 1.0
        norm_y = 1.0
    # print(norm_x, norm_y)
    for ii in zip(t_x, t_x[1:]):
        for jj in zip(t_y, t_y[1:]):
            increments_mul = (x[ii[1]] - x[ii[0]]) * (y[jj[1]] - y[jj[0]])
            overlap_term = overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0
            hy_cov += increments_mul * overlap_term
    hy_cov /= (norm_x * norm_y)
    return np.abs(hy_cov)
