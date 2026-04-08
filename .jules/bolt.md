# Bolt's Performance Journal

## 2025-05-22 - [Optimized Generator Prompt Builder Caching and Double Rendering]
**Learning:** Significant performance bottlenecks were found in the `Generator` class due to redundant Jinja2 template parsing in `Prompt` instantiation and double-rendering of prompts in `call`/`acall`.
**Action:** Implemented `_get_prompt_builder` in `Generator` to lazily cache a single `Prompt` instance. Modified `_pre_call` to accept an optional `prompt_str`, allowing `call` and `acall` to reuse the pre-rendered string. This resulted in a ~550x speedup for `get_prompt` latency (~22ms to ~0.04ms) for large templates.
