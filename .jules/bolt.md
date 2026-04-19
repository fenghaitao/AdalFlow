## 2025-05-15 - [Generator] Lazy Prompt Builder Caching and Redundant Render Removal

**Learning:** Redundant instantiation of the `Prompt` component and double-rendering of templates in `Generator.call` were causing significant latency overhead (~2ms per call). In a library where components manage recursive state and parameters via custom `__setattr__`, internal caching must use `object.__setattr__` to avoid accidental registration of cached objects as subcomponents.

**Action:** Implement lazy caching for frequently used sub-components (like `Prompt`) and ensure `__setattr__` handles cache invalidation. Pass pre-rendered strings to downstream methods to eliminate redundant Jinja2 rendering.
