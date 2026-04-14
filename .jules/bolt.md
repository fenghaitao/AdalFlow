## 2025-05-15 - [Prompt Builder Caching in Generator]
**Learning:** Re-instantiating the `Prompt` object in AdalFlow is expensive because it involves Jinja2 template parsing and variable discovery. For large templates, this can take several milliseconds (e.g., ~3.4ms), which dominates the overhead of a mock LLM call.

**Action:** Always cache the `Prompt` instance within high-level components like `Generator`. Use identity checks (`is`) for template and kwargs to safely invalidate the cache.

## 2025-05-15 - [Component __setattr__ Side Effects]
**Learning:** The `Component` base class in AdalFlow (similar to PyTorch) intercepts `__setattr__` to automatically register instances of `Component` in `self._components`. Storing a `Prompt` (which is a `Component`) as a private attribute triggers this registration.

**Action:** Use `super().__setattr__("_attr", value)` to store internal components that should not be part of the public component tree (e.g., for caching or private helpers).
