from fastapi import APIRouter, HTTPException
from typing import List
from schemas import MitigationCreateSchema, MitigationUpdateSchema, MitigationResponseSchema
from mitigation_service import create_mitigation, get_mitigation, get_all_mitigations, update_mitigation, delete_mitigation

router = APIRouter(prefix="/mitigations", tags=["Mitigations"])

@router.post("/", response_model=MitigationResponseSchema)
async def create(data: MitigationCreateSchema):
    return await create_mitigation(data)

@router.get("/", response_model=List[MitigationResponseSchema])
async def list_all():
    return await get_all_mitigations()

@router.get("/{mitigation_id}", response_model=MitigationResponseSchema)
async def get_one(mitigation_id: int):
    mitigation = await get_mitigation(mitigation_id)
    if not mitigation:
        raise HTTPException(status_code=404, detail="Mitigation not found")
    return mitigation

@router.put("/{mitigation_id}", response_model=MitigationResponseSchema)
async def update(mitigation_id: int, data: MitigationUpdateSchema):
    mitigation = await update_mitigation(mitigation_id, data)
    if not mitigation:
        raise HTTPException(status_code=404, detail="Mitigation not found")
    return mitigation

@router.delete("/{mitigation_id}")
async def delete(mitigation_id: int):
    mitigation = await delete_mitigation(mitigation_id)
    if not mitigation:
        raise HTTPException(status_code=404, detail="Mitigation not found")
    return {"detail": "Mitigation deleted successfully"}
