# app/api/endpoints/prompt.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas.prompt import PromptCreate, Prompt
from app.services.prompt_service import prompt_service

router = APIRouter()


@router.post("/", response_model=Prompt)
async def create_prompt(prompt: PromptCreate):
    try:
        return await prompt_service.create_prompt(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{prompt_id}", response_model=Prompt)
async def get_prompt(prompt_id: int):
    try:
        prompt = await prompt_service.get_prompt(prompt_id)
        if prompt is None:
            raise HTTPException(status_code=404, detail="Prompt not found")
        return prompt
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Prompt])
async def list_prompts():
    try:
        return await prompt_service.list_prompts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{prompt_id}", response_model=Prompt)
async def update_prompt(prompt_id: int, prompt: PromptCreate):
    try:
        prompt = await prompt_service.update_prompt(prompt_id, prompt)
        if prompt is None:
            raise HTTPException(status_code=404, detail="Prompt not found")
        return prompt
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{prompt_id}", response_model=bool)
async def delete_prompt(prompt_id: int):
    try:
        return await prompt_service.delete_prompt(prompt_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))