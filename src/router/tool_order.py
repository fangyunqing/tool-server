import datetime

from fastapi import APIRouter, Request
from core import CommonResult
from model import CreateToolOrderModel

tool_order_router = APIRouter(prefix="/tool_order", tags=["tool_order"])


@tool_order_router.get("/code/{code}")
async def query_by_code(request: Request, code: str):
    env = request.scope["env"]
    smt = env.DB.prepare(
        "SELECT * FROM tool_order WHERE code = ? LIMIT 30"
    )
    result = await smt.bind(code).run()
    return CommonResult.success(result.to_py()["results"])


@tool_order_router.post("/add")
async def add(request: Request, create: CreateToolOrderModel):
    # 是否费用发生变化
    env = request.scope["env"]
    config_result = await env.DB.prepare(
        "SELECT item_name, item_value FROM tool_config WHERE item_name LIKE '%_price'"
    ).run()
    real_fee = 0
    for config in config_result.results:
        if config.item_name == "account_price":
            real_fee += float(config.item_value) * create.add_account_num
        elif config.item_name == "day_price":
            real_fee += float(config.item_value) * create.add_day_num
    real_fee = round(real_fee, 2)
    if str(real_fee) != create.fee:
        return CommonResult.fail()
    # 插入
    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await env.DB.prepare(
        "INSERT INTO tool_order("
        "code, fee, account_price, add_account_num, day_price, add_day_num, order_status, create_time"
        ") "
        f"VALUES (?, ?, ?, ?, ?, ?, 1, ?)"
    ).bind(
        create.code, create.fee, create.account_price, create.add_account_num, create.day_price, create.add_day_num
        ,create_time
    ).run()
    return CommonResult.success()


