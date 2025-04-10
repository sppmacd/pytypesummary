from __future__ import annotations

from typesum import _fmt
from typesum._format_nodes import FormatNode, FormatResult
from typesum._utils import SaturatingInt


class Str(FormatNode):
    def __init__(self, obj: str) -> None:
        self.obj = obj
        # 0 - print full string
        # 1 - print shortened string
        # 2 - print shortened string stage 2
        # 3 - print only type
        self.contraction_level = SaturatingInt(0, 3)

    def contract(self) -> bool:
        return self.contraction_level.inc()

    def format(self) -> FormatResult:
        match self.contraction_level.val:
            case 0:
                obj_repr = f'"{self.obj}"'
                return f"{_fmt.string(obj_repr)}"
            case 1 | 2:
                MAX_LEN = [15, 6][self.contraction_level.val - 1]  # noqa: N806
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
