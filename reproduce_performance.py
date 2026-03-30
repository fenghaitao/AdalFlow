import time
import logging
from adalflow.core.generator import Generator
from adalflow.core.model_client import ModelClient
from adalflow.core.types import GeneratorOutput
from adalflow.core.default_prompt_template import DEFAULT_ADALFLOW_SYSTEM_PROMPT

# Mock ModelClient to avoid actual API calls
class MockModelClient(ModelClient):
    def call(self, api_kwargs, model_type):
        return "Mock response"
    def parse_chat_completion(self, completion):
        return GeneratorOutput(raw_response=completion)
    def convert_inputs_to_api_kwargs(self, input, model_kwargs, model_type):
        return {"input": input, **model_kwargs}

def benchmark_generator_large_template():
    client = MockModelClient()
    template = DEFAULT_ADALFLOW_SYSTEM_PROMPT
    prompt_kwargs = {"task_desc_str": "You are a helpful assistant."}

    gen = Generator(model_client=client, template=template, prompt_kwargs=prompt_kwargs)

    # Warm up
    gen.call(prompt_kwargs={"input_str": "Hello"})

    start_time = time.time()
    iterations = 100
    for i in range(iterations):
        gen.call(prompt_kwargs={"input_str": f"Hello {i}"})
    end_time = time.time()

    avg_latency = (end_time - start_time) / iterations
    print(f"Average Generator.call latency (large template): {avg_latency*1000:.4f} ms")

def benchmark_get_prompt_large_template():
    client = MockModelClient()
    template = DEFAULT_ADALFLOW_SYSTEM_PROMPT
    prompt_kwargs = {"task_desc_str": "You are a helpful assistant."}

    gen = Generator(model_client=client, template=template, prompt_kwargs=prompt_kwargs)

    start_time = time.time()
    iterations = 100
    for i in range(iterations):
        gen.get_prompt(input_str=f"Hello {i}")
    end_time = time.time()

    avg_latency = (end_time - start_time) / iterations
    print(f"Average Generator.get_prompt latency (large template): {avg_latency*1000:.4f} ms")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    benchmark_generator_large_template()
    benchmark_get_prompt_large_template()
