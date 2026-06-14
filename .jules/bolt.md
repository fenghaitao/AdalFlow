## 2025-05-22 - Prompt Object Caching in Generator
**Learning:** Instantiating a `Prompt` object in every call to `get_prompt` or `print_prompt` is expensive due to Jinja2 template parsing. Caching this object and using `object.__setattr__` to prevent it from being registered as a sub-component in the `Component` tree avoids redundant overhead and potential state synchronization issues.
**Action:** Implement lazy initialization and cache invalidation via `__setattr__` for internal helper objects that depend on component state.
