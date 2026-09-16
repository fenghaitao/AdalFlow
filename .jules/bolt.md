## 2025-05-18 - Pre-filter kwargs during Jinja2 prompt rendering
**Learning:** In `Prompt._convert_prompt_kwargs_to_str`, calling `_deep_render` inside a loop over `prompt_kwargs` caused `_deep_render` to construct and filter a new dictionary on every key, resulting in $O(N^2)$ execution overhead when rendering prompts with many keyword arguments.
**Action:** Pre-filter `Prompt` and `Template` instances from the keyword arguments dictionary once before looping over items, and pass the pre-filtered context directly into `_deep_render`.
