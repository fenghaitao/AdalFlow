from adalflow.core.generator import Generator
from adalflow.core.model_client import ModelClient

class MockModelClient(ModelClient):
    def call(self, api_kwargs, model_type):
        return "mock response"
    def parse_chat_completion(self, completion):
        from adalflow.core.types import GeneratorOutput
        return GeneratorOutput(raw_response=completion)
    def convert_inputs_to_api_kwargs(self, input, model_kwargs, model_type):
        return {"input": input}

model_client = MockModelClient()
template1 = "Hello {{name}}!"
template2 = "Hi {{name}}!"

gen = Generator(model_client=model_client, template=template1)
builder1 = gen._get_prompt_builder()
print(f"Builder 1 template: {builder1.template}")

# Test identity reuse
builder1_again = gen._get_prompt_builder()
print(f"Builders are identical: {builder1 is builder1_again}")
assert builder1 is builder1_again

# Test template change invalidation
gen.template = template2
builder2 = gen._get_prompt_builder()
print(f"Builder 2 template: {builder2.template}")
print(f"Builders are different after template change: {builder1 is not builder2}")
assert builder1 is not builder2
assert builder2.template == template2

# Test prompt_kwargs change invalidation
gen.prompt_kwargs = {"new": "kwargs"}
builder3 = gen._get_prompt_builder()
print(f"Builders are different after prompt_kwargs change: {builder2 is not builder3}")
assert builder2 is not builder3

print("Cache invalidation tests passed!")
