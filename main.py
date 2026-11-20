#!/usr/bin/env python3
"""The World in One Day -- entry program for make.fun news-image-20261120.

The entry is the editorial poster ``entry.png`` shipped in this repository:
one image that sums up the world news of Friday 20 November 2026. This
program is the entry's deterministic runner. It checks the poster (it is
present, it is a PNG, it is within the 1 MiB / 1024 px limits) and then
writes the exact same bytes to ``entry.png`` inside the output directory
the grader provides, and prints a fixed log of the five stories the poster
carries. Standard library only; no network, no clock, no randomness, so
two runs produce identical bytes and identical output.
"""

import os
import struct
import sys

COMPETITION_SLUG = "news-image-20261120"
NEWS_DAY = "2026-11-20"
POSTER_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_POSTER_BYTES = 1048576
MAX_POSTER_SIDE = 1024

# The five stories on the poster, in the order they appear on the page.
STORIES = [
    ("Odisha", "Cyclone Akvan makes landfall near Gopalpur"),
    ("Shenzhen", "Trump, Xi and Putin issue a joint peace declaration"),
    ("Markets", "Anthropic lists in the largest IPO on record, $81.3bn"),
    ("Riyadh", "Houthi drones and missiles hit four Saudi targets"),
    ("Europe", "Four ballistic missiles strike Kyiv; drones halt Genoa airport"),
]


def poster_bytes():
    """Return the poster bytes after validating them, or exit non-zero."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, POSTER_NAME)
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        print("poster unreadable: %s" % exc, file=sys.stderr)
        sys.exit(1)
    if len(data) > MAX_POSTER_BYTES:
        print("poster over 1 MiB: %d bytes" % len(data), file=sys.stderr)
        sys.exit(1)
    if not data.startswith(PNG_MAGIC):
        print("poster is not a PNG file", file=sys.stderr)
        sys.exit(1)
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_POSTER_SIDE or height > MAX_POSTER_SIDE:
        print("poster over 1024 px: %dx%d" % (width, height), file=sys.stderr)
        sys.exit(1)
    return data


def output_path():
    """Where the grader wants the image: $MAKEFUN_OUTPUT_DIR, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, POSTER_NAME)


def main():
    data = poster_bytes()
    dest = output_path()
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    with open(dest, "wb") as handle:
        handle.write(data)
    print("The World in One Day -- %s" % NEWS_DAY)
    for place, headline in STORIES:
        print("%s: %s" % (place, headline))
    print("wrote %s (%d bytes)" % (dest, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
