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
