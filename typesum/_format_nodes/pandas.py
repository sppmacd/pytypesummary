from __future__ import annotations

from typing import TYPE_CHECKING

from typesum._format_nodes import FormatNode, FormatResult
from typesum.expands import Expand

if TYPE_CHECKING:
    import pandas as pd
    from pandas.core.frame import Dtype

    from typesum import _fmt


class DataFrame(FormatNode):
    def __init__(self, obj: pd.DataFrame) -> None:
        super().__init__(
            obj,
            expands=[
                Expand.COLUMNS,
            ],
        )

    def format(self, style: _fmt.Style) -> FormatResult:
        type_name = style.type_("DataFrame")

        if not self._has_expand(Expand.COLUMNS):
            return type_name

        def format_column(col: str, dtype: Dtype) -> str:
            if self._has_expand(Expand.TYPE):
                return f"{col}: {style.type_(dtype)}"
            return col

        idx_string = (
            f"{self.obj.index.name}->" if self.obj.index.name is not None else ""
        )
        return f"{type_name}({idx_string}{style.number(len(self.obj))}*{{[{
            ', '.join(
                format_column(c, d) for c, d in zip(self.obj.columns, self.obj.dtypes)
            )
        }]}})"


class Series(FormatNode):
    def __init__(self, obj: pd.Series) -> None:
        super().__init__(
            obj,
            expands=[Expand.SIZE, Expand.TYPE],
        )

    def format(self, style: _fmt.Style) -> FormatResult:
        type_name = style.type_("Series")

        formatted_size = (
            style.number(len(self.obj)) if self._has_expand(Expand.SIZE) else None
        )
        formatted_dtype = (
            style.type_(self.obj.dtype) if self._has_expand(Expand.TYPE) else None
        )

        if formatted_size and formatted_dtype:
            return f"{type_name}({formatted_size}*{{{formatted_dtype}}})"
        if formatted_size:
            return f"{type_name}({formatted_size})"
        if formatted_dtype:
            return f"{type_name}({formatted_dtype})"

        return type_name
