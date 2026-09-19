## 2025-05-18 - Avoid Over-Filtering Prompt Keyword Context in `_deep_render`

**Learning:** `Prompt._deep_render` is called for every prompt keyword parameter when rendering prompts in AdalFlow. Filtering dictionary keys for `Prompt` or `Template` instances inside `_deep_render` introduces $O(N^2)$ dictionary creation overhead when rendering prompts with many keyword arguments. Short-circuiting early with `if not isinstance(value, (Prompt, Template)): return value` avoids creating non-essential dictionaries and speeds up prompt rendering by over 15x–20x without altering string template evaluation or nested Prompt resolution.

**Action:** When working on recursive rendering tools like `_deep_render`, always check whether the value requires transformation before constructing context dictionaries or copying structures.
