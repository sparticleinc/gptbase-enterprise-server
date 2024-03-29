from fastapi import APIRouter

from gptbase_enterprise.endpoints.config import router as config_router
from gptbase_enterprise.endpoints.environmental_data import router as environmental_data_router
from gptbase_enterprise.endpoints.gptbase import router as gptbase_router
from gptbase_enterprise.endpoints.question import router as question_router
from gptbase_enterprise.endpoints.wechat import router as wechat_router

router = APIRouter()
router.include_router(environmental_data_router)
router.include_router(gptbase_router)
router.include_router(config_router)
router.include_router(question_router)
router.include_router(wechat_router)
