# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ..runner import IRunner, ReturnType


class IRunStrategy(object):
    """
    runner strategy
    """

    @property
    def runner(self) -> IRunner:
        raise NotImplementedError("")

    async def async_run(self, *args, **kwargs) -> ReturnType:
        raise NotImplementedError("")


class IRunStrategyFactory(object):

    @classmethod
    def create(cls, strategy: IRunStrategy, runner: IRunner, **kwargs) -> IRunStrategy:
        raise NotImplementedError("NotImplemented .create(strategy, runner, **kwargs) -> IRunStrategy")
