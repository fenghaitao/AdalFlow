# Bolt's Journal

## Critical Learnings

## 2026-03-31 - Analytical Normal Inverse CDF for Confidence Interval
**Learning:** `np.percentile(np.random.normal(0, 1, 1000000), ...)` simulates Monte Carlo sampling to approximate standard normal quantiles, consuming ~55ms and allocating an 8MB NumPy float array on every single call. Standard library `statistics.NormalDist().inv_cdf` calculates exact quantiles analytically in <1 microsecond with zero heap buffer allocation.
**Action:** Always prefer analytical standard distribution functions from `statistics` or `scipy.special` over stochastic Monte Carlo sampling when computing theoretical distribution quantiles.
