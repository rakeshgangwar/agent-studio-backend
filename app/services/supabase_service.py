from supabase import create_client, Client
from app.config import settings
from app.models.schemas.agent import Agent, AgentCreate
from app.models.schemas.knowledge_base import KnowledgeBase
from app.models.schemas.tool import Tool
from app.models.schemas.prompt import Prompt
from typing import List, Dict, Any
import asyncio


class SupabaseService:
    def __init__(self):
        self.client: Client = create_client(settings.supabase_url, settings.supabase_key)

    async def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        try:
            result = await self.client.rpc('execute_query', {'query': query, 'params': params}).execute()
            return result.data
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            raise

    async def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        try:
            result = await self.client.rpc('get_table_schema', {'table_name': table_name}).execute()
            return result.data
        except Exception as e:
            print(f"Error getting table schema: {str(e)}")
            raise


supabase_service = SupabaseService()
