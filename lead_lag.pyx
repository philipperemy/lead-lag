cimport cython
import numpy as np
import random
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


    jjs = list(zip(t_y, t_y[1:]))
    jjs_indexes = list(range(len(jjs)))
    random.shuffle(jjs_indexes)
    for ii in zip(t_x, t_x[1:]):

        mid_point_copy = bisect_left(np.clip(np.array(t_y) - k, np.min(t_y), np.max(t_y)), ii[0])
        if mid_point_copy is not None:
            selected_jjs = []
            mid_point = mid_point_copy
            while True:
                if mid_point + 1 > len(t_y) - 1:
                    break
                jj = (t_y[mid_point], t_y[mid_point + 1])
                if overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0:
                    selected_jjs.append([jj[0], jj[1]])
                    mid_point += 1
                else:
                    break

            # go right
            mid_point = mid_point_copy - 1
            while True:
                if mid_point + 1 > len(t_y) - 1:
                    break
                jj = (t_y[mid_point], t_y[mid_point + 1])
                if overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0:
                    selected_jjs.append([jj[0], jj[1]])
                    mid_point -= 1
                else:
                    break

        else:
            selected_jjs = jjs

        for jj in selected_jjs:
            increments_mul = (x[ii[1]] - x[ii[0]]) * (y[jj[1]] - y[jj[0]])
            overlap_term = overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0 # just in case.
            hy_cov += increments_mul * overlap_term

    hy_cov /= (norm_x * norm_y)
    return np.abs(hy_cov)
