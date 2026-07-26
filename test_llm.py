from services.llm import LLM

llm = LLM()

print("Sending prompt...")

response = llm.ask(
    "Reply with exactly: Hello James! Ollama is working."
)

print("\nResponse:\n")
print(response)