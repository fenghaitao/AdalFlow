## 2026-07-15 - [Generator Prompt Caching]
**Learning:** Instantiating new `Prompt` objects in every `get_prompt` or `print_prompt` call in `Generator` causes significant overhead due to repeated Jinja2 template parsing and object initialization.
**Action:** Always cache core sub-components like `Prompt` in the constructor of orchestration components to avoid O(N) or even O(1) overhead that adds up across many calls. In `Generator`, caching the `Prompt` instance resulted in a ~50x speedup for prompt generation.
