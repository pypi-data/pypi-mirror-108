# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum
from functools import partial

from f1z1_common import EnumUtil

from .base import IRunStrategy, IRunStrategyFactory
from .coro import CoroStrategy
from .coro_function import CoroFunctionStrategy
from .function import FunctionStrategy


class RunStrategies(Enum):
    CORO = CoroStrategy
    CORO_FUNCTION = CoroFunctionStrategy
    FUNCTION = FunctionStrategy


class StrategyFactory(IRunStrategyFactory):

    @classmethod
    def create(cls, strategy, runner, **kwargs):
        klass = cls._to_subclass(strategy)
        f = cls._factory(klass, runner)
        return f(**kwargs)

    @classmethod
    def _factory(cls, subclass, runner):
        if not cls._is_strategy_subclass(subclass):
            raise ValueError(f"need a IRunnerStrategy subclass, but got {type(subclass).__name__}")
        return partial(subclass, runner)

    @staticmethod
    def _is_strategy_subclass(klass):
        return issubclass(klass, IRunStrategy)

    @staticmethod
    def _to_subclass(strategies: RunStrategies):
        return EnumUtil.unenum(strategies, "value")
