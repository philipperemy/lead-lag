from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from lead_lag import LeadLag


def main():
    min_data_precision = 0.05  # 50ms.
    start = datetime.utcnow().replace(microsecond=0)
    timestamp = [start - timedelta(seconds=i) * min_data_precision for i in range(1000)]
    values = np.cumsum(np.random.uniform(low=-1, high=1, size=len(timestamp)))
    ts = pd.Series(data=values, index=timestamp)

    data_lag_in_seconds = 4
    ts_lag = ts.shift(-data_lag_in_seconds * int(1 / min_data_precision))
    d = pd.DataFrame(data={'ts_lag': ts_lag, 'ts': ts}).dropna()

    ll = LeadLag(ts1=d['ts'], ts2=d['ts_lag'], max_lag=10)
    print('Running inference...')
    ll.run_inference()
    print(f'Estimated lag is {ll.lead_lag} seconds. True lag was {data_lag_in_seconds} seconds.')
    print(f'Positive lag means ts1 is leading. LLR: {ll.llr:.2f} (cf. paper for the definition of LLR).')
    # ll.plot_results()


if __name__ == '__main__':
    main()
