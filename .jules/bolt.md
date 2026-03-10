## 2025-05-15 - [Generator Prompt Caching]
**Learning:** Re-instantiating the `Prompt` class and re-parsing Jinja2 templates on every `Generator` call is a significant performance bottleneck (accounting for ~97% of the `get_prompt` overhead). Caching the `Prompt` instance in the `Generator` and using identity checks (`is`) for cache invalidation provides a ~40x speedup.
**Action:** Always check for redundant object instantiation and template parsing in hot paths. Use private `_get_...` methods with lazy initialization for internal components.

## 2025-05-15 - [Prompt Rendering Micro-optimization]
**Learning:** Recursive rendering logic in `Prompt._deep_render` was performing expensive dictionary filtering even when no nested `Prompt` or `Template` objects were present. Deferring this filtering and adding an early-exit check in the parent caller improved rendering speed by ~50%.
**Action:** Profile recursive functions to identify operations that can be deferred or skipped. Use early-exit flags (like `has_complex_obj`) to bypass expensive processing blocks.
