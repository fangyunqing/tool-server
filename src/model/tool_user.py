from pydantic import BaseModel


class AddToolUserModel(BaseModel):
    code: str
    life_time: int
    account_num: int


class UpdateToolUserModel(BaseModel):
    code: str
    life_time: int
    account_num: int
