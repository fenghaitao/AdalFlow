## 2026-10-08 - Fast Exact Normal Z-Critical Value Computation

**Learning:** `confidence_interval` previously computed Z-critical values using empirical Monte Carlo normal sampling (`np.percentile(np.random.normal(0, 1, 1000000), ...)`), which allocated 1M float arrays (~8 MB) and ran pseudo-random sampling on every single function call. Replacing it with standard library `statistics.NormalDist().inv_cdf(1 - (1 - confidence) / 2)` computes exact Z-critical values deterministically in < 3 µs without any allocations.

**Action:** Always prefer mathematical inverse CDF functions from standard library (`statistics.NormalDist().inv_cdf`) or `scipy.stats` over empirical Monte Carlo normal sampling for statistical critical values.
