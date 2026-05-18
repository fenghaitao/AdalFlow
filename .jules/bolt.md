## 2025-05-22 - [Optimizing Prompt Context Rendering]
**Learning:** Redundant context filtering in recursive rendering functions like `_deep_render` can lead to $O(N^2)$ complexity when processing a large number of keyword arguments ($N$). For $N=2000$, this resulted in over 1 second of overhead per prompt rendering.
**Action:** Pre-filter context dictionaries once before entering loops that perform recursive rendering. Pass the pre-filtered context as an optional argument to child calls to ensure $O(N)$ linear complexity.
