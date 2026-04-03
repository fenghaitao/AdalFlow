
import time
from adalflow.core.prompt_builder import Prompt

def bench_convert_kwargs():
    print("Benchmarking _convert_prompt_kwargs_to_str...")
    num_kwargs = 5000
    prompt_kwargs = {f"key_{i}": f"value_{i}" for i in range(num_kwargs)}
    prompt = Prompt(template="test")

    start_time = time.time()
    for _ in range(100):
        prompt._convert_prompt_kwargs_to_str(prompt_kwargs)
    end_time = time.time()

    print(f"Time for 100 calls with {num_kwargs} kwargs: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    bench_convert_kwargs()
