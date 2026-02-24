import datetime

from fastapi import APIRouter, Request
from core import CommonResult
from model import CreateToolOrderModel

tool_order_router = APIRouter(prefix="/tool_order", tags=["tool_order"])


@tool_order_router.get("/code/{code}")
async def query_by_code(request: Request, code: str):
    env = request.scope["env"]
    smt = env.DB.prepare(
        "SELECT * FROM tool_order WHERE code = ? ORDER BY create_time DESC LIMIT 30"
    )
    result = await smt.bind(code).run()
    return CommonResult.success(result.to_py()["results"])

@tool_order_router.get("order_status/{order_status}")
async def query_by_order_status(request: Request, order_status: int):
    env = request.scope["env"]
    smt = env.DB.prepare(
        "SELECT * FROM tool_order WHERE order_status = ? ORDER BY create_time DESC LIMIT 30"
    )
    result = await smt.bind(order_status).run()
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
    if real_fee != float(create.fee):
        return CommonResult.fail("订单费用发生变化，请关闭后重新下订单")
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


@tool_order_router.put("/pay/{order_id}")
async def pay_voucher(request: Request, order_id: int):
    env = request.scope["env"]
    pay_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await env.DB.prepare(
        "UPDATE tool_order SET order_status = 2, pay_time = ? WHERE id = ?"
    ).bind(pay_time, order_id).run()
    return CommonResult.success()

@tool_order_router.put("/confirm/{order_id}")
async def confirm(request: Request, order_id: int):
    env = request.scope["env"]
    finish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await env.DB.prepare(
        "UPDATE tool_order SET order_status = 3, finish_time = ? WHERE id = ?"
    ).bind(finish_time, order_id).run()

    user_result = await env.DB.prepare(
        "SELECT B.code, B.add_account_num, B.add_day_num, A.life_time, A.account_num FROM tool_order B "
        "LEFT JOIN tool_user A ON B.code = A.code "
        "WHERE B.id = ?"
    ).bind(order_id).run()

    user = user_result.results[0]
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    if user.account_num and user.life_time:
        current_account_num= user.account_num + user.add_account_num
        life_time = datetime.datetime.strptime(user.life_time, '%Y-%m-%d %H:%M:%S')
        if life_time > now:
            current_life_time = life_time + datetime.timedelta(days=user.add_day_num)
        else:
            current_life_time = now + datetime.timedelta(days=user.add_day_num)
        await (env.DB.prepare(
            "UPDATE tool_user SET life_time = ?, account_num = ?, update_time = ? WHERE code = ?"
        ).bind(
            current_life_time.strftime("%Y-%m-%d %H:%M:%S"),
            current_account_num,
            current_time,
            user.code)
        ).run()
    else:
        current_life_time = now + datetime.timedelta(days=user.add_day_num)
        current_account_num = user.add_account_num
        await (env.DB.prepare(
            "INSERT INTO tool_user(code, life_time, account_num, creat_time) VALUES (?, ?, ?, ?)"
        ).bind(
            user.code,
            current_life_time.strftime("%Y-%m-%d %H:%M:%S"),
            current_account_num,
            current_time)
        ).run()

    return CommonResult.success()


