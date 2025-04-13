"""FormatNode class."""

from __future__ import annotations

import copy
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typesum import _fmt
    from typesum.expands import Expand

FormatResult = str | None


class FormatNode:
    """The format node.

    TODO: docs
    """

    """List of supported "expands" ("fields" which will be printed
    in full). For example, we may print the full value ('full'),
    or type ('type'), or both (['full', 'type']). When contracting,
    the expands will be disabled one by one."""
    _enabled_expands: list[Expand]
    _forced_expands: list[Expand]

    def __init__(self, obj: _fmt.Formattable, *, expands: list[Expand]) -> None:
        self.obj = obj
        self._enabled_expands = copy.deepcopy(expands)

    @abstractmethod
    def format(self) -> FormatResult:
        """Format the node.

        Returns None if the know that the string
        will be too long; then the formatter will call 'contract'
        first.
        """

    def contract(self) -> bool:
        """Make the node return a shorter representation in `format`.

        Returns `False` if contraction is not possible anymore.
        """
        # First, try contracting children
        if self._contract_children():
            return True

        # Then, contract us by removing the first non-forced expand.
        for expand in self._enabled_expands:
            if expand not in self._forced_expands:
                self._enabled_expands.remove(expand)
                return True

        # Finally, if we can't contract anymore, return False.
        return False

    def set_forced_expands(self, expands: list[Expand]) -> None:
        """Set the forced expands.

        These expands will not be removed when contracting.
        """
        self._forced_expands = copy.deepcopy(expands)
        self._enabled_expands.extend(expands)
        self._remove_duplicated_expands()

    def _remove_duplicated_expands(self) -> None:
        # keep every expand only once, at the position it was first
        # encountered
        new_expands = []
        seen_expands = set()
        for exp in self._enabled_expands:
            if exp in seen_expands:
                continue
            new_expands.append(exp)
            seen_expands.add(exp)
        self._enabled_expands = new_expands

    def init(self) -> None:
        """Initialize the node. Called after the node is created."""

    def _has_expand(self, expand: Expand) -> bool:
        """Check if the expand is enabled."""
        return expand in self._enabled_expands

    def _contract_children(self) -> bool:
        """Overridden by derived nodes to contract their children.

        Used for lists, dicts etc.

        Returns `False` if contraction is not possible anymore.
        """
        return False
