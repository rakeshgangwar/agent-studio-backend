from app.services.supabase_service import SupabaseService
from app.models.schemas.knowledge_base import KnowledgeBase

class KnowledgeService(SupabaseService):
    async def get_knowledge_base(self, knowledge_base_id: int) -> KnowledgeBase | None:
        try:
            result = self.client.table('knowledge_bases').select('*').eq('id', knowledge_base_id).execute()
            if not result.data:
                return None
            knowledge_base_data = result.data[0]
            return KnowledgeBase(**knowledge_base_data)
        except Exception as e:
            print(f"Error getting knowledge base: {str(e)}")
            raise

knowledge_service = KnowledgeService()