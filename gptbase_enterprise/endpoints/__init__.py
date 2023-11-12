from fastapi import APIRouter

from gptbase_enterprise.endpoints.environmental_data import router as environmental_data_router

router = APIRouter()
router.include_router(environmental_data_router)
