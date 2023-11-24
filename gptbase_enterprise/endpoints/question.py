import httpx
from fastapi import APIRouter
from starlette.responses import StreamingResponse

from gptbase_enterprise.settings import GPTBASE_URL

router = APIRouter(prefix='/api/v1/question', tags=['Question'])


@router.post('/{ai_id}')
async def question(ai_id: str, message: dict):
    return StreamingResponse(fetch_data(ai_id, message))


async def fetch_data(ai_id: str, message: dict):
    try:
        timeout = httpx.Timeout(60.0, read=300.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream('POST', f'{GPTBASE_URL}/questions/{ai_id}', json=message) as response:
                async for chunk in response.aiter_text():
                    yield chunk

    except httpx.HTTPStatusError as ex:
        print(f"[question]:Response Error: {ex}")
    except httpx.RequestError as ex:
        print(f"[question]:Request Error: {ex}")
    except Exception as ex:
        print(f"[question]:An error occurred: {ex}")
