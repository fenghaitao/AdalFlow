# Bolt's Performance Journal

## 2024-05-22 - [Regex Pre-compilation]
**Learning:** Pre-compiling regex patterns as module-level constants in `functional.py` significantly reduces overhead during frequent LLM output parsing. Benchmarking showed ~33-53% improvement in `extract_json_str`.
**Action:** Always pre-compile regex if they are used in hot paths.

## 2024-05-22 - [Batch Token Decoding]
**Learning:** Using `tiktoken.decode_tokens_bytes` for batch processing instead of a loop calling `decode` for individual token IDs reduced processing time by ~33%.
**Action:** Use batch APIs provided by libraries whenever possible.

## 2024-05-22 - [Prompt Context Filtering]
**Learning:** Pre-filtering the context dictionary once in `Prompt._convert_prompt_kwargs_to_str` instead of filtering inside a recursive loop avoided an O(N^2) bottleneck, giving a ~500x speedup for large contexts.
**Action:** Be mindful of redundant work inside recursive functions or loops.

## 2024-05-22 - [Custom Recursive Serialization]
**Learning:** A direct recursive conversion for `to_dict` is 5x-20x faster than `json.loads(json.dumps(obj))`.
**Action:** Avoid JSON round-trips for internal object-to-dict conversions.

## 2024-05-22 - [Cache Lookup Optimization]
**Learning:** Replacing a membership test followed by a retrieval (`if x in cache: cache.get(x)`) with a single `cache.get()` call reduces redundant lookup overhead.
**Action:** Use `get()` with default values or check for `None` to avoid double lookups.

## 2024-05-22 - [Generator Prompt Caching]
**Learning:** Caching the `Prompt` instance in `Generator.__init__` avoids redundant object instantiation and Jinja2 template parsing in `get_prompt`.
**Action:** Cache expensive-to-initialize objects that don't change often.
