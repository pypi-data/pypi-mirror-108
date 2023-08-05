# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .base import IRunStrategy
from ..runner import IRunner


class CoroStrategy(IRunStrategy):
    """
    协程对象策略
    """

    def __init__(self, runner: IRunner):
        self._runner = runner

    @property
    def runner(self):
        return self._runner

    async def execute(self, runner: IRunner, **kwargs):
        return await runner.coro_or_func

    async def async_run(self, *args, **kwargs):
        return await self.execute(runner=self.runner)
