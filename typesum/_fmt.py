"""Format utils."""

import typing

HasRepr = typing.Any
Formattable = typing.Any

enable_fmt = True


def type_(text: HasRepr) -> str:
    return f"\033[1;32m{text}\033[0m" if enable_fmt else text


def number(num: HasRepr) -> str:
    return f"\033[35m{num}\033[0m" if enable_fmt else num


def error(text: HasRepr) -> str:
    return f"\033[31m{text}\033[0m" if enable_fmt else text


def string(text: HasRepr) -> str:
    return f"\033[33m{text}\033[0m" if enable_fmt else text
