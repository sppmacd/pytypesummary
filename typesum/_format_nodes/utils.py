from typesum._format_nodes import (
    FormatNode,
    default,
    iterables,
    numpy,
    pandas,
    primitives,
)
from typesum.expands import Expand


def create_format_node(obj, *, expand: list[Expand]) -> FormatNode:
    # print(type(obj).__name__)

    o: FormatNode
    if isinstance(obj, str):
        o = primitives.Str(obj)
    elif isinstance(obj, (list, tuple)):
        o = iterables.RaIterable(obj)
    elif type(obj).__name__ == "ndarray":
        o = numpy.Array(obj)
    elif type(obj).__name__ == "DataFrame":
        o = pandas.DataFrame(obj)
    elif type(obj).__name__ == "Series":
        o = pandas.Series(obj)
    else:
        o = default.Default(obj)

    o.set_forced_expands(expand)
    o.init()
    return o
