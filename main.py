#!/usr/bin/env python3
"""Entry point for the news-image-20261125 bounty.

Copies the pre-rendered entry.png (next to this file) to
/output/entry.png byte-for-byte, prints its sha256, exits 0.
Standard library only. No network, no randomness, no timestamps.
"""
import hashlib
import shutil
from pathlib import Path


def main():
    # Locate entry.png next to this file, never via the working directory,
    # so the grader can run this from anywhere with a read-only source dir.
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        raise SystemExit("entry.png not found next to main.py")
    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    digest = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
