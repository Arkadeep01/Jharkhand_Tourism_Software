from models import Mitigation
from schemas import MitigationCreateSchema, MitigationUpdateSchema

async def create_mitigation(data: MitigationCreateSchema):
    mitigation = await Mitigation.create(**data.dict())
    return mitigation

async def get_mitigation(mitigation_id: int):
    return await Mitigation.get_or_none(id=mitigation_id)

async def get_all_mitigations():
    return await Mitigation.all()

async def update_mitigation(mitigation_id: int, data: MitigationUpdateSchema):
    mitigation = await Mitigation.get_or_none(id=mitigation_id)
    if mitigation:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(mitigation, key, value)
        await mitigation.save()
    return mitigation

async def delete_mitigation(mitigation_id: int):
    mitigation = await Mitigation.get_or_none(id=mitigation_id)
    if mitigation:
        await mitigation.delete()
    return mitigation
