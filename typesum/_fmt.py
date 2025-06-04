"""Format utils."""

import typing

HasRepr = typing.Any
Formattable = typing.Any


class Style:
    def __init__(self, *, ansi: bool = True) -> None:
        self.ansi = ansi

    def type_(self, text: HasRepr) -> str:
        return f"\033[1;32m{text}\033[0m" if self.ansi else text

    def number(self, num: HasRepr) -> str:
        return f"\033[35m{num}\033[0m" if self.ansi else num

    def error(self, text: HasRepr) -> str:
        return f"\033[31m{text}\033[0m" if self.ansi else text

    def string(self, text: HasRepr) -> str:
        return f"\033[33m{text}\033[0m" if self.ansi else text
