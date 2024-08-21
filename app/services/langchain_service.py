from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from app.config import settings
from app.services.supabase_service import supabase_service


class LangchainService:
    def __init__(self):
        self.llm = OpenAI(temperature=0.7, openai_api_key=settings.openai_api_key)
        self.conversations = {}

    async def get_or_create_conversation(self, agent_id: int):
        if agent_id not in self.conversations:
            agent = await supabase_service.get_agent(agent_id)
            if not agent:
                raise ValueError(f"Agent with id {agent_id} not found")

            prompt_template = self._create_prompt_template(agent)
            memory = ConversationBufferMemory()
            self.conversations[agent_id] = ConversationChain(
                llm=self.llm,
                memory=memory,
                prompt=prompt_template,
                verbose=True
            )

        return self.conversations[agent_id]

    def _create_prompt_template(self, agent):
        prompt = f"You are {agent.name}, an AI assistant with the following description: {agent.description}\n\n"

        if agent.knowledge_bases:
            prompt += "You have access to the following knowledge bases:\n"
            for kb in agent.knowledge_bases:
                prompt += f"- {kb.name}: {kb.description}\n"

        if agent.tools:
            prompt += "\nYou have access to the following tools:\n"
            for tool in agent.tools:
                prompt += f"- {tool.name}: {tool.description}\n"

        prompt += "\n{history}\nHuman: {input}\nAI: "

        return PromptTemplate(
            input_variables=["history", "input"],
            template=prompt
        )

    async def chat(self, agent_id: int, message: str):
        conversation = await self.get_or_create_conversation(agent_id)
        response = conversation.predict(input=message)
        return response


langchain_service = LangchainService()