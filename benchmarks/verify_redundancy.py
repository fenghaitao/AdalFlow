
import unittest.mock as mock
from adalflow.core.generator import Generator
from adalflow.core.model_client import ModelClient

class MockClient(ModelClient):
    def init_sync_client(self): return None
    def init_async_client(self): return None
    def call(self, **kwargs): return "mock response"
    async def acall(self, **kwargs): return "mock response"
    def parse_chat_completion(self, completion):
        from adalflow.core.types import GeneratorOutput
        return GeneratorOutput(raw_response=completion, data=completion)
    def convert_inputs_to_api_kwargs(self, **kwargs): return {}

def test_redundant_calls():
    client = MockClient()
    generator = Generator(
        model_client=client,
        model_kwargs={"model": "gpt-3.5-turbo"},
        template="Hello {{ name }}!",
        prompt_kwargs={"name": "Bolt"}
    )

    with mock.patch.object(Generator, 'get_prompt', wraps=generator.get_prompt) as mocked_get_prompt:
        generator.call()
        print(f"get_prompt called {mocked_get_prompt.call_count} times in call()")

    with mock.patch.object(Generator, 'get_prompt', wraps=generator.get_prompt) as mocked_get_prompt:
        import asyncio
        asyncio.run(generator.acall())
        print(f"get_prompt called {mocked_get_prompt.call_count} times in acall()")

if __name__ == "__main__":
    test_redundant_calls()
