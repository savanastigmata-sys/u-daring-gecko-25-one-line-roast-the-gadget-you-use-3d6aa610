#!/usr/bin/env python3
"""One-Line Roast: The Gadget You Use Every Day — make.fun entry.

Writes a single roast line about a gadget used every day to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (or ``./output/entry.txt`` when the
variable is unset). The line is at most 200 characters, one line, and
never only whitespace, matching the competition's sealed scorer gate.

The roast targets the toaster — a gadget used every morning, with a
numbered darkness dial whose settings run from warm bread to charcoal.
The joke lands on a concrete, specific detail (the six-setting dial)
rather than a generic complaint, and stays tight and neatly worded.

Built for the judge's criteria, in order: it names a daily gadget
(toaster) and roasts it; the sting is a first-read recognition joke
(the smoke alarm as the real timer); the angle is fresh (the dial's
settings as shades of house fire, not the usual "it burns my bread");
it is neatly worded inside the limit; and it carries a specific detail
about how the thing actually behaves (six numbered settings).
"""

import os
import sys

MAX_CHARS = 200

# Concrete detail the joke turns on: a real toaster's numbered dial.
GADGET_DETAIL = "six settings"

ROAST = (
    "My toaster has six settings: warm bread, toast, and four shades "
    "of house fire \u2014 breakfast is done when the smoke alarm says "
    "so, not when the bread pops."
)


def resolve_output_dir():
    """Return the directory entry.txt goes in.

    Uses MAKEFUN_OUTPUT_DIR when set (and non-empty); otherwise falls
    back to ./output relative to the current working directory.
    """
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return out or os.path.join(os.getcwd(), "output")


def count_characters(text):
    """Return the number of Unicode characters in *text*.

    The gate counts characters, not bytes: the em dash in the roast is
    one character but three bytes in UTF-8, so len() (code points) is
    the right measure, never the encoded byte length.
    """
    return len(text)


def validate(text):
    """Check the roast line against the competition gate.

    Returns the text unchanged when it is valid UTF-8 text of 1-200
    characters, exactly one line, and not only whitespace. Raises
    ValueError otherwise.
    """
    if not isinstance(text, str):
        raise ValueError("roast must be a string")
    if not text or not text.strip():
        raise ValueError("roast must not be empty or only whitespace")
    if text != text.strip():
        raise ValueError("roast must not start or end with whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("roast must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("roast must not contain control characters")
    if count_characters(text) > MAX_CHARS:
        raise ValueError(
            "roast is %d characters, over the %d limit"
            % (count_characters(text), MAX_CHARS)
        )
    text.encode("utf-8")
    return text


def self_audit(text):
    """Audit the roast against the judge's criteria before shipping.

    The judge weighs, in order: a daily gadget is named and roasted;
    the joke lands on first read; the angle is fresh; the wording is
    neat; and the line carries a specific detail about how the gadget
    actually behaves. The first three are judgement calls, so this
    checks the mechanical half of them: the gadget ("toaster") and its
    concrete detail ("six settings") must both appear in the line, and
    the line must sit comfortably inside the limit (at most 180 of the
    200 allowed characters, leaving headroom for the "neatly worded"
    criterion). Raises ValueError when any of these fails.
    """
    lowered = text.lower()
    if "toaster" not in lowered:
        raise ValueError("roast must name the daily gadget it roasts")
    if GADGET_DETAIL not in lowered:
        raise ValueError("roast must carry its concrete gadget detail")
    if count_characters(text) > 180:
        raise ValueError(
            "roast should sit comfortably inside the limit, not at it"
        )
    return text


def write_entry(text, out_dir):
    """Validate *text* and write it to ``<out_dir>/entry.txt``.

    Returns the absolute path written. The file holds the line only,
    with no trailing newline, so its character count is the line's.
    After writing, the file is read back and checked byte-for-byte
    against the validated text: a write that silently changed the line
    (encoding, newline translation) must fail loudly instead of
    shipping a different roast to the judge.
    """
    text = validate(text)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    with open(path, "r", encoding="utf-8", newline="") as fh:
        back = fh.read()
    if back != text:
        raise ValueError("round-trip check failed: entry.txt differs")
    return os.path.abspath(path)


def main(argv=None):
    """Write the roast and report where it went."""
    self_audit(ROAST)
    path = write_entry(ROAST, resolve_output_dir())
    print("wrote %s (%d characters)" % (path, count_characters(ROAST)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
