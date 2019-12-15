from collections import deque
from time import time

import numpy as np
import pandas as pd

from lead_lag.contrast import CrossCorrelationHY


class LeadLag:

    def __init__(self,
                 arr_1_with_ts: np.array,
                 arr_2_with_ts: np.array,
                 max_absolute_lag: int,
                 verbose: bool,
                 specific_lags=None):
        self.contrasts = None
        # lead format format is also useful for plotting.
        self.x, self.y, self.t_x, self.t_y, = convert_to_lead_lag_format(arr_1_with_ts, arr_2_with_ts)
        assert len(self.x) == len(self.y)
        if specific_lags is None:
            self.lag_range = np.arange(-max_absolute_lag, max_absolute_lag + 1, 1)
        else:
            if sorted(specific_lags) != specific_lags:
                raise Exception('Make sure the lag list passed as argument is sorted.')
            self.lag_range = np.array(specific_lags)
        self.inference_time = None
        self.cc = CrossCorrelationHY(self.x, self.y, self.t_x, self.t_y,
                                     self.lag_range, normalize=True, verbose_mode=verbose)

    def run_inference(self, multi_threading=True):
        start_time = time()
        if multi_threading:
            self.contrasts = self.cc.fast_inference()
        else:
            self.contrasts = self.cc.slow_inference()
        self.inference_time = time() - start_time

    @property
    def lead_lag(self):
        if self.contrasts is None:
            return None
        if np.std(self.contrasts) == 0.0:
            return None
        return self.lag_range[np.argmax(self.contrasts)]

    @property
    def llr(self):
        if self.contrasts is None:
            return None
        positive_range_indexes = self.lag_range > 0
        negative_range_indexes = self.lag_range < 0
        positive_contrasts = np.sum(self.contrasts[positive_range_indexes])
        negative_contrasts = np.sum(self.contrasts[negative_range_indexes])
        if negative_contrasts != 0.0:
            llr = positive_contrasts / negative_contrasts
        else:
            llr = np.nan
        return llr

    def write_results_to_file(self, output_filename):
        self._contrasts_to_df().to_csv(path_or_buf=output_filename)

    def _contrasts_to_df(self):
        df = pd.DataFrame(data=np.transpose([self.lag_range, self.contrasts]), columns=['LagRange', 'Contrast'])
        df.set_index('LagRange', inplace=True)
        return df

    def plot_results(self):
        import matplotlib.pyplot as plt
        if self.contrasts is not None:
            self._contrasts_to_df().plot()
            plt.show()

    def plot_data(self, legend=None):
        import matplotlib.pyplot as plt
        plt.title('Non-synchronous data with leader / lagger relationship')
        plt.xlabel('Time Axis (grid granularity)')
        plt.scatter(self.t_x, self.x[self.t_x], s=0.5, color='lime')
        plt.scatter(self.t_y, self.y[self.t_y], s=0.5, color='blue')
        if legend is None:
            plt.legend(['X(t)', 'Y(t)'])
        else:
            plt.legend(legend)
        plt.show()


def convert_to_lead_lag_format(arr1, arr2):
    assert len(arr1.shape) == 2  # (x, t_x)
    assert len(arr2.shape) == 2  # (y, t_y)
    time_origin = min(arr2[0, 0], arr1[0, 0])
    arr1[:, 0] -= time_origin
    arr2[:, 0] -= time_origin
    time_end = int(max(arr2[-1, 0], arr1[-1, 0]))
    x = np.zeros(shape=time_end + 1) * np.nan
    t_x = []
    for element_slice in arr1:
        x[int(element_slice[0])] = element_slice[1]
        t_x.append(int(element_slice[0]))
    y = np.zeros(shape=time_end + 1) * np.nan
    t_y = []
    for element_slice in arr2:
        y[int(element_slice[0])] = element_slice[1]
        t_y.append(int(element_slice[0]))
    return x, y, t_x, t_y


class RealTimeAggregator:

    def __init__(self, history_length):
        self.ts = deque(maxlen=history_length)

    def add(self, value: float, timestamp: int):
        self.ts.append((timestamp, value))

    def get(self):
        return np.vstack(self.ts)
