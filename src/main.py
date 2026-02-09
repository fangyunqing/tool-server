from fastapi import FastAPI, Request
from pydantic import BaseModel
from workers import WorkerEntrypoint

from tool_order import company_router


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        import asgi

        return await asgi.fetch(app, request.js_object, self.env)

app = FastAPI()
app.include_router(company_router)
