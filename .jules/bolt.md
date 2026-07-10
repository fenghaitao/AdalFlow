## 2025-05-22 - [Optimizing Prompt rendering complexity]
**Learning:** In `Prompt._convert_prompt_kwargs_to_str`, `_deep_render` was being called for each keyword argument, and each call was performing an O(N) filtering of the context dictionary. This resulted in O(N^2) complexity for prompt preparation.
**Action:** Pre-filter the context once and pass it to `_deep_render` to achieve O(N) linear complexity.

## 2025-05-22 - [Caching Prompt instances in Generator]
**Learning:** `Generator.get_prompt` was re-instantiating `Prompt` on every call, causing redundant Jinja2 template parsing.
**Action:** Cache the `Prompt` instance in `Generator.__init__`. Note that this makes the generator less reactive to direct changes in `template` or `prompt_kwargs` attributes after initialization, but provides ~50x speedup for the common use case.
