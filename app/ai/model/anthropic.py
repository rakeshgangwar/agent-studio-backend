import getpass
import os
from langchain_anthropic import Anthropic, ChatAnthropic
from app.config import settings


class AnthropicModel:
    def __init__(self, model_name, temperature, max_tokens_to_sample, timeout, max_retries, top_p, top_k, streaming,
                 stream_usage):
        self.model = ChatAnthropic(
            model_name=model_name,
            # anthropic_api_key=settings.anthropic_api_key,
            api_key=settings.anthropic_api_key,
            temperature=temperature,
            max_tokens_to_sample=max_tokens_to_sample,
            timeout=timeout,
            max_retries=max_retries,
            top_p=top_p,
            top_k=top_k,
            streaming=streaming
        )

    def systemPrompt(self, prompt):
        messages = [
            {
                "role": "system",
                "content": prompt,
            }
        ]
        return self.model.invoke(messages)

    # def assign_tools(self, tools):
    #     self.model.bind_tools(tools)


anthropic = AnthropicModel(
    model_name="claude-2.1",
    temperature=0,
    max_tokens_to_sample=1024,
    timeout=None,
    max_retries=2,
    top_p=1.0,
    top_k=0,
    streaming=True,
    stream_usage=False
)

# anthropic.systemPrompt(prompt="You are a rockstar")
# print(anthropic.model.invoke("Who are you?").content)
