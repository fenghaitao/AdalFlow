# Bolt Performance Journal

## 2026-08-08 - [Optimized random_sample & Tokenizer.get_string_tokens]
**Learning:**
1. Using `np.random.choice` for small or unweighted sampling lists has high initialization and array conversion overhead. Implementing simple Python standard library fast paths with `random.sample` and `random.choices` yields a massive 5x to 15x execution speedup.
2. In `tiktoken`, looping through token IDs and calling `.decode([token_id])` for each token individually incurs significant Python interpreter overhead. Using `decode_single_token_bytes` or `decode_tokens_bytes` with utf-8 decoding (using `errors='replace'` to handle any split-byte unicode boundaries) provides a 50% speedup.

**Action:**
1. Always check for sampling tasks and prefer Python's built-in `random` module for simple or unweighted operations, using NumPy only when complex multidimensional or specialized weighted without replacement sampling is required.
2. For tokenizers/decoders, look for batch decoding APIs (`decode_single_token_bytes`/`decode_tokens_bytes`) instead of looping through token IDs one by one.
