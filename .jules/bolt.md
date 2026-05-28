# Bolt Performance Journal

## 2025-05-23 - Generator Prompt Builder Caching
**Learning:** Instantiating `Prompt` objects (which involves Jinja2 template parsing) is expensive (~1ms per call). Since `Generator` often uses the same template and preset prompt kwargs, caching the `Prompt` instance provides a significant speedup. Additionally, `Generator.call` and `acall` were redundantly rendering the prompt twice—once for tracing/mocking and once for the actual model call.
**Action:** Implement lazy caching for the `Prompt` builder in `Generator` and ensure it's invalidated on template/prompt_kwargs updates. Optimized `call` and `acall` to render once and pass the result down to `_pre_call`.

## 2025-05-23 - N² Complexity in Prompt Kwargs Conversion
**Learning:** The previous implementation of `_convert_prompt_kwargs_to_str` in `Prompt` class had O(N²) complexity relative to the number of keyword arguments because it filtered the entire context dictionary during each recursive call in `_deep_render`.
**Action:** Pre-filter the context once and pass it to `_deep_render`, reducing the complexity to O(N).
