from typesum._format_nodes import (
    FormatNode,
    default,
    iterables,
    numpy,
    pandas,
    primitives,
)


def create_format_node(obj) -> FormatNode:
    # TODO: dynamically import the modules if used
    import numpy as np
    import pandas as pd

    if isinstance(obj, str):
        return primitives.Str(obj)
    if isinstance(obj, (list, tuple)):
        return iterables.RaIterable(obj)
    if isinstance(obj, np.ndarray):
        return numpy.Array(obj)
    if isinstance(obj, pd.DataFrame):
        return pandas.DataFrame(obj)
    return default.Default(obj)
