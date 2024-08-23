import os
from langchain_core.messages import SystemMessage
from langchain_core.prompt_values import ChatPromptValue
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from app.config import settings

load_dotenv()


class OpenAI:
    def __init__(self, model_name, temperature=0.7, max_tokens_to_sample=1024, timeout=None, max_retries=3, top_p=1.0,
                 top_k=50, streaming=False, stream_usage=False):
        self.model = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens_to_sample,
            timeout=timeout,
            max_retries=max_retries,
            streaming=streaming,
            openai_api_key=settings.openai_api_key or os.getenv("OPENAI_API_KEY")
        )

    def bind_tools(self, tools):
        self.tools = tools

    def systemPrompt(self, prompt):
        messages = [
            SystemMessage(content=prompt)
        ]
        chat_prompt_value = ChatPromptValue(messages=messages)
        return self.model.invoke(chat_prompt_value)


openai = OpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    max_tokens_to_sample=1024,
    timeout=None,
    max_retries=2,
    top_p=1.0,
    top_k=0,
    streaming=True,
    stream_usage=False
)
