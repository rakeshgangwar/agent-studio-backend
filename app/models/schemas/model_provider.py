from datetime import datetime

from pydantic import BaseModel


class ModelProvider(BaseModel):
    id: int
    name: str
    description: str
    website: str
    created_at: datetime
    updated_at: datetime


class ModelProviderCreate(BaseModel):
    name: str
    description: str
    website: str
