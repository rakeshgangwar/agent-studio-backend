from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas.model import ModelCreate, Model
from app.services.model_service import model_service

router = APIRouter()


# @router.post("/", response_model=Model)
# async def create_model(model: ModelCreate):
#     try:
#         return await model_service.create_model(model)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.get("/{model_id}", response_model=Model)
async def get_model(model_id: int):
    try:
        model = await model_service.get_model(model_id)
        if model is None:
            raise HTTPException(status_code=404, detail="Model not found")
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Model])
async def list_models():
    try:
        return await model_service.list_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{model_id}", response_model=bool, deprecated=True)
async def delete_model(model_id: int):
    try:
        return await model_service.delete_model(model_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.put("/{model_id}", response_model=Model)
# async def update_model(model_id: int, model: ModelCreate):
#     try:
#         model = await model_service.update_model(model_id, model)
#         if model is None:
#             raise HTTPException(status_code=404, detail="Model not found")
#         return model
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
