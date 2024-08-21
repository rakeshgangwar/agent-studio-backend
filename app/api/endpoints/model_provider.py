from typing import List

from fastapi import APIRouter, HTTPException

from app.models.schemas.model_provider import ModelProvider, ModelProviderCreate
from app.services.model_provider_service import model_provider_service

router = APIRouter()


@router.get("/", response_model=List[ModelProvider])
async def list_model_providers():
    try:
        return await model_provider_service.list_model_providers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{model_provider_id}", response_model=ModelProvider)
async def get_model_provider(model_provider_id: int):
    try:
        model_provider = await model_provider_service.get_model_provider(model_provider_id)
        if model_provider is None:
            raise HTTPException(status_code=404, detail="ModelProvider not found")
        return model_provider
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ModelProvider)
async def create_model_provider(model_provider: ModelProviderCreate):
    try:
        return await model_provider_service.create_model_provider(model_provider)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))