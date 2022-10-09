## Lead Lag from non-synchronous data [[paper](https://arxiv.org/abs/1303.4871)]

> We propose a simple continuous time model for modeling the lead-lag effect between two financial
assets. A two-dimensional process (Xt, Yt) reproduces a lead-lag effect if, for some time shift
ϑ ∈ R, the process (Xt, Yt+ϑ) is a semi-martingale with respect to a certain filtration. The
value of the time shift ϑ is the lead-lag parameter. Depending on the underlying filtration,
the standard no-arbitrage case is obtained for ϑ = 0. We study the problem of estimating the
unknown parameter ϑ ∈ R, given randomly sampled non-synchronous data from (Xt) and (Yt).
By applying a certain contrast optimization based on a modified version of the Hayashi–Yoshida
covariation estimator, we obtain a consistent estimator of the lead-lag parameter, together with
an explicit rate of convergence governed by the sparsity of the sampling design. The complexity is
**O(n.LOG(n))**.

### API

Compute the lag in seconds between 2 time series in Python.

```python
lead_lag.lag(ts1: pd.Series, ts2: pd.Series, max_lag: Union[float, int]) -> Optional[float]
```

#### Arguments
- `ts1`: a Pandas Series.
- `ts2`: a Pandas Series.
- `max_lag`: the maximum lag to find in seconds. `max_lag` will define an interval to search for the best lag in `[max_lag, max_lag]`.

*NOTE*: the indexes of `ts1` and `ts2` do not need to match. The non-synchronous data is supported. At the moment, the minimum lag possible is 100 microseconds (for performance reasons).

#### Returns
The signed estimated `lag` (unit is second). If `lag>0`, `ts1` is the leader. If an error occurs, `None` is returned.

There is also a `lead_lag.LeadLag` object, which offers more features. Refer to the examples to learn how to use it.

### Example

Here is how the library works on the simplest example:

```python
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from lead_lag import lag

ts = pd.Series(
    data=np.cumsum(np.random.uniform(low=-1, high=1, size=1000)),
    index=[datetime(2022, 1, 1, 12, 0, 0) - timedelta(seconds=i) for i in range(1000)]
)
print('lag=', lag(ts, ts.shift(-9), max_lag=10))
# lag= 9.0
```

### Installation

Follow those steps to install it:

```bash
# 1. Recommended for all platforms.
pip install git+ssh://git@github.com/philipperemy/lead-lag

# 2. If you have python 3.9 and MacOS. Platform specific.
pip install lead_lag

# 3. Cloning the repository.
git clone git@github.com:philipperemy/lead-lag.git && cd lead-lag
virtualenv -p python3 venv && source venv/bin/activate
make
```

### More Examples

Browse the [examples](examples) directory to learn more about the lib:
- FTX vs Bitmex lead lag: FTX is leading Bitmex and the lag is 90ms on 2022-09-27.
- Bitflyer vs Btcbox lead lag: Bitflyer is leading Btcbox and the lag is 15s in 2018.

You can also run the Jupyter Notebook [lead_lag_example_2.ipynb](notebooks/lead_lag_example_2.ipynb):

```bash
make jupyter
```

### Numerical Illustrations

#### Non-synchronous data (generated from the Brownian Bachelier model)

We simulate a lead-lag Bachelier model without drift with: 

N = 10,000 (grid on which we sample random arriving times for both X and Y), #I = 500, #J = 3,000, ρ = 0.80, x0 = 1.0, y0 = 2.1, s1 = 1.0, s2 = 1.5, lead_lag = 200 (X is the leader, Y the lagger), finite grid Gn = [0, 400]. 

We show a realization of the process (Xt, Yt) and its corresponding Constrast vs Lag plot:

<p align="center">
  <img src="figures/Figure_1.png" width="400">
</p>


<p align="center">
  <img src="figures/Figure_2.png" width="400">
</p>

*The contrast is just a positive definitive cross correlation quantity.*

Clearly, the argmax of the contrast is located around the correct value (lead_lag = 200). We also observe some
persistence in the contrast (I may have forgotten an extra term in the modified HY estimator). Even though X has a
sampling rate 7x lower than Y, the estimator can still pick up the correct value. We can also normalize the contrast to
have an unbiased estimation of the cross correlation function rho for different lags. In theory this function should be
a Dirac centered around the lead_lag parameter with ρ(lead_lag) = 0.8 and 0 elsewhere.

<p align="center">
  <img src="figures/Figure_3.png" width="370">
</p>

We can also look at negative lags and define the LLR (standing for Lead/Lag Ratio) to measure the lead/lag
relationships. If LLR > 1, then X is the leader and Y the lagger and vice versa for LLR <= 1. In our case, for the
realization of our process (X,Y), we find LLR ~ 8.03.

<p align="center">
  <img src="figures/Figure_4.png" width="350">
</p>

#### Non-synchronous data (Bitcoin markets)

We now consider a real world use case where we have two Japanese bitcoin exchanges: bitflyer and btcbox. The former has
higher liquidity hence we expect it to lead the latter. If we plot the prices of BTC/JPY for both exchanges for a
specific day, we get:

<p align="center">
  <img src="figures/Figure_5.png" width="400">
</p>

So which one leads? We apply the same lead lag procedure using the constrast quantity computed on a
grid `Gn = ]-40,40[` (unit is second here).

<p align="center">
  <img src="figures/Figure_6.png" width="400">
</p>

The contrast is maximized for ϑ = 15 seconds. This promptly means that bitflyer is the leader as expected and that
btcbox takes on average 15 seconds to reflect any changes on its price.

### References

- [High-Frequency Covariance Estimates With Noisy and Asynchronous Financial Data](https://www.princeton.edu/~yacine/QMLE2D.pdf)
- [On covariance estimation of non-synchronously observed diffusion](http://www.ms.u-tokyo.ac.jp/~nakahiro/mypapers_for_personal_use/hayyos03.pdf)
- [Estimation of the lead-lag parameter from non-synchronous data](https://arxiv.org/pdf/1303.4871.pdf)
- https://stats.stackexchange.com/questions/235697/semi-martingale-vs-martingale-what-is-the-difference?rq=1
