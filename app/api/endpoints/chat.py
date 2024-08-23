from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.chat_service import chat_service
from app.models.schemas.chat import ChatInput, ChatResponse
from app.models.schemas.chat_session import ChatSession
from datetime import timedelta

router = APIRouter()


@router.post("/agents/{agent_id}/chat", response_model=ChatResponse)
async def chat_with_agent(agent_id: int, chat_input: ChatInput, background_tasks: BackgroundTasks):
    try:
        response = await chat_service.chat(agent_id, chat_input.message)
        background_tasks.add_task(chat_service.cleanup_inactive_sessions)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/{agent_id}/end-session")
async def end_chat_session(agent_id: int):
    try:
        await chat_service.end_session(agent_id)
        return {"message": "Session ended successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}", response_model=ChatSession)
async def get_session_history(session_id: str):
    try:
        return await chat_service.get_session_history(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
