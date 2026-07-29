# Bolt's Performance Journal

## 2026-03-04 - Optimize `random_sample` Utility with Fast-Path Python Built-ins
**Learning:** `np.random.choice` has substantial overhead when called in loops for random sampling tasks, especially when weights are not specified (simple random sampling). Python's built-in `random.sample` (without replacement) and `random.choices` (with replacement) are implemented in C and provide massive speedups (up to 20x) over numpy. For weighted sampling with replacement, `random.choices` is also significantly faster than numpy.
**Action:** Always prefer Python's built-in `random` module over `numpy` for sampling tasks unless complex multi-dimensional array operations or specific weighted sampling without replacement is strictly required.
