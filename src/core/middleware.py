from fastapi.responses import JSONResponse
from starlette.requests import Request

class CheckAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope)
            if request.url.path.startswith("/tool_order/order_status"):
                tool_token = request.headers["tool_token"]
                env = request.scope["env"]
                config_result = await env.DB.prepare(
                    "SELECT item_value FROM tool_config WHERE item_name = 'admin_code'"
                ).run()
                admin_code = config_result.results[0].item_value
                if tool_token == admin_code:
                    await self.app(scope, receive, send)
                else:
                    await JSONResponse(CommonResult.fail(code=401, message="Unauthorized"), 200)(scope, receive, send)
            else:
                await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)
