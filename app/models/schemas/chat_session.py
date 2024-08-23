from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.models.schemas.message import Message


class ChatSession(BaseModel):
    id: str
    agent_id: int
    messages: List[Message]
    created_at: datetime
    updated_at: datetime
    is_active: bool

class ChatSessionCreate(BaseModel):
    agent_id: int

class ChatSessionUpdate(BaseModel):
    messages: Optional[List[Message]] = None
    updated_at: Optional[datetime] = None
    is_active: Optional[bool] = None