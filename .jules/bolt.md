## 2025-05-14 - Redundant Prompt Instantiation in Generator
**Learning:** Instantiating the `Prompt` class is expensive (~22ms for large templates) because it parses the Jinja2 template. The `Generator` was originally re-instantiating `Prompt` on every call and rendering it twice (once for logging, once for the API), doubling the overhead.
**Action:** Cache the `Prompt` builder within `Generator` and pass the pre-rendered string to internal methods (`_pre_call`) to eliminate redundant work. Ensure `mock_output` also sets `output.input` to prevent downstream failures in training passes.
