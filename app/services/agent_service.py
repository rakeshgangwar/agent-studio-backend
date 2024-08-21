import asyncio
from typing import List

from app.models.schemas.agent import AgentCreate, Agent
from app.models.schemas.knowledge_base import KnowledgeBase
from app.models.schemas.tool import Tool
from app.models.schemas.prompt import Prompt
from app.services.supabase_service import SupabaseService


class AgentService(SupabaseService):
    async def create_agent(self, agent: AgentCreate) -> Agent:
        try:
            result = self.client.table('agents').insert({
                'name': agent.name,
                'description': agent.description
            }).execute()

            agent_id = result.data[0]['id']

            # Associate knowledge bases
            # await asyncio.gather(*[
            #     self.client.table('agent_knowledge_bases').insert({
            #         'agent_id': agent_id,
            #         'knowledge_base_id': kb_id
            #     }).execute()
            #     for kb_id in agent.knowledge_base_ids
            # ])

            # Associate tools
            # await asyncio.gather(*[
            #     self.client.table('agent_tools').insert({
            #         'agent_id': agent_id,
            #         'tool_id': tool_id
            #     }).execute()
            #     for tool_id in agent.tool_ids
            # ])

            # Associate prompts
            # await asyncio.gather(*[
            #     self.client.table('agent_prompts').insert({
            #         'agent_id': agent_id,
            #         'prompt_id': prompt_id
            #     }).execute()
            #     for prompt_id in agent.prompt_ids
            # ])

            return await self.get_agent(agent_id)
        except Exception as e:
            print(f"Error creating agent: {str(e)}")
            raise

    async def get_agent(self, agent_id: int) -> Agent | None:
        try:
            result = self.client.table('agents').select('*').eq('id', agent_id).execute()
            if not result.data:
                return None
            agent_data = result.data[0]

            # Fetch associated knowledge bases
            # kb_result = await self.client.table('agent_knowledge_bases') \
            #     .select('knowledge_bases(*)') \
            #     .eq('agent_id', agent_id) \
            #     .execute()
            # agent_data['knowledge_bases'] = [
            #     KnowledgeBase(**item['knowledge_bases'])
            #     for item in kb_result.data
            # ]

            # Fetch associated tools
            # tool_result = await self.client.table('agent_tools') \
            #     .select('tools(*)') \
            #     .eq('agent_id', agent_id) \
            #     .execute()
            # agent_data['tools'] = [
            #     Tool(**item['tools'])
            #     for item in tool_result.data
            # ]

            # Fetch associated prompts
            # prompt_result = await self.client.table('agent_prompts') \
            #     .select('prompts(*)') \
            #     .eq('agent_id', agent_id) \
            #     .execute()
            # agent_data['prompts'] = [
            #     Prompt(**item['prompts'])
            #     for item in prompt_result.data
            # ]

            return Agent(**agent_data)
        except Exception as e:
            print(f"Error getting agent: {str(e)}")
            raise

    async def list_agents(self) -> List[Agent]:
        try:
            result = self.client.table('agents').select('*').execute()
            agents = []
            for agent_data in result.data:
                # agent = self.get_agent(agent_data['id'])
                agents.append(agent_data)
            return agents
        except Exception as e:
            print(f"Error listing agents: {str(e)}")
            raise

    async def update_agent(self, agent_id: int, agent_update: AgentCreate) -> Agent:
        try:
            # Update agent details
            await self.client.table('agents').update({
                'name': agent_update.name,
                'description': agent_update.description
            }).eq('id', agent_id).execute()

            # Update knowledge bases
            await self.client.table('agent_knowledge_bases').delete().eq('agent_id', agent_id).execute()
            await asyncio.gather(*[
                self.client.table('agent_knowledge_bases').insert({
                    'agent_id': agent_id,
                    'knowledge_base_id': kb_id
                }).execute()
                for kb_id in agent_update.knowledge_base_ids
            ])

            # Update tools
            await self.client.table('agent_tools').delete().eq('agent_id', agent_id).execute()
            await asyncio.gather(*[
                self.client.table('agent_tools').insert({
                    'agent_id': agent_id,
                    'tool_id': tool_id
                }).execute()
                for tool_id in agent_update.tool_ids
            ])

            # Update prompts
            await self.client.table('agent_prompts').delete().eq('agent_id', agent_id).execute()
            await asyncio.gather(*[
                self.client.table('agent_prompts').insert({
                    'agent_id': agent_id,
                    'prompt_id': prompt_id
                }).execute()
                for prompt_id in agent_update.prompt_ids
            ])

            return await self.get_agent(agent_id)
        except Exception as e:
            print(f"Error updating agent: {str(e)}")
            raise

    async def delete_agent(self, agent_id: int) -> bool:
        try:
            # Delete associated records
            await self.client.table('agent_knowledge_bases').delete().eq('agent_id', agent_id).execute()
            await self.client.table('agent_tools').delete().eq('agent_id', agent_id).execute()
            await self.client.table('agent_prompts').delete().eq('agent_id', agent_id).execute()

            # Delete the agent
            result = await self.client.table('agents').delete().eq('id', agent_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error deleting agent: {str(e)}")
            raise


agent_service = AgentService()
