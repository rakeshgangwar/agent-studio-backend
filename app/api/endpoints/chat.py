from fastapi import APIRouter, HTTPException

from app.services import chat_service

router = APIRouter()


@router.post("/agents/{agent_id}/session/{session_id}/execute")
async def initiate_chat(agent_id: int, session_id: int):
    try:
        return await chat_service.initiate_chat(agent_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
