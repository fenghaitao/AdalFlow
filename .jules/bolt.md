## 2025-05-14 - [Optimize Generator and Prompt rendering]
**Learning:** Significant performance gains can be achieved by caching core orchestration objects like `Prompt` and avoiding redundant expensive operations like Jinja2 rendering in high-frequency call paths.
**Action:** Use lazy-loading cached properties for complex sub-objects and ensure single-pass rendering in component pipelines.

## 2025-05-14 - [O(N^2) in Prompt kwargs rendering]
**Learning:** Iteratively calling `_deep_render` on every keyword argument in a `Prompt` call was causing O(N^2) complexity due to redundant scans/copies, especially with many standard string arguments.
**Action:** Implement fast-paths to skip complex rendering loops for primitive-only data and pre-calculate rendering context.
