"""A list of used expands."""

from enum import Enum


class Expand(Enum):
    """Expand enum.

    TODO: docs
    """

    # Aggregate (count) array elements
    AGGREGATE = "aggregate"
    # Always print the value of an object
    VALUE = "value"
    # Print all array members
    ALL_ARRAY_MEMBERS = "all_array_members"
    # Print the long contracted string (15 chars)
    LONG_STRING = "long_string"
    # Print the short contracted string (6 chars)
    SHORT_STRING = "short_string"
    # Print array size/shape
    SIZE = "size"
    # Print columns (for dataframes)
    COLUMNS = "columns"
    # Print object's type (usually only if value was not printed)
    TYPE = "type"
