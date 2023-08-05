# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import get_event_loop, get_running_loop

from .base import IRunStrategy
from ..runner import IRunner


class FunctionStrategy(IRunStrategy):

    def __init__(self, runner: IRunner):
        self._runner = runner

    @property
    def runner(self):
        return self._runner

    async def execute(self, runner: IRunner, *args, **kwargs):
        loop = get_running_loop()
        if loop is None:
            loop = get_event_loop()
        return await  loop.run_in_executor(None, runner.coro_or_func, *runner.args)

    async def async_run(self, *args, **kwargs):
        return await self.execute(self.runner)
