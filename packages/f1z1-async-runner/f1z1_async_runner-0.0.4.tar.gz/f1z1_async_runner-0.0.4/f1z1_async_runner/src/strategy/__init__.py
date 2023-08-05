# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .base import IRunStrategy, IRunStrategyFactory
from .coro import CoroStrategy
from .coro_function import CoroFunctionStrategy
from .function import FunctionStrategy
from .factory import RunStrategies, StrategyFactory
