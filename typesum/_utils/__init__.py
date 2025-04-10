class SaturatingInt:
    """An integer which won't go above `maxval`."""

    def __init__(self, initval: int, maxval: int) -> None:
        self._val = initval
        self._maxval = maxval

    def inc(self) -> bool:
        """Increment the value by one.

        Returns False if the value is already at the maximum.
        """
        if self._val >= self._maxval:
            return False
        self._val += 1
        return True

    @property
    def val(self) -> int:
        """Get the current int value."""
        return self._val
