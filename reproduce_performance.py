import time
from adalflow.core.generator import Generator
from adalflow.core.model_client import ModelClient
from typing import Any, Dict, Optional

class MockModelClient(ModelClient):
    def call(self, api_kwargs: Dict, model_type: Any) -> str:
        return "mock response"

    def parse_chat_completion(self, completion: Any) -> Any:
        from adalflow.core.types import GeneratorOutput
        return GeneratorOutput(raw_response=completion)

    def convert_inputs_to_api_kwargs(self, input: str, model_kwargs: Dict, model_type: Any) -> Dict:
        return {"input": input, **model_kwargs}

def benchmark():
    # A larger template to make parsing more expensive
    # 500 variables
    template = "System: You are a helpful assistant.\n" + "\n".join([f"Variable {i}: {{var{i}}}" for i in range(500)]) + "\nInput: {{input_str}}"
    prompt_kwargs = {f"var{i}": f"value{i}" for i in range(500)}

    generator = Generator(
        model_client=MockModelClient(),
        model_kwargs={"model": "mock-model"},
        template=template,
        prompt_kwargs=prompt_kwargs,
        use_cache=False
    )

    # Warm up
    generator.call(prompt_kwargs={"input_str": "I love this!"})

    iterations = 100
    start_time = time.time()
    for i in range(iterations):
        generator.get_prompt(input_str=f"Input {i}")
    end_time = time.time()
    print(f"Average get_prompt latency (very large template): {(end_time - start_time) / iterations * 1000:.4f} ms")

    start_time = time.time()
    for i in range(iterations):
        generator.call(prompt_kwargs={"input_str": f"Input {i}"})
    end_time = time.time()
    print(f"Average call latency (very large template): {(end_time - start_time) / iterations * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
