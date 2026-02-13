from typing import Any

from pydantic import BaseModel

from python_modules.typing_extensions import overload


class CommonResult(BaseModel):

    message: str = "OK"
    data: Any = None
    code: int = 200

    @staticmethod
    def success(data: Any = None) -> dict:
        return CommonResult(data=data).model_dump()

    @staticmethod
    def fail(message: str, code=999, data: Any = None) -> dict:
        return CommonResult(code=code, message=message, data=data).model_dump()
