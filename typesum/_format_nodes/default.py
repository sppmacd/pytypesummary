from typesum import _fmt
from typesum._format_nodes import FormatNode, FormatResult
from typesum._utils import SaturatingInt


class Default(FormatNode):
    """The default formatter.

    Returns repr(obj) if short enough, otherwise the type name.
    """

    def __init__(self, obj: _fmt.Formattable) -> None:
        self.obj = obj
        self.contraction_level = SaturatingInt(0, 1)

    def contract(self) -> bool:
        return self.contraction_level.inc()

    def format(self) -> FormatResult:
        match self.contraction_level.val:
            case 0:
                return repr(self.obj)
            case 1:
                return _fmt.type_(type(self.obj).__name__)
        return None
