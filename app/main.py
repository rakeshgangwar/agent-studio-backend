from fastapi import FastAPI

from app.api.endpoints import agent, model, model_provider

app = FastAPI()

app.include_router(agent.router, prefix="/api/agents", tags=["Agents"])
app.include_router(model.router, prefix="/api/models", tags=["Models"])
app.include_router(model_provider.router, prefix="/api/model-providers", tags=["Model Providers"])

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
