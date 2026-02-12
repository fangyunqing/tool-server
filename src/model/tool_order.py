from pydantic import BaseModel

class CreateToolOrderModel(BaseModel):
    # 机器码
    code: str
    # 费用
    fee: str
    # 账户单价
    count_price: str
    # 账户增加数
    add_account_num: int
    # 天数单价
    day_price: str
    # 天数增加数
    add_day_num: int
