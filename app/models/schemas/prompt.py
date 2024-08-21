from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Prompt(BaseModel):
    id: int
    content: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PromptCreate(BaseModel):
    content: str
    description: Optional[str] = None