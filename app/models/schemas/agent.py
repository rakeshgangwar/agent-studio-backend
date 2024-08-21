from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class Agent(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AgentCreate(BaseModel):
    name: str
    description: Optional[str] = None
