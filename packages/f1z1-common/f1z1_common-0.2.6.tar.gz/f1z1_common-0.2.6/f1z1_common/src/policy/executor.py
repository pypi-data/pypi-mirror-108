# @Time     : 2021/6/2
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .base import AbstractExecutorPolicy
from ..components import CoroutineAdapters
from ..validator.is_validators import is_coroutine, is_async_function, is_function


class CoroExecutorPolicy(AbstractExecutorPolicy):
    """
    coro execute policy
    """

    async def executor(self, *args, **kwargs):
        return await self.executed


class CoroFunctionExecutorPolicy(AbstractExecutorPolicy):
    """
    coro function execute policy
    """

    async def executor(self, *args, **kwargs):
        return await self.executed(*args, **kwargs)


class FunctionExecutorPolicy(AbstractExecutorPolicy):
    """
    function execute policy
    """

    def __init__(self, executed, max_workers: int = None):
        super().__init__(executed)
        self._max_workers = max_workers

    async def executor(self, *args, **kwargs):
        fut = self._to_coroutine(*args, **kwargs)
        return await fut

    def _to_coroutine(self, *args, **kwargs):
        sync, max_workers = self.executed, self._max_workers
        adapter = CoroutineAdapters(sync, max_workers)
        return adapter.to_coroutine(*args, **kwargs)


class TaskExecutorPolicy(AbstractExecutorPolicy):

    async def executor(self, *args, **kwargs):
        return await self.executed


class ExecutorPolicyManager(AbstractExecutorPolicy):

    def __init__(self, executed, max_workers: int = None):
        super().__init__(executed)
        self._max_workers = max_workers

    async def executor(self, *args, **kwargs):
        executed = self.executed
        policy: AbstractExecutorPolicy = None
        if is_coroutine(executed):
            policy = self._coro_exec(executed)
        elif self._is_task(executed):
            policy = self._task_exec(executed)
        elif is_async_function(executed):
            policy = self._coro_func_exec(executed)
        elif is_function(executed):
            policy = self._func_exec(executed)
        else:
            raise ValueError(
                f"executed need Coroutine, Task, async function, or function, but got {type(executed).__name__}"
            )
        return await policy.executor(*args, **kwargs)

    def _coro_exec(self, executed):
        return CoroExecutorPolicy(executed)

    def _task_exec(self, executed):
        return TaskExecutorPolicy(executed)

    def _coro_func_exec(self, executed):
        return CoroFunctionExecutorPolicy(executed)

    def _func_exec(self, executed, max_workers: int = None):
        return FunctionExecutorPolicy(executed, max_workers)
