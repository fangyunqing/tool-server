from fastapi import APIRouter, Request
from core import CommonResult

login_router = APIRouter(prefix="/login", tags=["login"])


@login_router.put("/{admin_code}")
async def login(request: Request, admin_code: str):
    env = request.scope["env"]
    config_result = await env.DB.prepare(
        "SELECT item_name, item_value FROM tool_config WHERE item_name = 'admin_code'"
    ).run()
    result = config_result.results[0]
    if result.item_value == admin_code:
        return CommonResult.success()
    else:
        return CommonResult.fail(message="ERROR ADMIN CODE")