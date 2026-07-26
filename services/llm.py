from ollama import Client
from pprint import pprint

from config import settings
from tools.registry import execute, get_llm_tools
import tools


class LLMService:
    def __init__(self):
        self.client = Client(
            host=settings.ollama_url,
        )

        self.model = settings.ollama_model

    def _chat(self, messages):
        """
        Send a conversation to Ollama.
        """

        print("\n=== Tools ===")
        pprint(get_llm_tools())

        print("\n=== Messages ===")
        pprint(messages)

        response = self.client.chat(
            model=self.model,
            messages=messages,
            tools=get_llm_tools(),
            think=False,
        )

        print("\n=== Response ===")
        pprint(response)

        return self.client.chat(
            model=self.model,
            messages=messages,
            tools=get_llm_tools(),
        )

    def _execute_tool_calls(self, tool_calls):
        """
        Execute one or more tool calls.
        """

        results = []

        for tool_call in tool_calls:

            name = tool_call.function.name
            arguments = tool_call.function.arguments

            result = execute(
                name,
                **arguments,
            )

            results.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "content": result,
                }
            )

        return results

    def chat(self, messages):
        """
        Chat until the model has no more tool calls.
        """

        while True:

            response = self._chat(messages)

            message = response.message

            messages.append(message)

            if not message.tool_calls:
                return message.content

            messages.extend(
                self._execute_tool_calls(
                    message.tool_calls
                )
            )