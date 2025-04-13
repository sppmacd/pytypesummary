from __future__ import annotations

from typing import TYPE_CHECKING

from typesum import _fmt
from typesum._format_nodes import FormatNode, FormatResult
from typesum.expands import Expand

if TYPE_CHECKING:
    import pandas as pd


class DataFrame(FormatNode):
    def __init__(self, obj: pd.DataFrame) -> None:
        super().__init__(
            obj,
            expands=[
                Expand.COLUMNS,
            ],
        )

    def format(self) -> FormatResult:
        type_name = _fmt.type_("DataFrame")

        if not self._has_expand(Expand.COLUMNS):
            return type_name

        idx_string = (
            f"{self.obj.index.name}->" if self.obj.index.name is not None else ""
        )
        return f"{type_name}({idx_string}{_fmt.number(len(self.obj))}*{{[{
            ', '.join(self.obj.columns)
        }]}})"


class Series(FormatNode):
    def __init__(self, obj: pd.Series) -> None:
        super().__init__(
            obj,
            expands=[Expand.SIZE, Expand.TYPE],
        )

    def format(self) -> FormatResult:
        type_name = _fmt.type_("Series")

        formatted_size = (
            _fmt.number(len(self.obj)) if self._has_expand(Expand.SIZE) else None
        )
        formatted_dtype = (
            _fmt.type_(self.obj.dtype) if self._has_expand(Expand.TYPE) else None
        )

        if formatted_size and formatted_dtype:
            return f"{type_name}({formatted_size}*{{{formatted_dtype}}})"
        if formatted_size:
            return f"{type_name}({formatted_size})"
        if formatted_dtype:
            return f"{type_name}({formatted_dtype})"

        return type_name
