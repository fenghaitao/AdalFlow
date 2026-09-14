import unittest
from jinja2 import Template
from adalflow.core.prompt_builder import Prompt
from adalflow.optim.parameter import Parameter


class TestPrompt(unittest.TestCase):
    def test_basic_prompt_render(self):
        prompt = Prompt(template="Hello {{ name }}!")
        res = prompt.call(name="World")
        self.assertEqual(res, "Hello World!")

    def test_nested_prompt_render(self):
        inner_prompt = Prompt(template="{% for x in items %}{{ x }} {% endfor %}")
        outer_prompt = Prompt(template="List: {{ inner }}")
        res = outer_prompt.call(inner=inner_prompt, items=["a", "b", "c"])
        self.assertEqual(res.strip(), "List: a b c")

    def test_nested_jinja_template_render(self):
        env_tpl = Template("{{ word|upper }}")
        prompt = Prompt(template="Output: {{ sub }}")
        res = prompt.call(sub=env_tpl, word="hello")
        self.assertEqual(res, "Output: HELLO")

    def test_parameter_in_prompt_kwargs(self):
        param = Parameter(data="test_value")
        prompt = Prompt(template="Param: {{ p }}")
        res = prompt.call(p=param)
        self.assertEqual(res, "Param: test_value")


if __name__ == "__main__":
    unittest.main()
