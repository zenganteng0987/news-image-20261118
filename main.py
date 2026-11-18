"""Publish THE DAILY ATLAS for Wednesday 18 November 2026.

The image bundled with this entry (``entry.png``) is a one-page summary of
the world news of Wednesday 18 November 2026. It was composed
programmatically with PIL from that day's wire reports: 32 verified
Wednesday stories arranged as 15 illustrated cards, a BY THE NUMBERS
strip, and a dotted world map with a pin for every story.

This program simply publishes the composed page: it copies ``entry.png``
from the directory containing this file to ``/output/entry.png``, where
the competition harness expects to find it. The copy is a plain byte
copy, so running the program any number of times always produces a
byte-identical result.

Python 3.13, standard library only, no network access.
"""

import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DESTINATION = Path("/output/entry.png")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def check_source() -> None:
    """Fail early with a clear message if the bundled page is unusable."""
    if not SOURCE.is_file():
        raise SystemExit(f"error: bundled image not found: {SOURCE}")
    with SOURCE.open("rb") as handle:
        signature = handle.read(len(PNG_SIGNATURE))
    if signature != PNG_SIGNATURE:
        raise SystemExit(f"error: bundled image is not a PNG file: {SOURCE}")


def main() -> int:
    check_source()
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DESTINATION)
    print(f"Published {SOURCE.name} -> {DESTINATION} ({DESTINATION.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
