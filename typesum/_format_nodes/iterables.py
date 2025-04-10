from __future__ import annotations

import typing
from collections import Counter

from typesum import _fmt
from typesum._format_nodes import FormatNode, FormatResult, utils
from typesum._utils import SaturatingInt


def _aggregate_objects(obj_nodes: typing.Iterable) -> Counter:
    return Counter(a.format() or "..." for a in obj_nodes)


def _format_aggregated_types(agg_objs: Counter) -> str:
    return ", ".join(f"{_fmt.type_(v)}*{{{k}}}" for k, v in agg_objs.items())


def _aggregate_and_format_objects(obj_nodes: typing.Iterable) -> str:
    return _format_aggregated_types(_aggregate_objects(obj_nodes))


class RaIterable(FormatNode):
    """Format a random-access iterable (has iter, len, getindex)."""

    def __init__(self, obj: typing.Any) -> None:  # FIXME: require Sized & Iterable
        self.obj = obj
        # 0 - print every array element
        # 1 - print a short form (1*{int}, 2*{float}, ...)
        # 2 - print only type and size
        # 3 - print only type
        self.contraction_level = SaturatingInt(0, 3)

        # generate format nodes for each element
        self._generate_obj_nodes()

    def _generate_obj_nodes(self) -> None:
        # FIXME: don't generate for every element at there might be a lot
        #       of them
        self.obj_nodes = [utils.create_format_node(o) for o in self.obj]

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

    def format(self) -> FormatResult:
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
