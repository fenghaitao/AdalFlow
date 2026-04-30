## 2025-05-15 - [O(N²) Complexity in Prompt Rendering]
**Learning:** `Prompt._convert_prompt_kwargs_to_str` was performing an O(N) filter operation inside an O(N) loop over the same dictionary, resulting in O(N²) complexity for prompt rendering.
**Action:** Pre-filter dictionary arguments once and implement a fast-path skip for the common case where no nested templates are present.

## 2025-05-15 - [Generator Overhead from Redundant Prompt Parsing]
**Learning:** `Generator` was instantiating a new `Prompt` object on every call, adding ~1ms of overhead from Jinja2 template parsing.
**Action:** Cache the `Prompt` builder instance within `Generator` and implement attribute-based cache invalidation.
