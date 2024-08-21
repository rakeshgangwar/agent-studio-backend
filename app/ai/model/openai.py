import getpass
import os

from langchain_core.messages import SystemMessage
from langchain_core.prompt_values import ChatPromptValue
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


class OpenAI:
    def __init__(self, model_name, temperature, max_tokens_to_sample, timeout, max_retries, top_p, top_k, streaming,
                 stream_usage):
        self.model = ChatOpenAI(
            temperature=temperature,
            timeout=timeout,
            max_retries=max_retries,
            streaming=streaming,
        )

    def systemPrompt(self, prompt):
        messages = [
            SystemMessage(content=prompt)
        ]
        chat_prompt_value = ChatPromptValue(messages=messages)
        return self.model.invoke(chat_prompt_value)

    # def assign_tools(self, tools):
    #     self.model.bind_tools(tools)


openai = OpenAI(
    model_name="claude-3-5-sonnet-20240620",
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
# print(anthropic.model.invoke("Who are you?"))
