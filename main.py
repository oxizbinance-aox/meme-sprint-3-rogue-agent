#!/usr/bin/env python3
"""Meme Sprint 3 entrypoint: write the meme image to the output directory.

The image (entry.png, built by build_meme.py) is bundled in this repo. This
program copies it byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.png (default
/output/entry.png). Deterministic: two runs write identical bytes.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    src = HERE / "entry.png"
    if not src.is_file():
        # Fallback: the grader may run with the bot dir advertised instead.
        bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
        alt = Path(bot_dir) / "entry.png" if bot_dir else None
        if alt is not None and alt.is_file():
            src = alt
        else:
            print(f"entry.png missing next to main.py (looked in: {src}"
                  + (f", {alt}" if alt is not None else "") + ")",
                  file=sys.stderr)
            return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    if dst.stat().st_size != src.stat().st_size:
        print("copy size mismatch", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({dst.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
