# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .base import IRunStrategy
from ..runner import IRunner, KwargsType


class CoroFunctionStrategy(IRunStrategy):
    """
    协程函数策略
    """

    def __init__(self, runner: IRunner, kwargs: KwargsType = None):
        self._runner = runner
        self._kwargs = kwargs if kwargs else {}

    @property
    def runner(self):
        return self._runner

    @property
    def kwargs(self):
        return self._kwargs

    def _check_coro_function(self, value) -> bool:
        pass

    async def execute(self, runner: IRunner, **kwargs):
        return await runner.coro_or_func(*runner.args, **kwargs)

    async def async_run(self, *args, **kwargs):
        return await self.execute(
            self.runner,
            **self.kwargs
        )
