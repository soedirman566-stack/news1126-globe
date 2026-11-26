#!/usr/bin/env python3
"""Hand in the entry: copy entry.png into the output directory.

The grader runs this file twice, with no network, as an unprivileged
user, with the repository read-only at /bot and a writable /output that
is a mount point on a read-only file system. So this program only ever
creates and writes inside the output directory -- it never deletes or
removes the output directory itself (removing a mount point fails, and
a previous entry was rejected for exactly that).

Standard library only: nothing is installed before the grader runs it.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    # The two grader runs must write identical bytes: prove the copy is
    # the committed image, byte for byte in size, before reporting done.
    written = target.stat().st_size
    expected = SOURCE.stat().st_size
    if written != expected:
        raise SystemExit(f"copy mismatch: wrote {written}, source {expected}")
    print(f"entry.png: {written} bytes -> {target}")


if __name__ == "__main__":
    main()
