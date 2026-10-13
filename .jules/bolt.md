
## 2025-05-18 - Exact analytical NormalDist inverse CDF for confidence intervals
**Learning:** `np.percentile(np.random.normal(0, 1, 1000000), ...)` was generating 1M normal random floats on every call to `confidence_interval` to empirically estimate Z-critical values. Using standard library `statistics.NormalDist().inv_cdf` calculates the exact mathematical inverse CDF in microseconds without array allocations.
**Action:** Always check for empirical Monte Carlo sampling in standard mathematical / statistical routines and replace them with standard library analytical functions when available.
