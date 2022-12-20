from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from lead_lag import lag

print('processing...')
ts = pd.Series(
    data=np.cumsum(np.random.uniform(low=-1, high=1, size=1000)),
    index=[datetime(2022, 1, 1, 12, 0, 0) - timedelta(seconds=i) for i in range(1000)]
)
print('predicted lag=', lag(ts, ts.shift(-9), max_lag=10), '(answer is 9)')
