"""Some tests."""

import numpy as np
import pandas as pd

from typesum import obj_summary

if __name__ == "__main__":
    print(obj_summary(1))
    print(obj_summary("TEST"))
    print(obj_summary("TESTGGGGGGGGGGGGGGGG"))
    print(obj_summary("12345612345612345"))
    print(obj_summary("123456123456123456"))
    print(obj_summary("1234561234561234567"))
    print(obj_summary([1, 2.0, 3]))
    print(obj_summary([1, 2, "test", 4]))
    print(obj_summary([1, 2, ["test"], 4]))
    print(obj_summary([1, 2, ["test"], 4, 5, 6, ["test2"], "testaaaaggggaaaaa3"]))
    print(obj_summary(range(100)))
    print(obj_summary([*range(100)]))
    print(obj_summary(np.array([[1, 2, 3], [4, 5, 6]])))
    print(
        obj_summary(
            (
                np.array([[1, 2, 3], [4, 5, 6]]),
                np.array([[[1, 10], [2, 20], [3, 30]], [[4, 40], [5, 50], [6, 60]]]),
            ),
        ),
    )
    print(obj_summary(np.zeros((100, 100, 100))))

    # TODO: Support Pandas, PyTorch, ...
    print(obj_summary(pd.DataFrame({"a": [1, 2], "b": [3, 4]})))
    print(obj_summary(pd.DataFrame({"a": [1, 2], "b": [3, 4]}).set_index("a")))
