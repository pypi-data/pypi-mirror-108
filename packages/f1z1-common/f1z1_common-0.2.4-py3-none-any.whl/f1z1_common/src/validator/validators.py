# @Time     : 2021/5/27
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .base import AbstractValidator
from .errors import NotFunctionError, NotAsyncFunctionError
from .is_validators import is_function, is_async_function


class FunctionValidator(AbstractValidator):

    def is_validate(self, value, **kwargs) -> bool:
        return is_function(value)

    def raise_error(self, message: str):
        raise NotFunctionError(message)


class AsyncFunctionValidator(AbstractValidator):

    def is_validate(self, value, **kwargs) -> bool:
        return is_async_function(value)

    def raise_error(self, message: str):
        raise NotAsyncFunctionError(message)
