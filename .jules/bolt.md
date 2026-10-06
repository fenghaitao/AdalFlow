## 2025-05-20 - Exact standard normal inverse CDF vs. Monte Carlo sampling for confidence intervals

**Learning:** `confidence_interval` in `adalflow.eval.functional` previously computed standard normal Z-critical values by generating 1,000,000 empirical normal samples (`np.random.normal(0, 1, 1000000)`) and calculating `np.percentile`. This allocated 8MB of memory per call and took ~50ms per evaluation. Using Python standard library `statistics.NormalDist().inv_cdf(1 - (1 - confidence) / 2)` computes the exact Z-critical value deterministically in O(1) time without memory allocations, achieving a >25,000x speedup (~0.002ms per call).

**Action:** Always prefer mathematical inverse CDF functions (`statistics.NormalDist().inv_cdf` or `scipy.stats.norm.ppf`) over empirical Monte Carlo random sampling when calculating standard normal z-scores or confidence intervals.
