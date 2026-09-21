## 2026-03-31 - Prompt kwargs rendering O(N^2) dict filtering
**Learning:** In `Prompt._convert_prompt_kwargs_to_str` and `Prompt._deep_render`, invoking `_deep_render` on every prompt argument caused $O(N^2)$ dictionary filtering copies because `_deep_render` filtered the context dictionary for every argument before checking if the argument was even a `Prompt` or `Template`.
**Action:** Always check `isinstance(value, (Prompt, Template))` before doing dictionary filtering in recursive render methods, and pre-filter rendering context lazily once when nested components are detected.
