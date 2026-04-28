## 2025-05-15 - [Prompt Rendering & Generator Caching]
**Learning:** Jinja2 template parsing in `Prompt` instantiation takes ~3ms, which adds up significantly in tight loops. Additionally, recursive rendering logic (`_deep_render`) had O(N^2) complexity due to redundant filtering of keyword arguments within a loop.
**Action:** Always cache components that involve expensive parsing (like Jinja2) if they are reused. When implementing recursive rendering, pre-filter context dictionaries once to avoid O(N^2) bottlenecks when handling large numbers of keyword arguments.
