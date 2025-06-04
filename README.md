# PyTypeSummary

Display any Python object in a readable way, with a single function for
everything.

Output is limited so that it fits on the screen, but you can still
select what you want to see through [expands](./typesum/expands.py).

This is work in progress; API _will_ change.

## Install

Clone, then `pip install .`.

## Some examples

Basic usage:

```py
>>> import typesum as ts

>>> ts.print(1)
1

>>> ts.print("A very long string" * 1000)
"A very ...g string"
```

If you don't want to print, you can `format`:

```py
>>> import typesum as ts

>>> ts.format(1)
"1"

>>> ts.format("A very long string" * 1000)
"A very ...g string"
```

Lists:

```py
>>> ts.print([1, 2, 3, 4, 5]*2)
list[1, 2, 3, 4, 5, 1, 2, 3, 4, 5]

>>> ts.print([1, 2, 3, 4, 5]*10)
list[50]
```

Tuples:

```py
>>> ts.print((1, "string", 2))
tuple[1, "string", 2]

>>> ts.print((1, "string", 2), expand=["type"])
tuple[int(1), "string", int(2)]
```

Count elements:

```py
>>> ts.print([1,1,2,2,3,3,1,2,3]*10, expand=["aggregate"])
list[90: 90*{int}]

>>> ts.print([1,1,2,2,3,3,1,2,3]*10, expand=["aggregate", "value"])
list[90: 30*{1}, 30*{2}, 30*{3}]
```

NumPy arrays:

```py
>>> ts.print(np.array([4, 5, 6]))
ndarray((3,)*{int64})

>>> ts.print(np.array([[1, 2, 3], [4, 5, 6]]))
ndarray((2, 3)*{int64})
```

Pandas:

```py
>>> ts.print(pd.DataFrame({"a": [1, 2], "b": [3, 4]}))
DataFrame(2*{[a, b]})

>>> ts.print(pd.DataFrame({"a": [1, 2], "b": [3, 4]}).set_index("a"))
DataFrame(a->2*{[b]})

>>> ts.print(pd.DataFrame({"a": [1, 2], "b": [3, 4]}), expand=["type"])
DataFrame(2*{[a: int64, b: int64]})
```

PyTorch:

```py
>>> ts.print(torch.tensor([[1, 1], [2, 3], [3, -1], [4, 6], [5, 2]]))
tensor[cpu]((5, 2)*{int64})
```

Set maximum length (it is bypassed by manually specified expands):

```py
>>> ts
ts.MAX_LENGTH = 10

>>> ts.print(torch.tensor([[1, 1], [2, 3], [3, -1], [4, 6], [5, 2]]))
tensor(int64) (!)   # got longer than max length!
```
