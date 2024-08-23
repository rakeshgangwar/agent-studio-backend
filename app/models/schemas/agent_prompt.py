from pydantic import BaseModel

class AgentPrompt(BaseModel):
    id: int
    agent_id: int
    prompt_id: int

class AgentPromptCreate(BaseModel):
    agent_id: int
    prompt_id: int