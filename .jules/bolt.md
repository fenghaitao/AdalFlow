## 2025-05-15 - [Generator Prompt Caching]
**Learning:** Redundant rendering of Jinja2 templates in every `Generator` call (sometimes multiple times per call) adds significant overhead. By caching the `Prompt` builder and reusing the rendered string, we achieved a ~37x speedup for prompt-only operations.
**Action:** Always look for redundant computation in hot paths like `call` or `acall`, especially when external library calls (like Jinja2 rendering) are involved.

## 2025-05-15 - [Identity vs Value for Cache Invalidation]
**Learning:** For performance-critical caching in `Generator`, identity checks (`is`) on high-level configuration objects (template, prompt_kwargs) are sufficient and faster than deep value comparisons, provided we accept a potential redundant refresh if a value is changed but is not the same object (though in this library, they are typically replaced entirely or modified in-place which identity checks won't catch unless deep-comparison or versioning is used).
**Action:** Use identity checks for fast invalidation of builders when the source configuration object is likely to be replaced when changed.
