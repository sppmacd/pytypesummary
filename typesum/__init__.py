import typing
from abc import abstractmethod
from collections import Counter
from contextlib import contextmanager
from typing import Iterable

import numpy as np

# FIXME: More specific typings
HasRepr = typing.Any
Formattable = typing.Any


def _fmt_type(text: HasRepr) -> str:
    return f"\033[1;32m{text}\033[0m"


def _fmt_number(num: HasRepr) -> str:
    return f"\033[35m{num}\033[0m"


def _aggregate_objects(objs: Iterable) -> Counter:
    return Counter(map(obj_summary, objs))


def _format_aggregated_types(agg_objs: Counter) -> str:
    return ", ".join(f"{_fmt_number(v)}*{{{k}}}" for k, v in agg_objs.items())


def _aggregate_and_format_objects(objs: Iterable) -> str:
    return _format_aggregated_types(_aggregate_objects(objs))


####


class FormatNode:
    @abstractmethod
    def format(self) -> str:
        """Format the node."""
        pass


####


class _FormatNodeList(FormatNode):
    def __init__(self, obj: list):
        self.obj = obj

    def format(self) -> str:
        if len(self.obj) <= 3:
            return f"{_fmt_type('list')}[{', '.join(obj_summary(o) for o in self.obj)}]"
        return f"{_fmt_type('list')}[{_aggregate_and_format_objects(self.obj)}]"


class _FormatNodeTuple(FormatNode):
    def __init__(self, obj: tuple):
        self.obj = obj

    def format(self) -> str:
        return f"{_fmt_type('tuple')}({_aggregate_and_format_objects(self.obj)})"


class _FormatNodeNumpyArray(FormatNode):
    def __init__(self, obj: np.ndarray):
        self.obj = obj

    def format(self) -> str:
        return f"{_fmt_type('np.ndarray')}({self.obj.shape})"


class _FormatNodeDefault(FormatNode):
    """Format object as its type name."""

    def __init__(self, obj: Formattable):
        self.obj = obj

    def format(self) -> str:
        return _fmt_type(type(self.obj).__name__)


####


def _create_format_node(obj: FormatNode):
    if isinstance(obj, list):
        return _FormatNodeList(obj)
    if isinstance(obj, tuple):
        return _FormatNodeTuple(obj)
    if isinstance(obj, np.ndarray):
        return _FormatNodeNumpyArray(obj)
    return _FormatNodeDefault(obj)


def obj_summary(obj: Formattable) -> str:
    """Generate a short 'summary' string of the object"""
    return _create_format_node(obj).format()


if __name__ == "__main__":
    print(obj_summary([1, 2.0, 3]))
    print(obj_summary([1, 2, "test", 4]))
    print(obj_summary([1, 2, ["test"], 4]))
    print(obj_summary(np.array([[1, 2, 3], [4, 5, 6]])))
    print(
        obj_summary(
            (
                np.array([[1, 2, 3], [4, 5, 6]]),
                np.array([[[1, 10], [2, 20], [3, 30]], [[4, 40], [5, 50], [6, 60]]]),
            )
        )
    )
