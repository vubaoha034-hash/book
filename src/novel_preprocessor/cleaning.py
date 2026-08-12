"""Conservative, mechanical text cleanup for source preservation."""

from __future__ import annotations

import re


_ZERO_WIDTH = str.maketrans({
    "\ufeff": None,
    "\u200b": None,
    "\u200c": None,
    "\u200d": None,
    "\u2060": None,
    "\x00": None,
})


def normalize_text(text: str) -> str:
    """Remove only high-confidence mechanical noise.

    Punctuation, wording, paragraph order, full-width characters, and authorial
    language habits are deliberately left untouched.
    """

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\x0c", "\n")
    text = text.translate(_ZERO_WIDTH)
    text = text.replace("\u00a0", " ")
    text = "\n".join(line.rstrip(" \t") for line in text.split("\n"))
    text = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", text)
    return text.strip("\n")
