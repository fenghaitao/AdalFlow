import time
from adalflow.core.prompt_builder import Prompt
from jinja2 import Environment

def benchmark():
    # Long template with very few variables
    template_str = "System: You are a helpful assistant.\n" + "Literal text " * 10000 + "\nInput: {{input_str}}"
    prompt_kwargs = {"input_str": "test"}

    iterations = 100

    start_time = time.time()
    for i in range(iterations):
        prompt = Prompt(template=template_str, prompt_kwargs=prompt_kwargs)
        prompt.call()
    end_time = time.time()
    print(f"Average Prompt creation + call latency: {(end_time - start_time) / iterations * 1000:.4f} ms")

    prompt = Prompt(template=template_str, prompt_kwargs=prompt_kwargs)
    start_time = time.time()
    for i in range(iterations):
        prompt.call()
    end_time = time.time()
    print(f"Average Prompt call latency (reusing instance): {(end_time - start_time) / iterations * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
