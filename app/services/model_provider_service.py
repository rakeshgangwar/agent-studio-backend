from typing import List

from app.ai.model.anthropic import anthropic
from app.models.schemas.model_provider import ModelProviderCreate, ModelProvider
from app.services.supabase_service import SupabaseService


class ModelProviderService(SupabaseService):
    async def create_model_provider(self, model: ModelProviderCreate) -> ModelProvider:
        try:
            result = self.client.table('model_providers').insert({
                'name': model.name,
                'description': model.description,
                'version': model.website
            }).execute()

            model_provider_id = result.data[0]['id']

            return await self.get_model_provider(model_provider_id)
        except Exception as e:
            print(f"Error creating model_provider: {str(e)}")
            raise

    async def get_model_provider(self, model_provider_id: int) -> ModelProvider | None:
        try:
            result = self.client.table('model_providers').select('*').eq('id', model_provider_id).execute()
            if not result.data:
                return None
            model_provider_data = result.data[0]

            return ModelProvider(**model_provider_data)
        except Exception as e:
            print(f"Error getting model provider: {str(e)}")
            raise

    async def list_model_providers(self) -> List[ModelProvider]:
        try:
            result = self.client.table('model_providers').select('*').execute()
            model_providers = []
            for model_provider_data in result.data:
                # model = self.get_model(model_data['id'])
                model_providers.append(model_provider_data)
            return model_providers
        except Exception as e:
            print(f"Error listing model providers: {str(e)}")
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

    async def delete_model_provider(self, model_provider_id: int) -> bool:
        try:
            # Delete the model
            result = self.client.table('model_providers').delete().eq('id', model_provider_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error deleting model provider: {str(e)}")
            raise


model_provider_service = ModelProviderService()
