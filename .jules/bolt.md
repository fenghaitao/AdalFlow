## 2025-05-14 - [Prompt Rendering O(N^2) Complexity]
**Learning:** `Prompt._convert_prompt_kwargs_to_str` had an O(N^2) complexity bottleneck because it was filtering the entire context dictionary (to remove Prompt/Template objects) for *every* keyword argument during the rendering pass.
**Action:** Pre-filter the context dictionary once before the loop and pass it as an optional argument to `_deep_render` to achieve O(N) complexity.

## 2025-05-14 - [Generator Prompt Caching]
**Learning:** Creating a new `Prompt` instance on every `Generator.get_prompt()` call is expensive due to Jinja2 template parsing. Caching it in `__init__` gives a ~30-40x speedup for local processing.
**Action:** Cache the `Prompt` instance as `self.prompt` in `Generator.__init__`. Note that if `self.template` is changed after init, the cached prompt won't update unless handled (standard AdalFlow usage typically keeps it static).
