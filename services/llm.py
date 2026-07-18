from openai import OpenAI

class LLM:

    def __init__(self):
        self.client = OpenAI()

    def ask(self, prompt: str) -> str:

        response = self.client.responses.create(
            model="gpt-5.5",
            input=prompt,
            tools=[
                tool.definition
                for tool in TOOLS.values()
            ]
        )

        return response.output_text