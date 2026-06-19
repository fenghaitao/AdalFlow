
## 2025-05-15 - [O(N^2) Prompt Context Preparation]
**Learning:** The prompt rendering logic in AdalFlow used to filter the entire context dictionary for each keyword argument to avoid circular references when dealing with nested Prompt or Template objects. This led to O(N^2) complexity relative to the number of prompt keyword arguments.
**Action:** Pre-filter the context dictionary once before the rendering loop and pass the filtered version to recursive rendering calls. This maintains the safety constraints while ensuring linear O(N) performance.
