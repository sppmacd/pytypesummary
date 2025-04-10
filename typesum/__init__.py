"""Type summary."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typesum._format_nodes import utils

if TYPE_CHECKING:
    from typesum import _fmt
    from typesum.expands import Expand

MAX_LENGTH = 130


def obj_summary(
    obj: _fmt.Formattable,
    *,
    expand: list[Expand] | None = None,
) -> str:
    """Generate a short 'summary' string of the object.

    Args:
        obj: The object to summarize.
        expand: A list of "expands" to force on an object. They will
                not be contracted. This can be also used to add expands
                that are not added by default.

    """
    if not expand:
        expand = []

    fn = utils.create_format_node(obj, expand=expand)

    while True:
        fstr = fn.format()
        if fstr and len(fstr) <= MAX_LENGTH:
            return fstr
        if not fn.contract():
            if fstr:
                return fstr + " \033[31m(!)\033[m"
            return "..."


def print_summary(obj: _fmt.Formattable, *, expand: list[Expand] | None = None) -> None:
    """Print a short 'summary' string of the object."""
    print(obj_summary(obj, expand=expand))  # noqa: T201
