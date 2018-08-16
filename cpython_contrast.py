from time import time
import numpy as np
from os import cpu_count


def parallel_function(f, sequence, num_threads=None):
    from multiprocessing import Pool
    pool = Pool(processes=num_threads)
    result = pool.map(f, sequence)
    cleaned = [x for x in result if x is not None]
    pool.close()
    pool.join()
    return cleaned


class CrossCorrelationHY:

    def __init__(self, x, y, t_x, t_y, lag_range, normalize):
        self.x = np.array(x)
        self.y = np.array(y)
        self.t_x = np.array(t_x)
        self.t_y = np.array(t_y)
        self.lag_range = lag_range
        self.normalize = normalize

    def fast_inference(self):
        print('Using fast_inference().')
        contrast = parallel_function(self.call, self.lag_range, num_threads=int(cpu_count() // 2))
        return contrast

    def slow_inference(self):
        print('Using slow_inference().')
        contrasts = []
        for k in self.lag_range:
            contrasts.append(self.call(k))
        return contrasts

    def call(self, k):
        from lead_lag import shifted_modified_hy_estimator
        start_time = time()
        value = shifted_modified_hy_estimator(self.x, self.y, self.t_x, self.t_y, k, self.normalize)
        end_time = time()
        print(f'Estimation of the cross correlation for lag [{k}] '
              f'completed and took {end_time-start_time:.2f} seconds.')
        return value
