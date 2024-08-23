from app.services.agent_service import agent_service
from app.services.supabase_service import SupabaseService
from app.services.model_service import model_service
from app.services.knowledge_service import knowledge_service
from app.services.prompt_service import prompt_service
from app.ai.agent.agent import create_re_agent
from app.ai.model.anthropic import AnthropicModel
from app.ai.model.openai import OpenAI
from app.ai.tools.custom_api_tool import create_api_tool
from app.ai.memory.supabase_chat_memory import SupabaseChatMessageHistory
from langchain_core.messages import HumanMessage
from app.models.schemas.chat_session import ChatSession, ChatSessionCreate, ChatSessionUpdate, Message
import uuid
from datetime import datetime, timedelta

class ChatService(SupabaseService):
    async def get_or_create_session(self, agent_id: int) -> ChatSession:
        # Check for an existing active session
        result = self.client.table('chat_sessions').select('*').eq('agent_id', agent_id).eq('is_active', True).execute()
        if result.data:
            return ChatSession(**result.data[0])

        # Create a new session
        session_id = str(uuid.uuid4())
        new_session = ChatSessionCreate(agent_id=agent_id)
        result = self.client.table('chat_sessions').insert({
            'id': session_id,
            'agent_id': agent_id,
            'messages': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'is_active': True
        }).execute()
        
        return ChatSession(**result.data[0])

    async def chat(self, agent_id: int, message: str) -> str:
        session = await self.get_or_create_session(agent_id)
        
        agent = await agent_service.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent with id {agent_id} not found")

        model = await model_service.get_model(agent.model_id)
        model_provider = await model_service.get_model_provider(model.provider_id)
        # knowledge_base = await knowledge_service.get_knowledge_base(agent.knowledge_base_id) if agent.knowledge_base_id else None
        
        # Fetch all prompts associated with the agent
        agent_prompts = await agent_service.get_agent_prompts(agent_id)
        prompts = [await prompt_service.get_prompt(ap.prompt_id) for ap in agent_prompts]
        prompt_content = "\n".join([p.content for p in prompts if p])

        # Initialize the model based on the provider
        if model_provider.name.lower() == "anthropic":
            llm = AnthropicModel(model_name=model.version, **model.default_parameters)
        elif model_provider.name.lower() == "openai":
            llm = OpenAI(model_name=model.version)
        else:
            raise ValueError(f"Unsupported model provider: {model_provider.name}")
        
        # Check if the model type is supported for chat
        if model.type not in ["text-generation", "chat"]:
            raise ValueError(f"Unsupported model type for chat: {model.type}")
        
        # Initialize tools
        tools = []
        # for tool_config in agent.tools:
        #     tool = create_api_tool(tool_config)
        #     tools.append(tool)

        # Initialize memory
        memory = SupabaseChatMessageHistory(session_id=session.id)

        # Create the agent
        agent_executor = create_re_agent(llm, tools, prompt_content, memory)

        # Execute the agent
        config = {"configurable": {"thread_id": session.id}}
        response = ""
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=message)]}, config
        ):
            response += str(chunk)

        # Update session with new messages
        memory.add_message(HumanMessage(content=message))
        memory.add_message(HumanMessage(content=response))

        self.client.table('chat_sessions').update({
            'updated_at': datetime.now().isoformat()
        }).eq('id', session.id).execute()

        return response

    async def end_session(self, agent_id: int):
        self.client.table('chat_sessions').update({
            'is_active': False,
            'updated_at': datetime.now().isoformat()
        }).eq('agent_id', agent_id).eq('is_active', True).execute()

    async def cleanup_inactive_sessions(self, max_inactivity: timedelta = timedelta(hours=24)):
        cutoff_time = datetime.now() - max_inactivity
        self.client.table('chat_sessions').update({
            'is_active': False
        }).lt('updated_at', cutoff_time.isoformat()).eq('is_active', True).execute()

    async def get_session_history(self, session_id: str) -> ChatSession:
        result = self.client.table('chat_sessions').select('*').eq('id', session_id).execute()
        if not result.data:
            raise ValueError(f"Session with id {session_id} not found")
        return ChatSession(**result.data[0])

chat_service = ChatService()