from __future__ import annotations

from typing import TYPE_CHECKING

from typesum import _fmt
from typesum._format_nodes import FormatNode, FormatResult
from typesum.expands import Expand

if TYPE_CHECKING:
    import numpy as np


class Array(FormatNode):
    def __init__(self, obj: np.ndarray) -> None:
        super().__init__(
            obj,
            expands=[
                Expand.SIZE,
            ],
        )

    def format(self) -> FormatResult:
        type_name = _fmt.type_("ndarray")
        if self._has_expand(Expand.SIZE):
            return f"{type_name}({_fmt.number(self.obj.shape)}*{{{
                _fmt.type_(self.obj.dtype)
            }}})"

        return f"{type_name}({self.obj.dtype})"


class Generic(FormatNode):
    """Format numpy.generic types (scalars)."""

    def __init__(self, obj: np.generic) -> None:
        super().__init__(
            obj,
            expands=[],
        )

    def format(self) -> FormatResult:
        dtype_name = str(self.obj.dtype)
        # replace int -> i, uint -> u, float -> f
        dtype_name = (
            dtype_name.replace("uint", "u").replace("int", "i").replace("float", "f")
        )
        return f"{_fmt.number(self.obj.item())}{(dtype_name)}"
