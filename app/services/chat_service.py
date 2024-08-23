from app.services.agent_service import agent_service
from app.services.supabase_service import SupabaseService


class ChatService(SupabaseService):

    async def initiate_chat(self, agent_id):
        agent = await agent_service.get_agent(agent_id)
        return None
