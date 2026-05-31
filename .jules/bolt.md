
## 2026-05-31 - Optimized Prompt Rendering Complexity
**Learning:** Re-filtering the entire keyword argument dictionary for every template variable during prompt rendering leads to O(N²) complexity, which significantly degrades performance as the number of prompt variables grows.
**Action:** Pre-filter the context dictionary once to remove non-serializable objects (like Prompt or Template instances) and pass this pre-filtered dictionary to recursive rendering calls.
