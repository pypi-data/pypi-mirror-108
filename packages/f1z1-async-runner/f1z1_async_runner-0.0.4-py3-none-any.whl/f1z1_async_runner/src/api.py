# @Time     : 2021/5/28
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .runner.base import ArgsType, CoroOrFunction, KwargsType, IRunner
from .runner import AsyncRunner


def is_runner(value):
    return isinstance(value, IRunner)


def create_runner(
        coro_or_func: CoroOrFunction,
        args: ArgsType = None,
        kwargs: KwargsType = None
):
    return AsyncRunner(
        coro_or_func,
        args=args,
        kwargs=kwargs
    )


def start(runner: IRunner):
    if not is_runner(runner):
        raise ValueError(f"runner need IRunner instance, but got {type(runner).__name__}")
    return runner.run()
