import time
from dataclasses import dataclass
from typing import List
from adalflow.core.functional import get_dataclass_schema, custom_asdict

@dataclass
class Item:
    name: str
    value: int

@dataclass
class Container:
    items: List[Item]

def benchmark_functional():
    item = Item("a", 1)
    container = Container([item] * 10)
    n = 10000

    start = time.time()
    for _ in range(n):
        get_dataclass_schema(Container)
    end = time.time()
    print(f"get_dataclass_schema(Container) took: {end - start:.4f}s for {n} iterations")

    start = time.time()
    for _ in range(n):
        custom_asdict(container)
    end = time.time()
    print(f"custom_asdict(container) took: {end - start:.4f}s for {n} iterations")

if __name__ == "__main__":
    benchmark_functional()
