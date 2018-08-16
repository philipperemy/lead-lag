cimport cython
import numpy as np

"""
Used for Cython. This file will be converted to C code.
http://cython.org/
"""

cdef extern from "math.h":
    double sqrt(double m)



cdef inline overlap(long min1, long max1, long min2, long max2):
    return max(0, min(max1, max2) - max(min1, min2)) > 0


@cython.boundscheck(False)
@cython.wraparound(False)
def l2_norm_of_arr_diff(long[:] t_x, double[:] x):
    cdef double norm_x = 0.0
    cdef long i1 = 0
    cdef long i2 = 0
    cdef double v1 = 0.0
    cdef double v2 = 0.0
    for i in range(len(t_x) - 1):
        i1 = t_x[i]
        i2 = t_x[i+1]
        v1 = x[i1]
        v2 = x[i2]
        norm_x += (v2 - v1) ** 2
    norm_x = sqrt(norm_x)
    return norm_x


@cython.boundscheck(False)
@cython.wraparound(False)
def shifted_modified_hy_estimator(double[:] x, double[:] y,
                                  long[:] t_x, long[:] t_y,
                                  int k, normalize=False):  # contrast function
    cdef double hy_cov = 0.0
    cdef double norm_x = 0.0
    cdef double norm_y = 0.0
    cdef double increments_mul = 0.0
    cdef double overlap_term = 0.0

    cdef int jj_0 = 0
    cdef int jj_1 = 0
    cdef int ii_0 = 0
    cdef int ii_1 = 0

    if normalize:
        norm_x = l2_norm_of_arr_diff(t_x, x)
        norm_y = l2_norm_of_arr_diff(t_y, y)
    else:
        norm_x = 1.0
        norm_y = 1.0

    for i in range(len(t_x) - 1):
        for j in range(len(t_y) - 1):
            jj_0 = t_y[j]
            jj_1 = t_y[j+1]
            ii_0 = t_x[i]
            ii_1 = t_x[i+1]
            hy_cov += (x[ii_1] - x[ii_0]) * (y[jj_1] - y[jj_0]) * overlap(ii_0, ii_1, jj_0 - k, jj_1 - k)

    hy_cov /= (norm_x * norm_y)
    return np.abs(hy_cov)
