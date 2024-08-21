from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Tool(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime