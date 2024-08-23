from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class Agent(BaseModel):
    id: int
    model_config = ConfigDict(protected_namespaces=())
    model_id: Optional[int]
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AgentCreate(BaseModel):
    name: str
    description: Optional[str] = None


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None