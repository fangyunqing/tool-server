from fastapi import APIRouter, Request
from core import CommonResult

tool_config_router = APIRouter(prefix="/tool_config", tags=["tool_config"])


@tool_config_router.get("/price")
async def search(request: Request):
    env = request.scope["env"]
    config_result = await env.DB.prepare(
        "SELECT item_name, item_value FROM tool_config WHERE item_name LIKE '%_price'"
    ).run()
    res = {}
    for config in config_result.results:
        res[config.item_name] = config.item_value
    return CommonResult.success(res)