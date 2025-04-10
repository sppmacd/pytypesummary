"""Type summary."""

from typesum import _fmt
from typesum._format_nodes import utils

MAX_LENGTH = 130


def obj_summary(obj: _fmt.Formattable) -> str:
    """Generate a short 'summary' string of the object."""
    fn = utils.create_format_node(obj)

    while True:
        fstr = fn.format()
        if fstr and len(fstr) <= MAX_LENGTH:
            return fstr
        if not fn.contract():
            if fstr:
                return fstr + " \033[31m(!)\033[m"
            return "..."


def print_summary(obj: _fmt.Formattable) -> None:
    """Print a short 'summary' string of the object."""
    print(obj_summary(obj))  # noqa: T201
