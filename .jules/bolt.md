## 2026-06-28 - [Optimized prompt rendering complexity from O(N^2) to O(N)]
**Learning:** Found an O(N^2) complexity bottleneck in `Prompt._convert_prompt_kwargs_to_str` where redundant context filtering was performed in a loop. For prompts with many (e.g. 2000) keyword arguments, this caused rendering to take >1 second.
**Action:** Pre-filter keyword arguments once and pass the result to recursive rendering calls to maintain linear time complexity.

## 2026-06-28 - [Cached Prompt instance in Generator to reduce overhead]
**Learning:** `Generator.get_prompt` and `print_prompt` were instantiating a new `Prompt` and parsing the Jinja2 template on every call, adding ~1.4ms of overhead per call.
**Action:** Cache the `Prompt` instance in `Generator.__init__` to avoid redundant object creation and parsing.

## 2026-06-28 - [Pre-compiled high-frequency regex patterns]
**Learning:** String utility functions in `functional.py` were re-compiling complex regex patterns on every call, especially impactful for JSON extraction from LLM responses.
**Action:** Use module-level constants for pre-compiled regex patterns to improve performance by ~27%.
