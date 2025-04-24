from __future__ import annotations

from typing import TYPE_CHECKING

from typesum import _fmt
from typesum._format_nodes import FormatNode, FormatResult
from typesum.expands import Expand

if TYPE_CHECKING:
    import torch


class Tensor(FormatNode):
    def __init__(self, obj: torch.Tensor) -> None:
        super().__init__(
            obj,
            expands=[
                Expand.DEVICE,
                Expand.SIZE,
            ],
        )

    def format(self) -> FormatResult:
        type_name = _fmt.type_("tensor")
        if self._has_expand(Expand.DEVICE):
            type_name += f"[{self.obj.device}]"
        dtype_name = _fmt.type_(repr(self.obj.dtype)[len("torch.") :])
        if self._has_expand(Expand.SIZE):
            return f"{type_name}({_fmt.number(tuple(self.obj.shape))}*{{{dtype_name}}})"

        return f"{type_name}({dtype_name})"
