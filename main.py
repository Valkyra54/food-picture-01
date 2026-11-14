"""Food-picture-01 v3: copy the bundled ramen photograph to the output folder.

The bundled asset is a 1024x1024 JPEG stored next to this script as entry.png.
The program copies it byte-for-byte into the output directory and then checks
that the copy is identical, so the graded artifact is exactly the image we
reviewed in the lab.

The digest comparison is the copy guard: it catches a truncated or corrupted
write before the run can report success, instead of silently shipping a
damaged image.
"""

import hashlib
import os
import sys
from pathlib import Path

ASSET_NAME = "entry.png"


def resolve_target_dir() -> Path:
    """Where the graded entry.png must land.

    Defaults to the absolute /output directory; MAKEFUN_OUTPUT_DIR overrides
    it when set (and non-empty).
    """
    override = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if override:
        return Path(override)
    return Path("/output")


def expected_digest(asset: Path) -> str:
    """SHA-256 of the bundled image, computed from the asset itself."""
    return hashlib.sha256(asset.read_bytes()).hexdigest()


def publish_image(asset: Path, target_dir: Path) -> Path:
    """Write the asset's exact bytes to target_dir/entry.png and verify."""
    target_dir.mkdir(parents=True, exist_ok=True)
    blob = asset.read_bytes()
    target = target_dir / ASSET_NAME
    target.write_bytes(blob)
    written = hashlib.sha256(target.read_bytes()).hexdigest()
    if written != hashlib.sha256(blob).hexdigest():
        raise SystemExit(
            f"copy check failed: {target} digest {written} "
            "does not match the bundled image"
        )
    return target


def run() -> int:
    script_dir = Path(__file__).resolve().parent
    asset = script_dir / ASSET_NAME
    if not asset.is_file():
        print(f"bundled image missing: {asset}", file=sys.stderr)
        return 1
    digest = expected_digest(asset)
    target = publish_image(asset, resolve_target_dir())
    print(f"wrote {target} ({target.stat().st_size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
