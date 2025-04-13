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
    complex_list = ([*range(15), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "test", [], {}],)
    print_summary(complex_list)
    print_summary(complex_list, expand=[Expand.AGGREGATE])
    print_summary(complex_list[0][:5], expand=[Expand.TYPE])

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
    print_summary(
        [
            np.int8(-1),
            np.int16(-10),
            np.int32(-100),
            np.int64(-1000),
        ],
    )
    print_summary(
        [
            np.uint8(1),
            np.uint16(10),
            np.uint32(100),
            np.uint64(1000),
        ],
    )
    print_summary(
        [
            np.float16(1.2),
            np.float32(3.4),
            np.float64(5.67),
        ],
    )

    # Pandas
    print_summary(pd.DataFrame({"a": [1, 2], "b": [3, 4]}))
    print_summary(pd.DataFrame({"a": [1, 2], "b": [3, 4]}).set_index("a"))
    print_summary(pd.Series([1, 2, 3, 4, 5]))

    # TODO: PyTorch tensors
