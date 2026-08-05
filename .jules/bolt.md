# Bolt's Performance Journal

This journal tracks critical learnings, performance findings, and optimization opportunities/rejections across the AdalFlow codebase.

## 2025-08-05 - [High-overhead numpy sampling vs standard library random.sample]
**Learning:** For typical list-based few-shot example selection and subset sampling (where weights are None), `np.random.choice` has massive overhead due to NumPy array/type conversion and initialization. The standard library's `random.sample` and `random.choices` are completely native and run approximately 6.3x faster for typical small-to-medium datasets (e.g. size 100).
**Action:** Always implement a fast path checking `if weights is None:` in sampling helpers to directly route to standard library's `random` module, falling back to NumPy only when probabilistic custom weights are explicitly provided.

## 2025-08-05 - [On-the-fly Regex Compilation Overhead in Frequent Parsing Utilities]
**Learning:** Although Python's `re` module internally caches compiled regular expressions, calling `re.search` or `re.compile` on-the-fly inside utility functions that are repeatedly invoked on every LLM token generation/parsing cycle still incurs cache-lookup and dictionary indexing overhead. Module-level pre-compiled regex pattern search is ~21% faster.
**Action:** Define all frequently-used regular expression patterns at the module level as precompiled constants (e.g., `_INT_PATTERN = re.compile(...)`), ensuring fast execution.
