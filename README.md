# Estimation of the lead-lag from non-synchronous data
*Implementation of the paper https://arxiv.org/pdf/1303.4871.pdf*


## Abstract
We propose a simple continuous time model for modeling the lead-lag effect between two financial
assets. A two-dimensional process (Xt, Yt) reproduces a lead-lag effect if, for some time shift
ϑ ∈ R, the process (Xt, Yt+ϑ) is a semi-martingale with respect to a certain filtration. The
value of the time shift ϑ is the lead-lag parameter. Depending on the underlying filtration,
the standard no-arbitrage case is obtained for ϑ = 0. We study the problem of estimating the
unknown parameter ϑ ∈ R, given randomly sampled non-synchronous data from (Xt) and (Yt).
By applying a certain contrast optimization based on a modified version of the Hayashi–Yoshida
covariation estimator, we obtain a consistent estimator of the lead-lag parameter, together with
an explicit rate of convergence governed by the sparsity of the sampling design.

## Numerical Illustration on Simulated Data

### Non synchronous data

We simulate a lead-lag Bachelier model without drift with:
- N = 10,000 (grid on which we sample random arriving times for both X and Y).
- #I = 500
- #J = 3,000
- ρ = 0.80, x0 = 1.0, y0 = 2.1, s1 = 1.0, s2 = 1.5
- lead_lag = 200 (X is the leader, Y the lagger)
- finite grid Gn = [0, 400]

We show a realization of the process (Xt, Yt) and its corresponding Constrast vs Lag plot:

<p align="center">
  <img src="figures/Figure_1.png" width="500">
</p>


<p align="center">
  <img src="figures/Figure_2.png" width="500">
</p>

Clearly, the argmax of the constrast is located around the correct value (lead_lag = 200). We also observe some persistence in the constrast (I may have forgotten an extra term in the modified HY estimator). Even though X has a sampling rate 7x lower than Y, the estimator can still pick up the correct value.

## References
- [High-Frequency Covariance Estimates With Noisy and Asynchronous Financial Data](https://www.princeton.edu/~yacine/QMLE2D.pdf)
- [On covariance estimation of non-synchronously observed diffusion](http://www.ms.u-tokyo.ac.jp/~nakahiro/mypapers_for_personal_use/hayyos03.pdf)
- [Estimation of the lead-lag parameter from non-synchronous data](https://arxiv.org/pdf/1303.4871.pdf)
- https://stats.stackexchange.com/questions/235697/semi-martingale-vs-martingale-what-is-the-difference?rq=1
