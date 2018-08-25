from time import time

import numpy as np
import os
import pandas as pd
from glob import glob


def parallel_function(f, sequence, num_threads=None):
    from multiprocessing import Pool
    pool = Pool(processes=num_threads)
    result = pool.map(f, sequence)
    cleaned = [x for x in result if x is not None]
    pool.close()
    pool.join()
    return cleaned


class CrossCorrelationHY:

    def __init__(self, x, y, t_x, t_y, lag_range, normalize=True):
        self.x = np.array(x)
        self.y = np.array(y)
        self.t_x = np.array(t_x)
        self.t_y = np.array(t_y)
        self.lag_range = lag_range
        self.normalize = normalize
        if len(glob('lead_lag*.so')) == 0:
            print('The library has not been compiled. It will run much slower.')
            print('Run: make.')

    def fast_inference(self, num_threads=int(os.cpu_count() // 2)):
        contrast = parallel_function(self.call, self.lag_range, num_threads=num_threads)
        return contrast

    def slow_inference(self):
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
              f'has completed and it took {end_time-start_time:.2f} seconds.')
        return value

    def write_results_to_file(self, filename, contrasts):
        out = pd.DataFrame(data=np.transpose([self.lag_range, contrasts]), columns=['LagRange', 'Contrast'])
        out.to_csv(path_or_buf=filename, index=False)