"""Type summary."""

from __future__ import annotations

import typing
from abc import abstractmethod
from collections import Counter

import numpy as np
import pandas as pd

from typesum import _fmt

if typing.TYPE_CHECKING:
    from collections.abc import Iterable


class SaturatingInt:
    """An integer which won't go above `maxval`."""

    def __init__(self, initval: int, maxval: int):
        self._val = initval
        self._maxval = maxval

    def inc(self) -> bool:
        """Increment the value by one.

        Returns False if the value is already at the maximum.
        """
        if self._val >= self._maxval:
            return False
        self._val += 1
        return True

    @property
    def val(self) -> int:
        """Get the current int value."""
        return self._val


###


def _aggregate_objects(obj_nodes: Iterable) -> Counter:
    return Counter(a.format() or "..." for a in obj_nodes)


def _format_aggregated_types(agg_objs: Counter) -> str:
    return ", ".join(f"{_fmt.type_(v)}*{{{k}}}" for k, v in agg_objs.items())


def _aggregate_and_format_objects(obj_nodes: Iterable) -> str:
    return _format_aggregated_types(_aggregate_objects(obj_nodes))


FormatResult = str | None


class FormatNode:
    """The format node.

    TODO: docs
    """

    @abstractmethod
    def format(self) -> FormatResult:
        """Format the node.

        Returns None if the know that the string
        will be too long; then the formatter will call 'contract'
        first.
        """

    def contract(self) -> bool:
        """Make the node return a shorter representation in `format`.

        Returns `False` it its not possible anymore.
        """
        return False


class _FormatNodeStr(FormatNode):
    def __init__(self, obj: str):
        self.obj = obj
        # 0 - print full string
        # 1 - print shortened string
        # 2 - print shortened string stage 2
        # 3 - print only type
        self.contraction_level = SaturatingInt(0, 3)

    def contract(self) -> bool:
        return self.contraction_level.inc()

    def format(self) -> str | None:
        match self.contraction_level.val:
            case 0:
                obj_repr = f'"{self.obj}"'
                return f"{_fmt.string(obj_repr)}"
            case 1 | 2:
                MAX_LEN = [15, 6][self.contraction_level.val - 1]
                if len(self.obj) <= MAX_LEN + 3:
                    obj_repr = f'"{self.obj}"'
                    return f"{_fmt.string(obj_repr)}"
                obj_repr_beg = f'"{self.obj[: MAX_LEN // 2]}'
                obj_repr_end = f"{self.obj[-MAX_LEN // 2 :]}"
                ellipsis = "..." if len(self.obj) > MAX_LEN else ""
                return f"{_fmt.string(obj_repr_beg)}{_fmt.error(ellipsis)}{
                    _fmt.string(obj_repr_end)
                }{_fmt.string('"')}"
            case 3:
                return f"{_fmt.type_('str')}"
        return None


class _FormatNodeRaIterable(FormatNode):
    """Format a random-access iterable (has iter, len, getindex)."""

    def __init__(self, obj: typing.Any):  # FIXME: require Sized & Iterable
        self.obj = obj
        # 0 - print every array element
        # 1 - print a short form (1*{int}, 2*{float}, ...)
        # 2 - print only type and size
        # 3 - print only type
        self.contraction_level = SaturatingInt(0, 3)

        # generate format nodes for each element
        self._generate_obj_nodes()

    def _generate_obj_nodes(self):
        # FIXME: don't generate for every element at there might be a lot
        #       of them
        self.obj_nodes = [_create_format_node(o) for o in self.obj]

    def contract(self) -> bool:
        # First, contract all the children. If no child can be
        # contracted, start contracting us.
        any_child_contracted = False
        for on in self.obj_nodes:
            if on.contract():
                any_child_contracted = True
        if any_child_contracted:
            return True
        if self.contraction_level.val == 0:
            # This is to reset child contraction, as we'd like
            # to contract them again
            self._generate_obj_nodes()

        return self.contraction_level.inc()

    def format(self) -> str | None:
        type_name = type(self.obj).__name__

        match self.contraction_level.val:
            case 0:
                return f"{_fmt.type_(type_name)}[{
                    ', '.join(on.format() or '...' for on in self.obj_nodes)
                }]"
            case 1:
                return f"{_fmt.type_(type_name)}[{
                    _aggregate_and_format_objects(self.obj_nodes)
                }]"
            case 2:
                return f"{_fmt.type_(type_name)}[{len(self.obj)}]"
            case 3:
                return f"{_fmt.type_(type_name)}"

        return None


class _FormatNodeNumpyArray(FormatNode):
    def __init__(self, obj: np.ndarray):
        self.obj = obj
        # 0 - print full array (TODO)
        # 1 - print np.ndarray(shape,dtype)
        # 2 - print np.ndarray(dtype)
        self.contraction_level = SaturatingInt(1, 2)

    def contract(self) -> bool:
        return self.contraction_level.inc()

    def format(self) -> str | None:
        match self.contraction_level.val:
            case 1:
                return f"{_fmt.type_('ndarray')}({_fmt.number(self.obj.shape)}*{{{_fmt.type_(self.obj.dtype)}}}))"
            case 2:
                return f"{_fmt.type_('ndarray')}({self.obj.dtype})"
        return None


class _FormatNodePandasDataFrame(FormatNode):
    def __init__(self, obj: pd.DataFrame):
        self.obj = obj

    def format(self) -> str | None:
        return f"{_fmt.type_('DataFrame')}({_fmt.number(len(self.obj))}*{{[{
            ', '.join(self.obj.columns)
        }]}})"


class _FormatNodeDefault(FormatNode):
    """The default formatter.

    Returns repr(obj) if short enough, otherwise the type name.
    """

    def __init__(self, obj: _fmt.Formattable):
        self.obj = obj
        self.contraction_level = SaturatingInt(0, 1)

    def contract(self) -> bool:
        return self.contraction_level.inc()

    def format(self) -> str | None:
        match self.contraction_level.val:
            case 0:
                return repr(self.obj)
            case 1:
                return _fmt.type_(type(self.obj).__name__)
        return None


####


def _create_format_node(obj: FormatNode) -> FormatNode:
    if isinstance(obj, str):
        return _FormatNodeStr(obj)
    if isinstance(obj, (list, tuple)):
        return _FormatNodeRaIterable(obj)
    if isinstance(obj, np.ndarray):
        return _FormatNodeNumpyArray(obj)
    if isinstance(obj, pd.DataFrame):
        return _FormatNodePandasDataFrame(obj)
    return _FormatNodeDefault(obj)


MAX_LENGTH = 130


def obj_summary(obj: _fmt.Formattable) -> str:
    """Generate a short 'summary' string of the object."""
    fn = _create_format_node(obj)

    while True:
        fstr = fn.format()
        if fstr and len(fstr) <= MAX_LENGTH:
            return fstr
        if not fn.contract():
            if fstr:
                return fstr + " \033[31m(!)\033[m"
            return "..."
