import numpy as np
from bisect import bisect_left


def overlap(min1, max1, min2, max2):
    return max(0, min(max1, max2) - max(min1, min2))


def overlap_1d(x):
    return max(0, min(x[1], x[3]) - max(x[0], x[2]))


def shifted_modified_hy_estimator(x, y, t_x, t_y, k, normalize=False):  # contrast function
    # print('Common Python.')
    hy_cov = 0.0
    if normalize:
        norm_x = np.sqrt(np.sum(np.square(np.diff(x[t_x]))))
        norm_y = np.sqrt(np.sum(np.square(np.diff(y[t_y]))))
    else:
        norm_x = 1.0
        norm_y = 1.0

    clipped_t_y_minus_k = np.clip(t_y - k, np.min(t_y), np.max(t_y))
    # Complexity: O(n log n)
    for ii in zip(t_x, t_x[1:]):  # O(n)
        ii0, ii1 = ii[0], ii[1]
        x_inc = (x[ii1] - x[ii0])
        mid_point_origin = bisect_left(clipped_t_y_minus_k, ii0)  # O(log n)
        if mid_point_origin is not None:
            mid_point = mid_point_origin
            # go left
            while True:
                if mid_point + 1 > len(t_y) - 1:
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
                if mid_point + 1 > len(t_y) - 1:
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

# def shifted_modified_hy_estimator_opt5(x, y, t_x, t_y, k, normalize=False):  # contrast function
#     # print('Common Python.')
#     hy_cov = 0.0
#     if normalize:
#         norm_x = np.sqrt(np.sum(np.square(np.diff(x[t_x]))))
#         norm_y = np.sqrt(np.sum(np.square(np.diff(y[t_y]))))
#     else:
#         norm_x = 1.0
#         norm_y = 1.0
#
#     clipped_t_y_minus_k = np.clip(t_y - k, np.min(t_y), np.max(t_y))
#     # Complexity: O(n log n)
#     for ii in zip(t_x, t_x[1:]):  # O(n)
#         mid_point_copy = bisect_left(clipped_t_y_minus_k, ii[0])  # O(log n)
#         if mid_point_copy is not None:
#             selected_jjs = []
#             mid_point = mid_point_copy
#             # go left
#             while True:
#                 if mid_point + 1 > len(t_y) - 1:
#                     break
#                 jj = (t_y[mid_point], t_y[mid_point + 1])
#                 if overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0:
#                     selected_jjs.append([jj[0], jj[1]])
#                     mid_point += 1
#                 else:
#                     break
#             # go right
#             mid_point = mid_point_copy - 1
#             while True:
#                 if mid_point + 1 > len(t_y) - 1:
#                     break
#                 jj = (t_y[mid_point], t_y[mid_point + 1])
#                 if overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0:
#                     selected_jjs.append([jj[0], jj[1]])
#                     mid_point -= 1
#                 else:
#                     break
#         else:
#             raise Exception('Problem happened with bisect_left().')
#
#         x_inc = (x[ii[1]] - x[ii[0]])
#         for jj in selected_jjs:
#             # overlap_term = overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0
#             hy_cov += x_inc * (y[jj[1]] - y[jj[0]])  # * overlap_term
#
#     return np.abs(hy_cov) / (norm_x * norm_y)  # product of norm is positive.

