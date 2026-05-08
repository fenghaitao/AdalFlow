## 2025-05-14 - Optimized Generator prompt rendering and caching

**Learning:** Prompt instantiation in AdalFlow is relatively expensive (~1ms) because it involves Jinja2 template parsing and variable extraction. The Generator class was creating new Prompt instances on every prompt retrieval or representation call. Additionally, the call cycle was rendering the template twice (once for spans/logging and once in _pre_call).

**Action:** Implement lazy caching for the Prompt instance within Generator using a property. Use `object.__setattr__` to store the cached instance to avoid it being registered as a sub-component in the GradComponent tree, which would cause issues with parameter management. Update the call cycle to pass the rendered prompt string to `_pre_call` to avoid redundant rendering.
