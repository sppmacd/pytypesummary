from __future__ import annotations

from typesum import _fmt
from typesum._format_nodes import FormatNode, FormatResult
from typesum.expands import Expand


class Str(FormatNode):
    def __init__(self, obj: str) -> None:
        super().__init__(
            obj,
            expands=[Expand.VALUE, Expand.LONG_STRING],
        )

    def format(self) -> FormatResult:
        if self._has_expand(Expand.VALUE):
            obj_repr = f'"{self.obj}"'
            return f"{_fmt.string(obj_repr)}"

        # contracted string
        has_long_string = self._has_expand(Expand.LONG_STRING)
        has_short_string = self._has_expand(Expand.SHORT_STRING)
        if has_long_string or has_short_string:
            max_len = 15 if has_long_string else 6
            if len(self.obj) <= max_len + 3:
                obj_repr = f'"{self.obj}"'
                return f"{_fmt.string(obj_repr)}"
            obj_repr_beg = f'"{self.obj[: max_len // 2]}'
            obj_repr_end = f"{self.obj[-max_len // 2 :]}"
            ellipsis = "..." if len(self.obj) > max_len else ""
            return f"{_fmt.string(obj_repr_beg)}{_fmt.error(ellipsis)}{
                _fmt.string(obj_repr_end)
            }{_fmt.string('"')}"

        # no expansion
        return f"{_fmt.type_('str')}"
