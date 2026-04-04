
import time
import re
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from adalflow.core.functional import extract_json_str, custom_asdict

def benchmark_extract_json_str():
    text = """
Here is some text before the JSON.
```json
{
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "hobbies": ["reading", "traveling", "swimming"],
    "nested": {
        "key": "value",
        "another": 123
    }
}
```
And some text after.
"""
    iterations = 10000
    start_time = time.time()
    for _ in range(iterations):
        extract_json_str(text)
    end_time = time.time()
    print(f"extract_json_str took: {end_time - start_time:.4f} seconds for {iterations} iterations")

@dataclass
class Child:
    f1: str = "1"
    f2: str = "2"
    f3: str = "3"
    f4: str = "4"
    f5: str = "5"
    f6: str = "6"
    f7: str = "7"
    f8: str = "8"
    f9: str = "9"
    f10: str = "10"

@dataclass
class Parent:
    children: List[Child]
    p1: str = "1"
    p2: str = "2"
    p3: str = "3"
    p4: str = "4"
    p5: str = "5"

def benchmark_custom_asdict():
    children = [Child() for i in range(20)]
    parent = Parent(children=children)

    # Many excluded fields to highlight the O(N) vs O(1) lookup
    exclude = {
        "Child": [f"f{i}" for i in range(1, 11) if i % 2 == 0],
        "Parent": ["p2", "p4"]
    }

    iterations = 10000
    start_time = time.time()
    for _ in range(iterations):
        custom_asdict(parent, exclude=exclude)
    end_time = time.time()
    print(f"custom_asdict took: {end_time - start_time:.4f} seconds for {iterations} iterations")

if __name__ == "__main__":
    benchmark_extract_json_str()
    benchmark_custom_asdict()
