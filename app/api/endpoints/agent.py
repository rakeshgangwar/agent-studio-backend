from fastapi import APIRouter, HTTPException
from typing import List

from app.services.supabase_service import supabase_service
from app.models.schemas.agent import AgentCreate, Agent
from app.services.agent_service import agent_service

router = APIRouter()


@router.post("/", response_model=Agent)
async def create_agent(agent: AgentCreate):
    try:
        return await agent_service.create_agent(agent)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: int):
    try:
        agent = await supabase_service.get_agent(agent_id)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Agent])
async def list_agents():
    try:
        return await agent_service.list_agents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{agent_id}", response_model=bool)
async def delete_agent(agent_id: int):
    try:
        return await supabase_service.delete_agent(agent_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: int, agent: AgentCreate):
    try:
        agent = await supabase_service.update_agent(agent_id, agent)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
