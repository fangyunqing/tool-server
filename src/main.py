import json
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from workers import WorkerEntrypoint
from core import CommonResult
from python_modules.starlette import status

from router import tool_order_router, tool_config_router, login_router


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
app.include_router(login_router)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logging.exception(str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=CommonResult.fail(str(exc)),
    )

@app.middleware("auth")
async def check_auth(request: Request, call_next):
    if request.url.path.endswith("admin_tool_order"):
        tool_token = request.headers["tool_token"]
        env = request.scope["env"]
        config_result = await env.DB.prepare(
            "SELECT item_value FROM tool_config WHERE item_name = 'admin_code'"
        ).run()
        admin_code = config_result.results[0].item_value
        if tool_token == admin_code:
            response = await call_next(request)
            return response
        else:
            return CommonResult.fail(code=401, message="Unauthorized")
    else:
        response = await call_next(request)
        return response