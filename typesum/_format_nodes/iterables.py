from __future__ import annotations

import typing
from collections import Counter

from typesum import _fmt
from typesum._format_nodes import FormatNode, FormatResult, utils
from typesum.expands import Expand


def _aggregate_objects(obj_nodes: typing.Iterable) -> Counter:
    return Counter(a.format() or "..." for a in obj_nodes)


def _format_aggregated_types(agg_objs: Counter) -> str:
    return ", ".join(f"{_fmt.number(v)}*{{{k}}}" for k, v in agg_objs.items())


def _aggregate_and_format_objects(obj_nodes: typing.Iterable) -> str:
    return _format_aggregated_types(_aggregate_objects(obj_nodes))


class RaIterable(FormatNode):
    """Format a random-access iterable (has iter, len, getindex)."""

    def __init__(self, obj: typing.Any) -> None:  # FIXME: require Sized & Iterable
        super().__init__(
            obj,
            expands=[
                Expand.ALL_ARRAY_MEMBERS,
                Expand.SIZE,
            ],
        )

    def _generate_obj_nodes(self) -> None:
        # FIXME: don't generate for every element at there might be a lot
        #       of them
        self.obj_nodes = [
            utils.create_format_node(o, expand=self._forced_expands) for o in self.obj
        ]

    def init(self) -> None:
        self._generate_obj_nodes()

    def _contract_children(self) -> bool:
        # First, contract all the children. If no child can be
        # contracted, start contracting us.
        any_child_contracted = False
        for on in self.obj_nodes:
            if on.contract():
                any_child_contracted = True
        return any_child_contracted

    def format(self) -> FormatResult:
        type_name = _fmt.type_(type(self.obj).__name__)

        if self._has_expand(Expand.ALL_ARRAY_MEMBERS):
            return f"{type_name}[{
                ', '.join(on.format() or '...' for on in self.obj_nodes)
            }]"

        has_size = self._has_expand(Expand.SIZE)

        if self._has_expand(Expand.AGGREGATE):
            if has_size:
                return f"{type_name}[{_fmt.number(len(self.obj))}: {
                    _aggregate_and_format_objects(self.obj_nodes)
                }]"
            return f"{type_name}[{_aggregate_and_format_objects(self.obj_nodes)}]"

        if has_size:
            return f"{type_name}[{_fmt.number(len(self.obj))}]"

        return type_name
