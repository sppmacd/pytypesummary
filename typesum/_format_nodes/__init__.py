"""FormatNode class."""

from __future__ import annotations

from abc import abstractmethod

from typesum import _fmt
from typesum._utils import SaturatingInt

FormatResult = str | None


class FormatNode:
    """The format node.

    TODO: docs
    """

    @abstractmethod
    def format(self) -> FormatResult:
        """Format the node.

        Returns None if the know that the string
        will be too long; then the formatter will call 'contract'
        first.
        """

    def contract(self) -> bool:
        """Make the node return a shorter representation in `format`.

        Returns `False` it its not possible anymore.
        """
        return False
