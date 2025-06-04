from __future__ import annotations

from typing import TYPE_CHECKING

from typesum._format_nodes import FormatNode, FormatResult
from typesum.expands import Expand

if TYPE_CHECKING:
    import numpy as np

    from typesum import _fmt


class Array(FormatNode):
    def __init__(self, obj: np.ndarray) -> None:
        super().__init__(
            obj,
            expands=[
                Expand.SIZE,
            ],
        )

    def format(self, style: _fmt.Style) -> FormatResult:
        type_name = style.type_("ndarray")
        if self._has_expand(Expand.SIZE):
            return f"{type_name}({style.number(self.obj.shape)}*{{{
                style.type_(self.obj.dtype)
            }}})"

        return f"{type_name}({self.obj.dtype})"


class Generic(FormatNode):
    """Format numpy.generic types (scalars)."""

    def __init__(self, obj: np.generic) -> None:
        super().__init__(
            obj,
            expands=[],
        )

    def format(self, style: _fmt.Style) -> FormatResult:
        dtype_name = str(self.obj.dtype)
        # replace int -> i, uint -> u, float -> f
        dtype_name = (
            dtype_name.replace("uint", "u").replace("int", "i").replace("float", "f")
        )
        return f"{style.number(self.obj.item())}{(dtype_name)}"
