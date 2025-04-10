"""Some tests."""

import numpy as np
import pandas as pd

from typesum import print_summary
from typesum.expands import Expand

if __name__ == "__main__":
    print_summary(1)
    print_summary("TEST")
    print_summary("TESTGGGGGGGGGGGGGGGG")
    print_summary("12345612345612345")
    print_summary("123456123456123456")
    print_summary("1234561234561234567")
    print_summary([1, 2.0, 3])
    print_summary([1, 2, "test", 4])
    print_summary([1, 2, ["test"], 4])
    print_summary([1, 2, ["test"], 4, 5, 6, ["test2"], "testaaaaggggaaaaa3"])
    print_summary(range(100))
    print_summary(
        [*range(15), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "test", [], {}],
        expand=[Expand.AGGREGATE],
    )

    # NumPy
    print_summary(np.array([[1, 2, 3], [4, 5, 6]]))
    print_summary(
        (
            np.array([[1, 2, 3], [4, 5, 6]]),
            np.array([[[1, 10], [2, 20], [3, 30]], [[4, 40], [5, 50], [6, 60]]]),
        ),
    )
    print_summary(
        (
            np.array([[1, 2, 3], [4, 5, 6]]),
            np.array([[[1, 10], [2, 20], [3, 30]], [[4, 40], [5, 50], [6, 60]]]),
        ),
        expand=[Expand.SIZE, Expand.FULL_VALUE],
    )

    print_summary(np.zeros((100, 100, 100)))

    # Pandas
    print_summary(pd.DataFrame({"a": [1, 2], "b": [3, 4]}))
    print_summary(pd.DataFrame({"a": [1, 2], "b": [3, 4]}).set_index("a"))

    # TODO: Pandas Series

    # TODO: PyTorch tensors
