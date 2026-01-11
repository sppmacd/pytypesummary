from __future__ import annotations

import os
import sys

from typesum import _fmt
from typesum._format_nodes import utils
from typesum.config import AnsiPrint, Config
from typesum.expands import Expand


class Formatter:
    """A "top-level" class for Typesum formatting."""

    def __init__(self, config: Config | None = None) -> None:
        """Initialize the formatter with a configuration."""
        if config is None:
            config = Config()

        self._config = config

    def format(
        self,
        obj: _fmt.Formattable,
        *,
        expand: list[Expand | str] | None = None,
        enable_ansi: bool | None = None,
        _is_print: bool = False,
    ) -> str:
        """Generate a short 'summary' string of the object.

        See `typesum.format` for more details.

        """
        if not expand:
            expand = []

        if enable_ansi is None:
            enable_ansi = False
            if _is_print:
                match self._config.ansi_print:
                    case AnsiPrint.ALWAYS:
                        enable_ansi = True
                    case AnsiPrint.TTY_ONLY:
                        enable_ansi = (
                            sys.stdout.isatty() if sys.platform != "win32" else False
                        )
                    case AnsiPrint.NEVER:
                        enable_ansi = False
            else:
                enable_ansi = self._config.ansi_format

        expand_enum: list[Expand] = [
            Expand(e) if isinstance(e, str) else e for e in expand
        ]

        fn = utils.create_format_node(obj, expand=expand_enum)

        style = _fmt.Style(ansi=enable_ansi)

        while True:
            fstr = fn.format(style)
            if fstr and len(fstr) <= self._config.max_length:
                return fstr
            if not fn.contract():
                if fstr:
                    return fstr + style.error(" (!)")
                return "..."

    def print(
        self,
        *objs: list[_fmt.Formattable],
        expand: list[Expand | str] | None = None,
        enable_ansi: bool | None = None,
    ) -> None:
        """Print a short 'summary' string of the object."""

        def _format(obj):
            return self.format(
                obj,
                expand=expand,
                enable_ansi=enable_ansi,
                _is_print=True,
            )

        if len(objs) == 1:
            print(_format(objs[0]))

        print("[")
        for obj in objs:
            print("  " + _format(obj) + ",")
        print("]")
