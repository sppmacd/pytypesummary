from __future__ import annotations

from typing import TYPE_CHECKING

from typesum import _fmt
from typesum._format_nodes import FormatNode, FormatResult
from typesum._utils import SaturatingInt

if TYPE_CHECKING:
    import numpy as np


class Array(FormatNode):
    def __init__(self, obj: np.ndarray) -> None:
        self.obj = obj
        # 0 - print full array (TODO)
        # 1 - print np.ndarray(shape,dtype)
        # 2 - print np.ndarray(dtype)
        self.contraction_level = SaturatingInt(1, 2)

    def contract(self) -> bool:
        return self.contraction_level.inc()

    def format(self) -> FormatResult:
        match self.contraction_level.val:
            case 1:
                return f"{_fmt.type_('ndarray')}({_fmt.number(self.obj.shape)}*{{{
                    _fmt.type_(self.obj.dtype)
                }}}))"
            case 2:
                return f"{_fmt.type_('ndarray')}({self.obj.dtype})"
        return None
