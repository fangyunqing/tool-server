from fastapi import APIRouter, Request

tool_order_router = APIRouter(prefix="/tool_order", tags=["tool_order"])


@tool_order_router.get("/name")
async def search(request: Request):
    env = request.scope["env"]
    try:
        results = await env.DB.prepare(
            "SELECT * FROM tool_config"
        ).all()
    except Exception as e:
        return {"error": str(e)}
    return {"env": "11", "results": "11"}
