## 2025-05-14 - Caching core components in orchestrators
**Learning:** Instantiating helper components like `Prompt` on every method call in a core class like `Generator` introduces significant overhead (up to 1.4ms per call). Caching them as instance attributes reduces this to ~0.03ms.
**Action:** Always check if helper components in orchestrator classes (`Generator`, `Retriever`, etc.) are being recreated unnecessarily.
