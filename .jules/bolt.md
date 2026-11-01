# Bolt's Performance Journal

This journal tracks critical learnings about performance optimizations in AdalFlow.

## 2026-10-31 - Analytical Normal Inverse CDF for Confidence Interval Calculation
**Learning:** Calculating z-critical values using empirical Monte Carlo random normal sampling (`np.random.normal(0, 1, 1000000)` and `np.percentile`) incurred huge performance penalties (~53ms and allocating 8MB RAM array per call) and suffered from stochastic variance. Using standard library `statistics.NormalDist().inv_cdf` evaluates the exact inverse cumulative distribution function analytically in O(1) time without heap allocations.
**Action:** When computing critical z-values, standard errors, or confidence bounds in statistics and evaluation modules, always prefer analytical inverse CDF (`statistics.NormalDist().inv_cdf` or `scipy.stats.norm.ppf`) over empirical random sampling.
