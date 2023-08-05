# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Any, Callable, Coroutine, Dict, Tuple, TypeVar, Union

ArgsType = Tuple[Any]
KwargsType = Dict[str, Any]
CoroOrFunction = Union[Callable, Coroutine]
ReturnType = TypeVar("ReturnType")


class IRunner(object):
    """
    runner interface
    """

    @property
    def coro_or_func(self) -> CoroOrFunction:
        raise NotImplementedError("coro_or_func")

    @property
    def args(self) -> ArgsType:
        raise NotImplementedError("")

    def run(self, *args, **kwargs) -> ReturnType:
        raise NotImplementedError("")
