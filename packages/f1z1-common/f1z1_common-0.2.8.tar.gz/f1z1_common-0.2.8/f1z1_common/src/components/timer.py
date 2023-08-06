# @Time     : 2021/6/2
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import sleep
from collections.abc import Awaitable
from enum import Enum
from functools import lru_cache
from typing import Union

from ..utils import EnumUtil
from ..validator import is_validators

from .base import ITimeController

NumberTypes = Union[int, float]


class TimeUnit(Enum):
    SECOND = 1
    MILLISECOND = 1000
    MICROSECOND = 1000000


class TimeUtil(object):

    @classmethod
    def to_timestamp(cls, timestamp: NumberTypes, unit: TimeUnit = TimeUnit.MILLISECOND):
        f = {
            TimeUnit.SECOND: cls._to_second,
            TimeUnit.MILLISECOND: cls._to_millisecond,
            TimeUnit.MICROSECOND: cls._to_microsecond
        }.get(unit, cls._to_millisecond)
        return f(timestamp)

    @classmethod
    def _to_second(cls, timestamp: NumberTypes):
        return cls._to_round(timestamp, TimeUnit.SECOND)

    @classmethod
    def _to_millisecond(cls, timestamp: NumberTypes):
        return cls._to_round(timestamp, TimeUnit.MILLISECOND)

    @classmethod
    def _to_microsecond(cls, timestamp: NumberTypes):
        return cls._to_round(timestamp, TimeUnit.MICROSECOND)

    @classmethod
    def _to_round(cls, number: NumberTypes, unit: TimeUnit) -> int:
        cls.check_number(number)
        convert: int = EnumUtil.unenum(unit, "value")
        return round(number * convert)

    @staticmethod
    def check_number(number: NumberTypes):
        if not is_validators.is_number(number):
            raise ValueError(
                f"timestamp need int or float, but got {type(number).__name__}"
            )


class TimeController(Awaitable, ITimeController):

    def __init__(self,
                 wait_time: NumberTypes,
                 unit: TimeUnit = TimeUnit.MILLISECOND):
        self._wait_time = wait_time
        self._unit = unit

    @property
    def wait_time(self):
        return self._wait_time

    @wait_time.setter
    def wait_time(self, new_wait_time: NumberTypes) -> None:
        TimeUtil.check_number(new_wait_time)
        self._wait_time = new_wait_time

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit: TimeUnit) -> None:
        if not is_validators.is_enum(unit):
            return
        self._unit = unit

    async def timeout(self):
        return await sleep(
            self._get_timeout_by(self.wait_time, self.unit)
        )

    def __await__(self):
        return self.timeout().__await__()

    @lru_cache()
    def _get_timeout_by(self, wait_time: NumberTypes, unit: TimeUnit) -> int:
        return TimeUtil.to_timestamp(wait_time, unit)
