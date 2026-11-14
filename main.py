"""food-picture-01 v2: deliver the finished ramen photograph to the output folder.

The shipped file is a 1024x1024 photorealistic tonkotsu ramen image stored as
JPEG bytes under the name entry.png -- tall glossy noodle pull, a prominent
upright sheet of nori, curling steam, a deep-orange molten jammy yolk, a
charred chashu fan and bold chili-oil swirls over creamy broth. The program
does nothing but place an exact copy of that file in the output directory,
so repeated runs always yield identical bytes. It uses only the standard
library and makes no network calls.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


def resolve_output_dir() -> Path:
    """Return the directory the copy goes to.

    The sandbox default is the absolute path /output. MAKEFUN_OUTPUT_DIR
    may point somewhere else when the program is run in a scratch folder.
    """
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    target = Path(override) if override else Path("/output")
    target.mkdir(parents=True, exist_ok=True)
    return target


def verify_copy(source: Path, target: Path) -> None:
    """Raise unless the copied file is a byte-for-byte match of the source."""
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    target_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    if source_hash != target_hash:
        raise RuntimeError("copied entry.png differs from the source file")


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    picture = script_dir / "entry.png"
    destination = resolve_output_dir() / "entry.png"
    # Copy first, then hash both files: the guard only passes on an exact copy.
    shutil.copyfile(picture, destination)
    verify_copy(picture, destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
