from typesum._format_nodes import (
    FormatNode,
    default,
    iterables,
    numpy,
    pandas,
    primitives,
)
from typesum.expands import Expand


def _is_instance_by_full_name(obj, name: str) -> bool:
    for m in type(obj).mro():
        full_name = f"{m.__module__}.{m.__name__}"
        if full_name == name:
            return True
    return False


def create_format_node(obj, *, expand: list[Expand]) -> FormatNode:
    o: FormatNode
    if isinstance(obj, str):
        o = primitives.Str(obj)
    elif isinstance(obj, (list, tuple)):
        o = iterables.RaIterable(obj)
    elif _is_instance_by_full_name(obj, "numpy.ndarray"):
        o = numpy.Array(obj)
    elif _is_instance_by_full_name(obj, "numpy.generic"):
        o = numpy.Generic(obj)
    elif _is_instance_by_full_name(obj, "pandas.core.frame.DataFrame"):
        o = pandas.DataFrame(obj)
    elif _is_instance_by_full_name(obj, "pandas.core.series.Series"):
        o = pandas.Series(obj)
    else:
        o = default.Default(obj)

    o.set_forced_expands(expand)
    o.init()
    return o
