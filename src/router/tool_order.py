from fastapi import APIRouter, Request
from core import CommonResult

tool_order_router = APIRouter(prefix="/tool_order", tags=["tool_order"])


@tool_order_router.get("/code/{code}")
async def query_by_code(request: Request, code: str):
    env = request.scope["env"]
    smt = env.DB.prepare(
        "SELECT * FROM tool_order WHERE code = ? LIMIT 30"
    )
    result = await smt.bind(code).run()
    return CommonResult.success(result.to_py()["results"])

