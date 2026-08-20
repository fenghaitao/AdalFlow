# Bolt's Performance Journal - Critical Learnings

## Critical Codebase Learnings
- In `tiktoken`, `decode_tokens_bytes(token_ids)` for batch processing is significantly more efficient than calling `decode([token_id])` in a loop, as it reduces function call overhead (~33% speedup).
- When serializing objects in `adalflow.utils.serialization`, the `hasattr(obj, '__dataclass_fields__')` check is preferred for dataclass detection to avoid circular dependencies.
- `Generator` prompt instance caching in `__init__` avoids redundant template parsing and object creation (~50x speedup in `get_prompt`).
- BM25 score calculation optimized by precomputing document length normalization factors and constructing inverted index over query terms.
- PyYAML `CSafeLoader` and `CDumper` yield ~3-5x performance gains over pure-Python implementations. Custom representers (e.g., `OrderedDict`) must be registered on `CDumper` explicitly.
- In `TextSplitter` with `split_by="token"`, passing pre-calculated `estimated_num_tokens` avoids redundant tiktoken re-encoding in `Document.__post_init__`.

## 2026-03-09 - Hoisting Type Checks in Dataclass Serialization/Deserialization
**Learning:** In `dataclass_obj_from_dict` and `_asdict_inner` (`adalflow/core/functional.py`), type inspection (`check_if_class_field_args_zero_exists`, `check_if_class_field_args_one_exists`) and exclude lookup was previously being evaluated inside loops for every element/field in collections.
**Action:** Always hoist container and generic type reflection outside element iteration loops, and pre-compute sets for excluded fields per dataclass instance to achieve ~3.3x speedup on collection deserialization.
