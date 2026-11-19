#!/usr/bin/env python3
"""Deliver the Daily Atlas front page for the 18 November 2026 edition.

The finished artwork lives beside this script as ``entry.png``.  When the
grader runs this file, the picture is validated and then placed, byte for
byte, at ``/output/entry.png`` where the judging pipeline expects it.
"""

import shutil
import sys
from pathlib import Path

# Every PNG file opens with these eight bytes; anything else is not the
# artwork we shipped and must not be handed to the grader.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

OUTPUT_FOLDER = Path("/output")
OUTPUT_NAME = "entry.png"


def find_artwork() -> Path:
    """Return the path of the image stored next to this script."""
    artwork = Path(__file__).resolve().parent / "entry.png"
    if not artwork.is_file():
        raise SystemExit(
            f"cannot continue: the image file is missing ({artwork})"
        )
    return artwork


def confirm_png_format(artwork: Path) -> None:
    """Refuse to publish anything whose header is not a PNG header."""
    with artwork.open("rb") as stream:
        opening = stream.read(len(PNG_SIGNATURE))
    if opening != PNG_SIGNATURE:
        raise SystemExit(
            f"cannot continue: {artwork.name} fails the PNG signature test"
        )


def deliver(artwork: Path) -> Path:
    """Copy the artwork into the output folder and return its new path."""
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT_FOLDER / OUTPUT_NAME
    shutil.copyfile(artwork, destination)
    return destination


def announce_delivery(destination: Path) -> None:
    """Print a one-line receipt for the copy that was just published.

    The receipt states the delivered file's size in bytes together with
    its SHA-256 digest, so a human (or a log scraper) can confirm at a
    glance that the bytes in /output are exactly the bytes that shipped.
    """
    import hashlib

    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    print(
        f"delivered {destination}: "
        f"{destination.stat().st_size} bytes, sha256 {digest}"
    )


def run() -> int:
    artwork = find_artwork()
    confirm_png_format(artwork)
    destination = deliver(artwork)
    announce_delivery(destination)
    return 0


if __name__ == "__main__":
    sys.exit(run())
