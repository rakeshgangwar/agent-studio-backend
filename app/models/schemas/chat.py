from pydantic import BaseModel


class ChatInput(BaseModel):
    agent_id: int
    message: str


class ChatResponse(BaseModel):
    response: str