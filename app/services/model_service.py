import asyncio
from typing import List

from app.models.schemas.model import ModelCreate, Model
from app.services.supabase_service import SupabaseService
from app.ai.model.anthropic import anthropic


class ModelService(SupabaseService):
    async def create_model(self, model: ModelCreate) -> Model:
        try:
            result = self.client.table('models').insert({
                'name': model.name,
                'description': model.description,
                'version': model.version,
                'type': model.type
            }).execute()

            model_id = result.data[0]['id']

            return await self.get_model(model_id)
        except Exception as e:
            print(f"Error creating model: {str(e)}")
            raise

    async def get_model(self, model_id: int) -> Model | None:
        try:
            result = self.client.table('models').select('*').eq('id', model_id).execute()
            if not result.data:
                return None
            model_data = result.data[0]

            return Model(**model_data)
        except Exception as e:
            print(f"Error getting model: {str(e)}")
            raise

    async def list_models(self) -> List[Model]:
        anthropic.systemPrompt(prompt="Your name is John Cena")
        print(anthropic.model.invoke("What is your name?"))
        try:
            result = self.client.table('models').select('*').execute()
            models = []
            for model_data in result.data:
                # model = self.get_model(model_data['id'])
                models.append(model_data)
            return models
        except Exception as e:
            print(f"Error listing models: {str(e)}")
            raise

    # async def update_model(self, model_id: int, model_update: ModelCreate) -> Model:
    #     try:
    #         # Update model details
    #         await self.client.table('models').update({
    #             'name': model_update.name,
    #             'description': model_update.description
    #         }).eq('id', model_id).execute()
    #
    #         return await self.get_model(model_id)
    #     except Exception as e:
    #         print(f"Error updating model: {str(e)}")
    #         raise

    async def delete_model(self, model_id: int) -> bool:
        try:
            # Delete the model
            result = self.client.table('models').delete().eq('id', model_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error deleting model: {str(e)}")
            raise


model_service = ModelService()
