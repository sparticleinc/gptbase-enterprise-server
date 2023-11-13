from typing import Optional

from fastapi import APIRouter

from gptbase_enterprise.models import Config

router = APIRouter(prefix='/api/v1/config', tags=['Config'])


# 获取配置
@router.get('/')
async def get_config(name: Optional[str] = 'default'):
    info = await Config.filter(deleted_at=None, name=name).first()
    return info.data
