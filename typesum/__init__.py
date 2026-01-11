"""Type summary."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typesum.config import Config
from typesum.formatter import Formatter

if TYPE_CHECKING:
    from typesum import _fmt
    from typesum.expands import Expand

_default_formatter = Formatter(Config())


def format(  # noqa: A001
    obj: _fmt.Formattable,
    *,
    expand: list[Expand | str] | None = None,
    enable_ansi: bool | None = None,
) -> str:
    """Generate a short 'summary' string of the object.

    Args:
        obj: The object to summarize.
        expand: A list of "expands" to force on an object. They will
            not be contracted. This can be also used to add expands
            that are not added by default.
        enable_ansi: Whether to use ANSI escape codes for formatting.
            This overrides configuration.

    """
    return _default_formatter.format(
        obj,
        expand=expand,
        enable_ansi=enable_ansi,
    )


def print(  # noqa: A001
    *objs: list[_fmt.Formattable],
    expand: list[Expand | str] | None = None,
    enable_ansi: bool | None = None,
) -> None:
    """Print a short 'summary' string of the object."""
    return _default_formatter.print(
        *objs,
        expand=expand,
        enable_ansi=enable_ansi,
    )
