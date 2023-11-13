from uuid import UUID

from fastapi import APIRouter, HTTPException

from gptbase_enterprise.models import EnvironmentData
from gptbase_enterprise.schemata import EnvironmentDataIn

router = APIRouter(prefix='/api/v1/environmental_data', tags=['Environmental data'])


# 获取环境配置
@router.get('/{ai_id}')
async def get_environmental_data(ai_id: UUID):
    environmental_data = await EnvironmentData.filter(robot_id=ai_id, deleted_at__isnull=True).all()
    return environmental_data


# 新增环境配置
@router.post('/{ai_id}')
async def create_environmental_data(ai_id: UUID, environmental_data: EnvironmentDataIn):
    environmental_data.robot_id = ai_id
    environmental_data_obj = await EnvironmentData.create(**environmental_data.dict(exclude_unset=True))
    return environmental_data_obj


# 修改环境配置
@router.put('/{environmental_data_id}')
async def update_environmental_data(environmental_data_id: UUID, environmental_data: EnvironmentDataIn):
    environmental_data_obj = await EnvironmentData.get_or_none(id=environmental_data_id, deleted_at__isnull=True)
    if environmental_data_obj is None:
        raise HTTPException(
            status_code=404, detail='Not found')
    await EnvironmentData.filter(id=environmental_data_id).update(
        **environmental_data.dict(exclude_unset=True))

    return await EnvironmentData.get(id=environmental_data_id)


# 删除环境配置
@router.delete('/{environmental_data_id}', status_code=204)
async def delete_environmental_data(environmental_data_id: UUID):
    environmental_data_obj = await EnvironmentData.get_or_none(id=environmental_data_id, deleted_at__isnull=True)
    if environmental_data_obj is None:
        raise HTTPException(
            status_code=404, detail='Not found')
    await environmental_data_obj.soft_delete()
