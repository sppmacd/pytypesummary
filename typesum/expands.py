"""Contains Expand enum."""

from enum import Enum


class Expand(Enum):
    """A list of defined Expands.

    Expands allows the user to specify additional data that can be
    printed by the formatter. The supported expands differ by object
    type.

    They are typically passed as array to format() or print():
    ```
    typesum.format(obj, expand=["value", "type"])`
    ```

    You can also use the Expand enum directly:
    ```
    from typesum.expands import Expand
    typesum.format(obj, expand=[Expand.VALUE, Expand.TYPE])
    ```
    """

    AGGREGATE = "aggregate"
    """Aggregate (count) array elements"""

    ALL_ARRAY_MEMBERS = "all_array_members"
    """Print all array members"""

    COLUMNS = "columns"
    """Print column names (for dataframes)"""

    DEVICE = "device"
    """Print device (for Torch tensors)"""

    LONG_STRING = "long_string"
    """Print the long contracted string (15 chars)"""

    SHORT_STRING = "short_string"
    """Print the short contracted string (6 chars)"""

    SIZE = "size"
    """Print array size/shape"""

    TYPE = "type"
    """Print object's type (usually only if value was not printed)"""

    VALUE = "value"
    """Always print the value of an object"""
