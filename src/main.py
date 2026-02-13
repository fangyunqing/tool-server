import json
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from workers import WorkerEntrypoint
from core import CommonResult
from python_modules.starlette import status

from router import tool_order_router, tool_config_router


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        import asgi

        return await asgi.fetch(app, request.js_object, self.env)




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)

app.include_router(tool_order_router)
app.include_router(tool_config_router)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logging.exception(str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=CommonResult.fail(str(exc)),
    )