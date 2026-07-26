from services.llm import LLMService

llm = LLMService()

messages = [
    {
        "role": "user",
        "content": "What tasks do I have?"
    }
]

print(llm.chat(messages))