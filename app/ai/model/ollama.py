from langchain_ollama import ChatOllama


class OllamaModel:
    def __init__(self, model, temperature):
        self.model = ChatOllama(
            model=model,
            temperature=temperature,
        )


ollama = OllamaModel(
    model="llama3",
    temperature=0.7
)