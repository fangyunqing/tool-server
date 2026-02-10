from fastapi import APIRouter, Request

from core import CommonResult

tool_config_router = APIRouter(prefix="/tool_config", tags=["tool_config"])


@tool_config_router.get("/price")
async def search(request: Request):
    try:
        env = request.scope["env"]
        data = await env.DB.prepare(
            "SELECT item_name, item_value FROM tool_config"
        ).run()
        return CommonResult.success(data.to_py()["results"])
    except Exception as e:
        return {"error": str(e)}
