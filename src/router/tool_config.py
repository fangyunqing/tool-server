from fastapi import APIRouter, Request
from workers import Response

from core import CommonResult

tool_config_router = APIRouter(prefix="/tool_config", tags=["tool_config"])


@tool_config_router.get("/price")
async def search(request: Request):
    try:
        env = request.scope["env"]
        data = await env.DB.prepare(
            "SELECT * FROM tool_config WHERE item_name like '%price'"
        ).run()
        return Response.json(data)
    except Exception as e:
        return {"error": str(e)}
