import time
import json
from adalflow.core.functional import extract_json_str

def benchmark():
    content = "a" * 10000
    large_json_str = '{"data": "' + content + '", "more": "data"}'
    text = "Some prefix " + large_json_str + " some suffix"

    n = 1000
    start = time.time()
    for _ in range(n):
        extract_json_str(text)
    end = time.time()
    print(f"Large string extraction took: {end - start:.4f}s for {n} iterations")

if __name__ == "__main__":
    benchmark()
