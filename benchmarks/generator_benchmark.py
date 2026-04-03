import time
import jinja2
from adalflow.core.generator import Generator
from adalflow.core.model_client import ModelClient
from adalflow.core.prompt_builder import Prompt

class MockModelClient(ModelClient):
    def call(self, api_kwargs, model_type):
        return "mock response"
    def parse_chat_completion(self, completion):
        from adalflow.core.types import GeneratorOutput
        return GeneratorOutput(raw_response=completion)
    def convert_inputs_to_api_kwargs(self, input, model_kwargs, model_type):
        return {"input": input, **model_kwargs}

def benchmark_generator_call():
    # Large template to emphasize rendering cost
    template = "Large Template: " + " ".join([f"{{{{ var_{i} }}}}" for i in range(500)])
    prompt_kwargs = {f"var_{i}": f"value_{i}" for i in range(500)}

    generator = Generator(
        model_client=MockModelClient(),
        template=template,
        prompt_kwargs=prompt_kwargs
    )

    # Warm up
    generator.call()

    start_time = time.time()
    iterations = 1000
    for _ in range(iterations):
        generator.call()
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average Generator.call latency: {avg_time:.6f} seconds")

def benchmark_generator_get_prompt():
    template = "Large Template: " + " ".join([f"{{{{ var_{i} }}}}" for i in range(500)])
    prompt_kwargs = {f"var_{i}": f"value_{i}" for i in range(500)}

    generator = Generator(
        model_client=MockModelClient(),
        template=template,
        prompt_kwargs=prompt_kwargs
    )

    # Warm up
    generator.get_prompt()

    start_time = time.time()
    iterations = 1000
    for _ in range(iterations):
        generator.get_prompt()
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average Generator.get_prompt latency: {avg_time:.6f} seconds")

if __name__ == "__main__":
    benchmark_generator_get_prompt()
    benchmark_generator_call()
