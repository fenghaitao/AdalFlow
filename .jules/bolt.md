## 2025-05-22 - [Generator Prompt Rendering Optimization]
**Learning:** Prompt object instantiation (~12ms) is significantly more expensive than rendering (~0.03ms) due to Jinja2 template parsing. Additionally, the Generator class was performing redundant renderings (up to 3 times in forward pass).
**Action:** Always cache the Prompt builder instance within orchestration components. Pass pre-rendered strings to internal methods to avoid redundant Jinja2 calls.
