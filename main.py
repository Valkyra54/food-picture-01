"""food-picture-01 entry: copy the shipped ramen photograph to the output dir.

The image is a photorealistic tonkotsu ramen picture (entry.png, JPEG bytes
under that name, 1024x1024). This program only copies it, so both runs
produce byte-identical output. Standard library only, no network.
"""

import os
import shutil
import sys


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Guard the byte-identical-runs requirement: the copy must be exact.
    if os.path.getsize(dst) != os.path.getsize(src):
        raise RuntimeError("copied entry.png size does not match source")
    return 0


if __name__ == "__main__":
    sys.exit(main())
