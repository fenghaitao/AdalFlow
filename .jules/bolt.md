## 2025-05-15 - [O(N²) Complexity in Prompt Rendering]
**Learning:** `Prompt._convert_prompt_kwargs_to_str` had O(N²) complexity because it created a new filtered context dictionary for every keyword argument during the recursive `_deep_render` phase. For 1000+ keyword arguments, this resulted in significant latency (~280ms+).
**Action:** Implement an O(N) fast-path that skips recursive rendering if no templates are present, and pre-filter the context dictionary once before the rendering loop to avoid redundant allocations and iterations.

## 2025-05-15 - [Correct and Efficient JSON Extraction]
**Learning:** Manual character-by-character brace/bracket counting for JSON extraction is slow and logically incorrect as it fails when braces appear inside string literals.
**Action:** Use `json.JSONDecoder().raw_decode` for robust and efficient extraction of nested JSON structures from larger text blocks. It correctly handles string escapes and nested braces/brackets.

## 2025-05-15 - [Dataclass Introspection Caching]
**Learning:** `dataclasses.fields()` is relatively expensive when called frequently in hot paths like `asdict` or schema generation, especially for deeply nested structures.
**Action:** Use `weakref.WeakKeyDictionary` to cache field lookups at the module level. This avoids memory leaks for dynamic classes while providing a measurable speedup for serialization and introspection.
