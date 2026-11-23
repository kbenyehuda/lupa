#!/usr/bin/env python3
"""Generate small JPEG thumbnails for visual review."""
import argparse
from pathlib import Path

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".avif"}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src", type=Path, help="folder of original photos")
    ap.add_argument("--out", type=Path, required=True, help="thumbnail output folder")
    ap.add_argument("--size", type=int, default=512, help="max edge in px")
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in args.src.rglob("*") if p.suffix.lower() in EXTS)
    for p in files:
        dest = args.out / (p.stem + ".jpg")
        try:
            with Image.open(p) as im:
                im = ImageOps.exif_transpose(im).convert("RGB")
                im.thumbnail((args.size, args.size))
                im.save(dest, "JPEG", quality=80)
        except Exception as e:  # keep going on bad files
            print(f"skip {p.name}: {e}")
    print(f"wrote {len(files)} thumbnails to {args.out}")


if __name__ == "__main__":
    main()
