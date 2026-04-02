
import time
import logging
from adalflow.core.generator import Generator
from adalflow.core.model_client import ModelClient
from adalflow.core.types import GeneratorOutput

class MockClient(ModelClient):
    def call(self, api_kwargs, model_type):
        return "ok"
    def parse_chat_completion(self, completion):
        return GeneratorOutput(raw_response=completion, data=completion)
    def convert_inputs_to_api_kwargs(self, input, model_kwargs, model_type):
        return {"prompt": input}

def benchmark():
    # A larger template to make parsing/rendering overhead more significant
    large_template = "This is a large template. " * 500 + "Variable: {{var}}"
    prompt_kwargs = {"var": "value"}

    generator = Generator(
        model_client=MockClient(),
        model_kwargs={"model": "test-model"},
        template=large_template,
        prompt_kwargs=prompt_kwargs
    )

    print("Benchmarking get_prompt (template parsing + rendering)...")
    start_time = time.time()
    iters = 1000
    for _ in range(iters):
        generator.get_prompt()
    end_time = time.time()
    print(f"Average get_prompt latency: {(end_time - start_time) / iters:.6f}s")

    print("\nBenchmarking call (includes get_prompt twice + other overhead)...")
    generator.mock_output = True
    start_time = time.time()
    for _ in range(iters):
        generator.call()
    end_time = time.time()
    print(f"Average call latency: {(end_time - start_time) / iters:.6f}s")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    benchmark()