# def shifted_modified_hy_estimator_opt_4(x, y, t_x, t_y, k, normalize=False):  # contrast function
#     # print('Common Python.')
#     hy_cov = 0.0
#     if normalize:
#         norm_x = 0.0
#         for ii in zip(t_x, t_x[1:]):
#             norm_x += (x[ii[1]] - x[ii[0]]) ** 2
#         norm_x = np.sqrt(norm_x)
#         norm_y = 0.0
#         for jj in zip(t_y, t_y[1:]):
#             norm_y += (y[jj[1]] - y[jj[0]]) ** 2
#         norm_y = np.sqrt(norm_y)
#     else:
#         norm_x = 1.0
#         norm_y = 1.0
#
#     clipped_t_y_minus_k = np.clip(t_y - k, np.min(t_y), np.max(t_y))
#
#     # Complexity: O(n log n)
#     for ii in zip(t_x, t_x[1:]):  # O(n)
#         mid_point_copy = bisect_left(clipped_t_y_minus_k, ii[0])  # O(log n)
#         x_inc = (x[ii[1]] - x[ii[0]])
#         if mid_point_copy is not None:
#             selected_jjs = []
#             mid_point = mid_point_copy
#             while True:
#                 if mid_point + 1 > len(t_y) - 1:
#                     break
#                 jj = (t_y[mid_point], t_y[mid_point + 1])
#                 if overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0:
#                     selected_jjs.append([jj[0], jj[1]])
#                     mid_point += 1
#                 else:
#                     break
#
#             # go right
#             mid_point = mid_point_copy - 1
#             while True:
#                 if mid_point + 1 > len(t_y) - 1:
#                     break
#                 jj = (t_y[mid_point], t_y[mid_point + 1])
#                 if overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0:
#                     selected_jjs.append([jj[0], jj[1]])
#                     mid_point -= 1
#                 else:
#                     break
#         else:
#             selected_jjs = list(zip(t_y, t_y[1:]))
#
#         for jj in selected_jjs:
#             increments_mul = x_inc * (y[jj[1]] - y[jj[0]])
#             # overlap_term = overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0
#             hy_cov += increments_mul  # * overlap_term
#
#     hy_cov /= (norm_x * norm_y)
#     return np.abs(hy_cov)

# def shifted_modified_hy_estimator_opt2(x, y, t_x, t_y, k, normalize=False):  # contrast function
#     hy_cov = 0.0
#     if normalize:
#         norm_x = 0.0
#         for ii in zip(t_x, t_x[1:]):
#             norm_x += (x[ii[1]] - x[ii[0]]) ** 2
#         norm_x = np.sqrt(norm_x)
#         norm_y = 0.0
#         for jj in zip(t_y, t_y[1:]):
#             norm_y += (y[jj[1]] - y[jj[0]]) ** 2
#         norm_y = np.sqrt(norm_y)
#     else:
#         norm_x = 1.0
#         norm_y = 1.0
#
#     import random
#     jjs = list(zip(t_y, t_y[1:]))
#     jjs_indexes = list(range(len(jjs)))
#     random.shuffle(jjs_indexes)
#     for ii in zip(t_x, t_x[1:]):
#         mid_point_copy = None
#         for jj_index in jjs_indexes:
#             jj = list(jjs[jj_index])
#             if overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0:
#                 mid_point_copy = jj_index
#                 break
#
#         if mid_point_copy is not None:
#             hola = []
#             mid_point = mid_point_copy
#             while True:
#                 if mid_point + 1 > len(t_y) - 1:
#                     break
#                 jj = (t_y[mid_point], t_y[mid_point + 1])
#                 if overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0:
#                     hola.append([jj[0], jj[1]])
#                     mid_point += 1
#                 else:
#                     break
#
#             # go right
#             mid_point = mid_point_copy - 1
#             while True:
#                 if mid_point + 1 > len(t_y) - 1:
#                     break
#                 jj = (t_y[mid_point], t_y[mid_point + 1])
#                 if overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0:
#                     hola.append([jj[0], jj[1]])
#                     mid_point -= 1
#                 else:
#                     break
#         else:
#             hola = jjs
#
#         for jj in hola:
#             increments_mul = (x[ii[1]] - x[ii[0]]) * (y[jj[1]] - y[jj[0]])
#             overlap_term = overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0
#             hy_cov += increments_mul * overlap_term
#
#     hy_cov /= (norm_x * norm_y)
#     return np.abs(hy_cov)


