## 2025-05-15 - [Generator Performance Optimization]
**Learning:** Significant performance bottleneck identified in `Generator` class due to repeated `Prompt` instantiation (~22ms/call) and double-rendering of prompts in `call`/`acall`. `Prompt` instantiation involves expensive Jinja2 template parsing.
**Action:** Implemented `_get_prompt_builder` with identity-based caching for `template` and `prompt_kwargs`. Optimized `call`/`acall` to pass pre-rendered `prompt_str` to `_pre_call`. This reduced `get_prompt` latency by ~350x and `call` latency by ~90x.
