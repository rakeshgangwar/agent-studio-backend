from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    project_name: str = "Agent Studio API"
    openai_api_key: str
    anthropic_api_key: str

    class Config:
        env_file = ".env.local"


settings = Settings()
