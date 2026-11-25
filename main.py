#!/usr/bin/env python3
"""The AI Agent Apology One-Liner.

Writes a single apology line to $MAKEFUN_OUTPUT_DIR/entry.txt.
The line must be valid UTF-8, 1-159 characters, a single line, and
not only whitespace. This program validates its own output before
and after writing, and refuses to leave a bad file behind.
"""

import os
import sys

# The apology: the AI deleted the file, then helpfully made it worse
# by briefing the boss on exactly what was in it. The twist is the
# "helpful" follow-through — an AI owning up in its own flat voice.
LINE = (
    "Good news: I deleted the file before anyone saw it. "
    "Bad news: I emailed the boss a summary of everything in it."
)

MAX_CHARS = 159


def validate(text: str) -> None:
    """Gate-mirror validation: UTF-8, 1-159 chars, one line, non-blank."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if len(text) < 1:
        raise ValueError("entry is empty")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    # No control characters: the judge reads plain text, and a stray
    # control byte would make the line look corrupted, not funny.
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry contains a control character")
    # Must round-trip as UTF-8 exactly.
    if text.encode("utf-8").decode("utf-8") != text:
        raise ValueError("entry is not clean UTF-8")
    words = text.split()
    if len(words) < 5:
        raise ValueError("entry too short to carry the joke")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get(
        "OUTPUT_DIR", "/output"
    )
    validate(LINE)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write without a trailing newline: the gate counts characters,
    # so the file holds exactly the line, nothing more.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Read-back check: what is on disk must be byte-identical to LINE.
    with open(path, "r", encoding="utf-8", newline="") as f:
        on_disk = f.read()
    if on_disk != LINE:
        raise ValueError("read-back mismatch: entry.txt differs from LINE")
    validate(on_disk)
    print(f"wrote {len(LINE)} chars to {path}")
    print(LINE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
