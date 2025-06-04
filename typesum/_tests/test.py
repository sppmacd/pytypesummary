"""Some tests."""  # noqa: INP001

# ruff: noqa: ANN201 (return type annotations)
# ruff: noqa: D101, D102 (docstrings)
# ruff: noqa: PT009 (assertEqual)

from unittest import TestCase

import typesum as ts
import typesum._fmt

typesum._fmt.enable_fmt = False  # noqa: SLF001
typesum.MAX_LENGTH = 55


class TestDefault(TestCase):
    def test(self):
        self.assertEqual(ts.format(1), "1")


class TestStr(TestCase):
    def test(self):
        self.assertEqual(ts.format("TEST"), '"TEST"')
        self.assertEqual(ts.format("TESTGGGGGGGGGGGGGGGG"), '"TESTGGGGGGGGGGGGGGGG"')
        self.assertEqual(ts.format("12345612345612345"), '"12345612345612345"')
        self.assertEqual(ts.format("123456123456123456"), '"123456123456123456"')
        self.assertEqual(ts.format("1234561234561234567"), '"1234561234561234567"')


class TestIterable(TestCase):
    def test_list(self):
        self.assertEqual(ts.format([1, 2.0, 3]), "list[1, 2.0, 3]")
        self.assertEqual(ts.format([1, 2, "test", 4]), 'list[1, 2, "test", 4]')
        self.assertEqual(
            ts.format([1, 2, ["test"], 4]),
            'list[1, 2, list["test"], 4]',
        )
        self.assertEqual(
            ts.format([1, 2, ["test"], 4, 5, 6, ["test2"], "testaaaaggggaaaaa3"]),
            "list[int, int, list[1], int, int, int, list[1], str]",
        )

    def test_range(self):
        self.assertEqual(ts.format(range(100)), "range(0, 100)")

    def test_tuple(self):
        complex_list = ([*range(15), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "test", [], {}],)
        self.assertEqual(ts.format(complex_list), "tuple[list[24]]")
        self.assertEqual(
            ts.format(complex_list, expand=["aggregate"]),
            "tuple[1*{list[15*{int}, 6*{float}, 1*{str}, 1*{list[]}, 1*{dict}]}]",
        )
        self.assertEqual(
            ts.format(complex_list[0][:5], expand=["type"]),
            "list[int(0), int(1), int(2), int(3), int(4)]",
        )


class TestNumPy(TestCase):
    def test_array(self):
        import numpy as np

        self.assertEqual(
            ts.format(np.array([4, 5, 6])),
            "ndarray((3,)*{int64})",
        )
        self.assertEqual(
            ts.format(np.array([[1, 2, 3], [4, 5, 6]])),
            "ndarray((2, 3)*{int64})",
        )
        self.assertEqual(
            ts.format(
                (
                    np.array([[1, 2, 3], [4, 5, 6]]),
                    np.array(
                        [[[1, 10], [2, 20], [3, 30]], [[4, 40], [5, 50], [6, 60]]],
                    ),
                ),
            ),
            "tuple[ndarray(int64), ndarray(int64)]",
        )
        self.assertEqual(
            ts.format(
                (
                    np.array([[1, 2, 3], [4, 5, 6]]),
                    np.array(
                        [[[1, 10], [2, 20], [3, 30]], [[4, 40], [5, 50], [6, 60]]],
                    ),
                ),
                expand=["size"],
            ),
            "tuple[2]",
            # FIXME: I don't like this output. This is because
            # the default output (with all sizes) is too long, and we
            # can't contract SIZE, so we contract ALL_ARRAY_MEMBERS
            # instead. Maybe we shouldn't contract a default expand just
            # because of an forced expand?
        )
        self.assertEqual(
            ts.format(np.zeros((100, 100, 100))),
            "ndarray((100, 100, 100)*{float64})",
        )

    def test_generic(self):
        import numpy as np

        self.assertEqual(
            ts.format(
                [
                    np.int8(-1),
                    np.int16(-10),
                    np.int32(-100),
                    np.int64(-1000),
                ],
            ),
            "list[-1i8, -10i16, -100i32, -1000i64]",
        )
        self.assertEqual(
            ts.format(
                [
                    np.uint8(1),
                    np.uint16(10),
                    np.uint32(100),
                    np.uint64(1000),
                ],
            ),
            "list[1u8, 10u16, 100u32, 1000u64]",
        )
        self.assertEqual(
            ts.format(
                [
                    np.float16(1.2),
                    np.float32(3.4),
                    np.float64(5.67),
                ],
            ),
            "list[1.2001953125f16, 3.4000000953674316f32, 5.67f64]",
        )


class TestPandas(TestCase):
    def test_dataframe(self):
        import pandas as pd

        self.assertEqual(
            ts.format(pd.DataFrame({"a": [1, 2], "b": [3, 4]})),
            "DataFrame(2*{[a, b]})",
        )
        self.assertEqual(
            ts.format(pd.DataFrame({"a": [1, 2], "b": [3, 4]}).set_index("a")),
            "DataFrame(a->2*{[b]})",
        )
        self.assertEqual(
            ts.format(
                pd.DataFrame({"a": [1, 2], "b": [3, 4]}).set_index("a"),
                expand=["type"],
            ),
            "DataFrame(a->2*{[b: int64]})",
        )

    def test_series(self):
        import pandas as pd

        self.assertEqual(ts.format(pd.Series([1, 2, 3, 4, 5])), "Series(5*{int64})")


class TestTorch(TestCase):
    def test_tensor(self):
        import torch

        self.assertEqual(
            ts.format(
                torch.tensor([1, 2, 3, 4, 5]),
            ),
            "tensor[cpu]((5,)*{int64})",
        )


class TestExpand(TestCase):
    def test_invalid_expand(self):
        with self.assertRaises(ValueError):  # noqa: PT027
            ts.format([1, 2, 3], expand=["invalid_expand"])
