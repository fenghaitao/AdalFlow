## 2025-05-22 - [Optimized Prompt Rendering and Generator Overhead]
**Learning:** Jinja2 template parsing is expensive (up to ~20ms for large templates). O(N^2) complexity in recursive prompt rendering significantly impacts performance with large keyword arguments.
**Action:** Cache the `Prompt` instance in `Generator` and implement lazy initialization. Pre-filter keyword arguments once in `_convert_prompt_kwargs_to_str` and use a fast-path for non-nested templates.
