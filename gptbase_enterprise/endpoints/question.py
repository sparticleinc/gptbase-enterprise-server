import httpx
from fastapi import APIRouter
from starlette.responses import StreamingResponse

from gptbase_enterprise.settings import GPTBASE_URL

router = APIRouter(prefix='/api/v1/question', tags=['Question'])


@router.post('/{ai_id}')
async def question(ai_id: str, message: dict):
    return StreamingResponse(fetch_data(ai_id, message))


async def fetch_data(ai_id: str, message: dict):
    async with httpx.AsyncClient() as client:
        async with client.stream('POST', f'{GPTBASE_URL}/questions/{ai_id}', json=message) as response:
            async for chunk in response.aiter_text():
                yield chunk
