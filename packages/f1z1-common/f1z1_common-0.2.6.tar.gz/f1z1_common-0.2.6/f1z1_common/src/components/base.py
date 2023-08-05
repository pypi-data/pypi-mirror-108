# @Time     : 2021/6/2
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Coroutine


class ICoroutineAdapters(object):
    """
    coroutine adapters
    """

    def to_coroutine(self, *args, **kwargs) -> Coroutine:
        raise NotImplementedError("NotImplemented .to_coroutine(*args, **kwargs) -> Coroutine")


class ITimeController(object):
    """
    emitter timer
    """

    async def timeout(self, *args, **kwargs):
        raise NotImplementedError("NotImplemented .timeout(*args, **kwargs)")
