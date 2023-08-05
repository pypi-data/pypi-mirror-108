# @Time     : 2021/6/2
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from asyncio import Task, create_task
from typing import Callable, Coroutine, TypeVar, Union

from ..validator.is_validators import is_coroutine

CoroOrFunction = Union[Callable, Coroutine]
CoroOrFuncOrTask = Union[CoroOrFunction, Task]
ReturnType = TypeVar("ReturnType")


class AbstractTaskPolicy(metaclass=ABCMeta):
    """
    task policy
    """

    def __init__(self, coro_or_func: CoroOrFunction):
        self._coro_or_func = coro_or_func

    @property
    def coro_or_func(self):
        return self._coro_or_func

    @abstractmethod
    def to_task(self, *args, **kwargs) -> Task:
        raise NotImplementedError("NotImplemented .to_task(*args, **kwargs) -> Task")

    def _create_task(self, coro):
        if not is_coroutine(coro):
            raise ValueError(
                f"coro need Coroutine, but got {type(coro).__name__}"
            )
        return create_task(coro)


class AbstractExecutorPolicy(object):
    """
    executor policy
    """

    def __init__(self, executed: CoroOrFuncOrTask):
        self._executed = executed

    @property
    def executed(self):
        return self._executed

    @abstractmethod
    async def executor(self, *args, **kwargs) -> ReturnType:
        raise NotImplementedError("NotImplemented .executor(*args, **kwargs) -> ReturnType")

    async def run(self, *args, **kwargs) -> ReturnType:
        return await self.executor(*args, **kwargs)

    def _is_task(self, executed):
        return isinstance(executed, Task)
