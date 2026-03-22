## 2025-05-22 - [Generator Prompt Caching]
**Learning:** Significant performance bottleneck discovered in 'Prompt' object instantiation (~9ms) due to redundant Jinja2 template parsing in every 'Generator' call. Caching the 'Prompt' instance within 'Generator' and invalidating it based on template/kwargs identity reduces 'get_prompt' overhead by ~140x (from ~10ms to ~0.07ms).
**Action:** Always cache 'Prompt' instances in orchestration components if the template is static or changes infrequently. Use identity checks ('is') for efficient cache invalidation of large prompt configurations.

## 2025-05-22 - [Redundant Rendering in Generator]
**Learning:** 'Generator.call' and 'acall' rendered the prompt twice (once for span tracing/logging and once in '_pre_call').
**Action:** Pass the already rendered 'prompt_str' to downstream methods like '_pre_call' to avoid redundant O(N) rendering operations.
