from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Prompt(BaseModel):
    id: int
    name: str
    content: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PromptCreate(BaseModel):
    name: str
    content: str
    description: Optional[str] = None


class PromptUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None