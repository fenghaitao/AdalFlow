import time
import json
import re
from adalflow.core.functional import extract_json_str, extract_list_str

def benchmark():
    # Correctness test
    test_json = 'Some text before {"a": "}"} some text after'
    try:
        extracted = extract_json_str(test_json)
        print(f"Original extraction result: {extracted}")
        json.loads(extracted)
        print("Original extraction is valid JSON")
    except Exception as e:
        print(f"Original extraction failed: {e}")

    # Performance test
    n = 1000
    large_text = 'Pre' + ' ' * 100 + '{"key": "' + 'val' * 100 + '", "list": [' + '1,' * 100 + '2]}' + ' ' * 100 + 'Post'

    start = time.time()
    for _ in range(n):
        extract_json_str(large_text)
    end = time.time()
    print(f"Original extract_json_str took: {end - start:.4f}s for {n} iterations")

if __name__ == "__main__":
    benchmark()
