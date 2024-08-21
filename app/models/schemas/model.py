from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Json


class Model(BaseModel):
    id: int
    name: str
    type: str
    version: str
    description: Optional[str] = None
    configuration: Optional[Json]
    default_parameters: Optional[Json]
    created_at: datetime
    updated_at: datetime
    is_active: bool
    provider_id: int


class ModelCreate(BaseModel):
    name: str
    type: str
    version: str
    description: Optional[str] = None
    configuration: Optional[Json] = None
    default_parameters: Optional[Json] = None
    is_active: bool
    provider_id: int
