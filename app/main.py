from fastapi import FastAPI

from app.api.endpoints import agent

app = FastAPI()

app.include_router(agent.router, prefix="/api/agents", tags=["Agents"])

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
