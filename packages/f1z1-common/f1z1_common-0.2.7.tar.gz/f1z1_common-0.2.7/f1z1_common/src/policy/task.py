# @Time     : 2021/6/2
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .base import AbstractTaskPolicy
from ..components import CoroutineAdapters
from ..validator.is_validators import is_coroutine, is_async_function, is_function


class CoroTaskPolicy(AbstractTaskPolicy):

    def to_task(self, *args, **kwargs):
        return self._create_task(self._get_coro())

    def _get_coro(self):
        return self.coro_or_func


class CoroFunctionPolicy(AbstractTaskPolicy):

    def to_task(self, *args, **kwargs):
        return self._create_task(self._get_async_ctx(*args, **kwargs))

    async def _get_async_ctx(self, *args, **kwargs):
        return await self.coro_or_func(*args, **kwargs)


class FunctionTaskPolicy(AbstractTaskPolicy):

    def __init__(self, coro_or_func, max_workers: int = None):
        super().__init__(coro_or_func)
        self._max_workers = max_workers

    def to_task(self, *args, **kwargs):
        fut = self._to_coroutine(*args, **kwargs)
        return self._create_task(fut)

    def _to_coroutine(self, *args, **kwargs):
        sync, max_workers = self.coro_or_func, self._max_workers
        adapter = CoroutineAdapters(sync, max_workers)
        return adapter.to_coroutine(*args, **kwargs)


class TaskPolicyManager(AbstractTaskPolicy):

    def __init__(self, coro_or_func, max_workers: int = None):
        super().__init__(coro_or_func)
        self._max_workers = max_workers

    def to_task(self, *args, **kwargs):
        coro_or_func = self.coro_or_func
        policy: AbstractTaskPolicy = None
        if is_coroutine(coro_or_func):
            policy = self._coro_policy(coro_or_func)
        elif is_async_function(coro_or_func):
            policy = self._coro_func_policy(coro_or_func)
        elif is_function(coro_or_func):
            policy = self._func_policy(coro_or_func, self._max_workers)
        else:
            raise ValueError(
                f"coro_or_func need Coroutine, async function or function, but got {type(coro_or_func).__name__}"
            )
        return policy.to_task(*args, **kwargs)

    def _coro_policy(self, coro_or_func):
        return CoroTaskPolicy(coro_or_func)

    def _coro_func_policy(self, coro_or_func):
        return CoroFunctionPolicy(coro_or_func)

    def _func_policy(self, coro_or_func, max_workers: int = None):
        return FunctionTaskPolicy(coro_or_func, max_workers)
