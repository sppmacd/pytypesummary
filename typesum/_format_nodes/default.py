from typesum import _fmt
from typesum._format_nodes import FormatNode, FormatResult
from typesum.expands import Expand


class Default(FormatNode):
    """The default formatter.

    Returns repr(obj) if short enough, otherwise the type name.
    """

    def __init__(self, obj: _fmt.Formattable) -> None:
        super().__init__(obj, expands=[Expand.FULL_VALUE])

    def format(self) -> FormatResult:
        type_name = _fmt.type_(type(self.obj).__name__)
        if self._has_expand(Expand.FULL_VALUE):
            if self._has_expand(Expand.TYPE):
                return f"{type_name}({self.obj!r})"
            return repr(self.obj)
        return type_name
