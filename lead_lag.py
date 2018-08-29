from time import time

import numpy as np
import pandas as pd

from contrast import CrossCorrelationHY
from scripts.read_bitcoin_data import bitcoin_data


class LeadLag:

    def __init__(self, csv_file_1: str,
                 csv_file_2: str,
                 max_absolute_lag: int,
                 verbose: bool):
        self.contrasts = None
        x, y, t_x, t_y = bitcoin_data(csv_file_1, csv_file_2)
        self.lag_range = np.arange(-max_absolute_lag, max_absolute_lag + 1, 1)
        self.inference_time = None
        self.cc = CrossCorrelationHY(x, y, t_x, t_y, self.lag_range, normalize=True, verbose_mode=verbose)

    def run_inference(self, multi_threading=True):
        start_time = time()
        if multi_threading:
            self.contrasts = self.cc.fast_inference()
        else:
            self.contrasts = self.cc.slow_inference()
        self.inference_time = time() - start_time

    @property
    def lead_lag(self):
        return self.lag_range[np.argmax(self.contrasts)] if self.contrasts else None

    def write_results_to_file(self, output_filename):
        self._contrasts_to_df().to_csv(path_or_buf=output_filename)

    def _contrasts_to_df(self):
        df = pd.DataFrame(data=np.transpose([self.lag_range, self.contrasts]), columns=['LagRange', 'Contrast'])
        df.set_index('LagRange', inplace=True)
        return df

    def plot(self):
        import matplotlib.pyplot as plt
        if self.contrasts is not None:
            self._contrasts_to_df().plot()
            plt.show()
