cimport cython
import numpy as np
from bisect import bisect_left

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
    cdef int i = 0
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
    # print('Cython 1.2 v5')
    cdef long double hy_cov = 0.0
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

    cdef int ii0, ii1, jj0, jj1;
    clipped_t_y_minus_k = np.clip(np.array(t_y) - k, int(np.min(t_y)), int(np.max(t_y)))
    # Complexity: O(n log n)
    for ii in zip(t_x, t_x[1:]):  # O(n)
        ii0, ii1 = ii[0], ii[1]
        x_inc = (x[ii1] - x[ii0])
        mid_point_origin = bisect_left(clipped_t_y_minus_k, ii0)  # O(log n)
        if mid_point_origin is not None:
            # if mid_point_origin < 0:
            #     mid_point_origin = 0
            # if mid_point_origin >= len(t_y):
            #     mid_point_origin = len(t_y) - 1

            # go left
            mid_point = mid_point_origin
            while True:
                if mid_point + 1 > len(t_y) - 1 or mid_point < 0:
                    break
                jj0, jj1 = (t_y[mid_point], t_y[mid_point + 1])
                if overlap(ii0, ii1, jj0 - k, jj1 - k) > 0.0:
                    hy_cov += (y[jj1] - y[jj0]) * x_inc
                    mid_point += 1
                else:
                    break
            # go right
            mid_point = mid_point_origin - 1
            while True:
                if mid_point + 1 > len(t_y) - 1 or mid_point < 0:
                    break
                jj0, jj1 = (t_y[mid_point], t_y[mid_point + 1])
                if overlap(ii0, ii1, jj0 - k, jj1 - k) > 0.0:
                    hy_cov += (y[jj1] - y[jj0]) * x_inc
                    mid_point -= 1
                else:
                    break
        else:
            raise Exception('Problem happened with bisect_left().')

    return np.abs(hy_cov) / (norm_x * norm_y)  # product of norm is positive.
