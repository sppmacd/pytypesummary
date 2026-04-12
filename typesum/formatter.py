from __future__ import annotations

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
        **kwargs: dict[str, _fmt.Formattable],
    ) -> None:
        """Print a short 'summary' string of the object."""

        def _format_obj(obj):
            return self.format(
                obj,
                expand=expand,
                enable_ansi=enable_ansi,
                _is_print=True,
            )

        def _format_pair(key, value):
            if key is None:
                return _format_obj(value)
            return f"{key} = {_format_obj(value)}"

        object_pairs = []
        if objs:
            object_pairs.extend((None, obj) for obj in objs)
        if kwargs:
            object_pairs.extend(kwargs.items())

        if len(object_pairs) == 1:
            print(_format_pair(*object_pairs[0]))
        else:
            print("[")
            for key, value in object_pairs:
                print("  " + _format_pair(key, value) + ",")
            print("]")
