from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AnsiPrint(Enum):
    """Configure ANSI escape codes for Formatter#print() function."""

    ALWAYS = "always"
    """print() functions will always use ANSI escape codes, even when
    not printing to a TTY (e.g to a file)."""

    TTY_ONLY = "tty_only"
    """print() functions will use ANSI escape codes only when printing
    to a TTY (e.g. terminal). This is the default behavior."""

    NEVER = "never"
    """print() functions will never output any ANSI escape codes."""

@dataclass
class Config:
    """Typesum formatter configuration."""

    ansi_print: AnsiPrint | str = AnsiPrint.TTY_ONLY
    """Use ANSI escape codes for Formatter#print() function?"""

    ansi_format: bool = False
    """Use ANSI escape codes for Formatter#format() function?"""

    max_length: int = 130
    """Maximum string length. This is bypassed by forced expands."""
