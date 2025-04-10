from __future__ import annotations

from typing import TYPE_CHECKING

from typesum import _fmt
from typesum._format_nodes import FormatNode, FormatResult

if TYPE_CHECKING:
    import pandas as pd


class DataFrame(FormatNode):
    def __init__(self, obj: pd.DataFrame) -> None:
        self.obj = obj

    def format(self) -> FormatResult:
        idx_string = (
            f"{self.obj.index.name}->" if self.obj.index.name is not None else ""
        )
        return f"{_fmt.type_('DataFrame')}({idx_string}{_fmt.number(len(self.obj))}*{{[{
            ', '.join(self.obj.columns)
        }]}})"
