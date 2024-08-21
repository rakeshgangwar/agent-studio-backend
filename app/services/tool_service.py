from app.models.schemas.tool import Tool
from app.services.supabase_service import SupabaseService


class ToolService(SupabaseService):
    async def create_tool(self, name: str, description: str = None) -> Tool:
        try:
            result = await self.client.table('tools').insert({
                'name': name,
                'description': description
            }).execute()
            return Tool(**result.data[0])
        except Exception as e:
            print(f"Error creating tool: {str(e)}")
            raise
