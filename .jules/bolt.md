# Bolt's Performance Journal

## 2025-05-22 - [Optimization of Prompt Rendering and Generator Caching]

**Learning:**
1. `Component` class in AdalFlow has custom `__setattr__` and `__getattr__` that manage `_parameters` and `_components`. Directly setting attributes like `self._prompt_builder = ...` can trigger unwanted registration or failures if the attribute isn't expected by the base class. Using `object.__setattr__(self, name, value)` is safer for internal performance caches.
2. `Prompt._convert_prompt_kwargs_to_str` had an O(N^2) complexity bottleneck because it was filtering the entire keyword argument dictionary inside a loop over the same dictionary keys. For large prompts (e.g., 2000 keys), this resulted in ~1.1s overhead just for string conversion.
3. `Generator` was re-instantiating `Prompt` (and thus re-parsing Jinja2 templates) on every call to `get_prompt`, `print_prompt`, etc.

**Action:**
1. Use `object.__setattr__` for private internal caches in `Component` subclasses to avoid framework overhead and potential `AttributeError` during initialization.
2. Always pre-filter shared context dictionaries *once* before entering loops that perform recursive rendering or deep processing.
3. Implement lazy caching for objects that require expensive parsing (like Jinja2 templates) if they are used multiple times in the component lifecycle.
