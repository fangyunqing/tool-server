from typing import Any

from pydantic import BaseModel


class CommonResult(BaseModel):

    message: str = "success"
    data: Any = None
    code: int = 200

    @staticmethod
    def success(data: Any = None) -> dict:
        return CommonResult(data=data).model_dump()

    @staticmethod
    def fail(code: int, message: str, data: Any = None) -> dict:
        return CommonResult(code=code, message=message, data=data).model_dump()

