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
        "SELECT item_name, item_value FROM tool_config WHERE item_name LILE '%_price'"
    ).run()
    print(22)
    real_fee = 0
    for config in config_result.results:
        if config.item_name == "account_price":
            real_fee += float(config.item_value) * create.add_account_num
        elif config.item_name == "day_price":
            real_fee += float(config.item_value) * create.add_day_num
    real_fee = round(real_fee, 2)
    if str(real_fee) != create.fee:
        raise Exception("费用发生变化，请重新提交")
    # 插入
    print(1)
    await env.DB.prepare(
        "INSERT INTO tool_order(code, fee, count_price, add_account_num, day_price, add_price_num) "
        "VALUES (?, ?, ?, ?, ?, ?)"
    ).bind(
        create.code, create.fee, create.count_price, create.add_account_num, create.day_price, create.add_price_num
    ).run()
    return CommonResult.success()


