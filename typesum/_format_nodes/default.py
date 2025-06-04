from typesum import _fmt
from typesum._format_nodes import FormatNode, FormatResult
from typesum.expands import Expand


class Default(FormatNode):
    """The default formatter.

    Returns repr(obj) if short enough, otherwise the type name.
    """

    def __init__(self, obj: _fmt.Formattable) -> None:
        super().__init__(obj, expands=[Expand.VALUE])

    def format(self, style: _fmt.Style) -> FormatResult:
        type_name = style.type_(type(self.obj).__name__)
        if self._has_expand(Expand.VALUE):
            style_func = (
                style.number if isinstance(self.obj, (int, float, complex)) else None
            )

            obj_repr = style_func(repr(self.obj)) if style_func else repr(self.obj)

            if self._has_expand(Expand.TYPE):
                return f"{type_name}({obj_repr})"
            return obj_repr

        return type_name