# def shifted_modified_hy_estimator(x, y, t_x, t_y, k, normalize=False):  # contrast function
#     hy_cov = 0.0
#     if normalize:
#         norm_x = 0.0
#         for ii in zip(t_x, t_x[1:]):
#             norm_x += (x[ii[1]] - x[ii[0]]) ** 2
#         norm_x = np.sqrt(norm_x)
#         norm_y = 0.0
#         for jj in zip(t_y, t_y[1:]):
#             norm_y += (y[jj[1]] - y[jj[0]]) ** 2
#         norm_y = np.sqrt(norm_y)
#     else:
#         norm_x = 1.0
#         norm_y = 1.0
#
#     # t_y_arr = np.array(list(zip(t_y, t_y[1:])))
#     # max_time_per_index_y = max(t_y_arr[:, 1] - t_y_arr[:, 0])
#
#     for ii in zip(t_x, t_x[1:]):
#         # overlap_terms = []
#         # we can go left and go right as long as
#         print(ii)
#         mid_point_copy = take_closest(t_y - k, int((ii[1] - ii[0]) // 2))
#         jjs = []
#         # go left.
#         mid_point = mid_point_copy
#         while True:
#             jj = (t_y[mid_point], t_y[mid_point + 1])
#             if overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0:
#                 jjs.append([jj[0], jj[1]])
#                 mid_point += 1
#             else:
#                 break
#
#         # go right
#         mid_point = mid_point_copy - 1
#         while True:
#             jj = (t_y[mid_point], t_y[mid_point + 1])
#             if overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0:
#                 jjs.append([jj[0], jj[1]])
#                 mid_point -= 1
#             else:
#                 break
#
#         for jj in jjs:
#             increments_mul = (x[ii[1]] - x[ii[0]]) * (y[jj[1]] - y[jj[0]])
#             overlap_term = overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0
#             hy_cov += increments_mul * overlap_term
#             # overlap_terms.append(overlap_term)
#             # nonzero = np.nonzero(np.array(overlap_terms, dtype=int))
#             # print(nonzero[0], nonzero[-1])
#     hy_cov /= (norm_x * norm_y)
#     return np.abs(hy_cov)


# def shifted_modified_hy_estimator(x, y, t_x, t_y, k, normalize=False):  # contrast function
#     hy_cov = 0.0
#     if normalize:
#         norm_x = 0.0
#         for ii in zip(t_x, t_x[1:]):
#             norm_x += (x[ii[1]] - x[ii[0]]) ** 2
#         norm_x = np.sqrt(norm_x)
#         norm_y = 0.0
#         for jj in zip(t_y, t_y[1:]):
#             norm_y += (y[jj[1]] - y[jj[0]]) ** 2
#         norm_y = np.sqrt(norm_y)
#     else:
#         norm_x = 1.0
#         norm_y = 1.0
#
#     for ii in zip(t_x, t_x[1:]):
#         overlaps = []
#         lll = list(zip(t_y, t_y[1:]))
#         for jj in lll:
#             increments_mul = (x[ii[1]] - x[ii[0]]) * (y[jj[1]] - y[jj[0]])
#             overlap_term = overlap(ii[0], ii[1], max(jj[0] - k, 0), max(jj[1] - k, 0)) > 0.0
#             hy_cov += increments_mul * overlap_term
#             overlaps.append(overlap_term)
#         winners = list(np.where(np.array(overlaps) != 0)[0])
#         if len(winners) > 0:
#             print(ii)
#             # print(ii, [lll[w] for w in winners])
#     hy_cov /= (norm_x * norm_y)
#     return np.abs(hy_cov)


# def shifted_modified_hy_estimator_opt1(x, y, t_x, t_y, k, normalize=False):  # contrast function
#     print('Optimisation 1.')
#     hy_cov = 0.0
#     if normalize:
#         norm_x = 0.0
#         for ii in zip(t_x, t_x[1:]):
#             norm_x += (x[ii[1]] - x[ii[0]]) ** 2
#         norm_x = np.sqrt(norm_x)
#         norm_y = 0.0
#         for jj in zip(t_y, t_y[1:]):
#             norm_y += (y[jj[1]] - y[jj[0]]) ** 2
#         norm_y = np.sqrt(norm_y)
#     else:
#         norm_x = 1.0
#         norm_y = 1.0
#     for ii in zip(t_x, t_x[1:]):
#         last_overlap_term = 0
#         for jj in zip(t_y, t_y[1:]):
#             increments_mul = (x[ii[1]] - x[ii[0]]) * (y[jj[1]] - y[jj[0]])
#             overlap_term = overlap(ii[0], ii[1], jj[0] - k, jj[1] - k) > 0.0
#             if overlap_term == 0 and last_overlap_term != 0:
#                 break
#             last_overlap_term = overlap_term
#             hy_cov += increments_mul * overlap_term
#     hy_cov /= (norm_x * norm_y)
#     return np.abs(hy_cov)
