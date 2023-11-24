import httpx
from fastapi import APIRouter
from starlette.requests import Request

from gptbase_enterprise.settings import GPTBASE_URL, GPTBASE_KEY

router = APIRouter(prefix='/api/v1/gptbase', tags=['Gptbase'])


@router.api_route("/{rest:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def forward_data(request: Request):
    url = f"{GPTBASE_URL}{request.url.path.replace('/api/v1/gptbase', '')}"
    url += f"?{request.query_params}" if request.query_params else ""

    print(f"[gptbase_url]: {url}")

    headers = {"Authorization": f"Bearer {GPTBASE_KEY}"}
    body = await request.body() if request.method != "GET" and request.method != "DELETE" else None
    timeout = httpx.Timeout(60.0, read=300.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.request(request.method, url, data=body, headers=headers)
            response.raise_for_status()
            if response.content:
                return response.json()
        except httpx.HTTPStatusError as e:
            print(f"[gptbase_error]: {e}")
            raise e
        except Exception as e:
            print(f"[gptbase_error]: {e}")
            raise e
    return
