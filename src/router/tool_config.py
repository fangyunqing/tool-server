from fastapi import APIRouter, Request

from core import CommonResult

tool_config_router = APIRouter(prefix="/tool_config", tags=["tool_config"])


@tool_config_router.get("/price")
async def search(request: Request):
    env = request.scope["env"]
    return CommonResult.success(await env.DB.prepare(
        "SELECT * FROM tool_config WHERE item_name like '%price'"
    ).run().results)
