# app/services/prompt_service.py
from typing import List
from app.models.schemas.prompt import PromptCreate, Prompt
from app.services.supabase_service import SupabaseService


class PromptService(SupabaseService):
    async def create_prompt(self, prompt: PromptCreate) -> Prompt:
        try:
            result = self.client.table('prompts').insert({
                'content': prompt.content,
                'description': prompt.description
            }).execute()

            prompt_id = result.data[0]['id']

            return await self.get_prompt(prompt_id)
        except Exception as e:
            print(f"Error creating prompt: {str(e)}")
            raise

    async def get_prompt(self, prompt_id: int) -> Prompt | None:
        try:
            result = self.client.table('prompts').select('*').eq('id', prompt_id).execute()
            if not result.data:
                return None
            prompt_data = result.data[0]

            return Prompt(**prompt_data)
        except Exception as e:
            print(f"Error getting prompt: {str(e)}")
            raise

    async def list_prompts(self) -> List[Prompt]:
        try:
            result = self.client.table('prompts').select('*').execute()
            prompts = []
            for prompt_data in result.data:
                # model = self.get_model(model_data['id'])
                prompts.append(prompt_data)
            return prompts
        except Exception as e:
            print(f"Error listing prompts: {str(e)}")
            raise

    async def update_prompt(self, prompt_id: int, prompt_update: PromptCreate) -> Prompt:
        try:
            self.client.table('prompts').update({
                'content': prompt_update.content,
                'description': prompt_update.description
            }).eq('id', prompt_id).execute()

            return await self.get_prompt(prompt_id)
        except Exception as e:
            print(f"Error updating prompt: {str(e)}")
            raise

    async def delete_prompt(self, prompt_id: int) -> bool:
        try:
            result = self.client.table('prompts').delete().eq('id', prompt_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error deleting prompt: {str(e)}")
            raise


prompt_service = PromptService()
