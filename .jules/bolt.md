## 2025-05-15 - [Optimization] Prompt Rendering and Generator Caching

**Learning:**
1. `Prompt._convert_prompt_kwargs_to_str` had O(N²) complexity because it performed dictionary filtering for *every* keyword argument to prevent circular references in nested templates, even when no nested templates were present. Moving filtering outside the loop and adding a fast-path `has_nested` check reduced latency for 1000 keyword arguments from ~500ms to ~1ms.
2. `Generator` was instantiating a new `Prompt` object and re-rendering the entire template up to 3 times per `call()`. Caching the `Prompt` instance and passing the rendered `prompt_str` down the call stack eliminated this redundancy.
3. In `Component`-based classes (like `Generator`), internal helper objects should be stored using `object.__setattr__(self, name, value)` to prevent them from being automatically registered in `self._components`, which avoids them appearing in serialized output or `__repr__`.

**Action:**
- Always check for O(N²) patterns when processing large dictionaries in core utility functions.
- Use lazy-loading and caching for expensive objects like Jinja2-based `Prompt` builders.
- Use `object.__setattr__` for private internal state in `adalflow.Component` subclasses to bypass the custom `__setattr__` logic.
