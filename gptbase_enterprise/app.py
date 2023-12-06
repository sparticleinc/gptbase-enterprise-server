import nest_asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (get_swagger_ui_html)
from starlette import status
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise

from gptbase_enterprise.endpoints import router
from gptbase_enterprise.settings import TORTOISE_ORM

nest_asyncio.apply()

app = FastAPI(
    openapi_url='/api/openapi.json',
)


async def general_exception_handler(request, err):
    base_error_message = f'Failed to execute: {request.method}: {request.url}'
    return JSONResponse({
        'detail': str(err),
        'message': base_error_message
    }, status_code=status.HTTP_400_BAD_REQUEST)


origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_middleware(
    ServerErrorMiddleware,
    handler=general_exception_handler,
)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
)
app.include_router(router)


@app.get('/api/docs-swagger', include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(
        openapi_url='/api/openapi.json',
        title='Documentation',
    )


@app.get('/')
def read_root():
    return 'hello gptbase-enterprise!'
