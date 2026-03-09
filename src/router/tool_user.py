import time

from core import CommonResult
from fastapi import APIRouter, Request
from model import AddToolUserModel, UpdateToolUserModel

tool_user_router = APIRouter(prefix="/tool_user", tags=["tool_user"])


@tool_user_router.get("/code/{code}")
async def query_by_code(request: Request, code: str):
    env = request.scope["env"]
    config_result = await env.DB.prepare(
        "SELECT * FROM tool_user WHERE code = ?"
    ).bind(code).run()
    return CommonResult.success(config_result.to_py()["results"])


@tool_user_router.get("/list")
async def query(request: Request):
    env = request.scope["env"]
    config_result = await env.DB.prepare(
        "SELECT * FROM tool_user ORDER BY create_time DESC"
    ).run()
    return CommonResult.success(config_result.to_py()["results"])


@tool_user_router.post("/add")
async def create(request: Request, add: AddToolUserModel):
    env = request.scope["env"]
    await env.DB.prepare(
        "INSERT INTO tool_user (code, life_time, account_num, create_time) VALUES (?, ?, ?, ?)",
    ).bind(add.code, add.life_time, add.account_num, int(time.time() * 1000)).run()
    return CommonResult.success()



@tool_user_router.post("/update")
async def renew(request: Request, update: UpdateToolUserModel):
    env = request.scope["env"]
    await env.DB.prepare(
        "UPDATE tool_user SET life_time = ?, account_num = ?, update_time = ? WHERE code = ?",
    ).bind(update.life_time, update.account_num, int(time.time() * 1000), update.code).run()
    return CommonResult.success()


@tool_user_router.delete("/{code}")
async def remove(request: Request, code: str):
    env = request.scope["env"]
    await env.DB.prepare(
        "DELETE FROM tool_user WHERE code = ?",
    ).bind(code).run()
    return CommonResult.success()