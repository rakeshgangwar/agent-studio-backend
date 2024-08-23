from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime