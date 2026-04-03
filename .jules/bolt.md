## 2025-05-22 - Optimized Prompt Rendering (N^2)$ Bottleneck
**Learning:** In recursive rendering logic, performing context filtering (e.g., to avoid circular references) inside a loop over keyword arguments results in (N^2)$ complexity, which significantly impacts performance as the number of keywords grows.
**Action:** Always pre-filter or cache context transformations once per pass when iterating over large datasets or keyword dictionaries. Implement early exits for common cases (like string keywords) to avoid unnecessary overhead.
