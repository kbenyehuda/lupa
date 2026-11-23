#!/usr/bin/env python3
"""Extract EXIF time/GPS from photos, reverse-geocode, and group into day chapters."""
import argparse
import json
import time
from datetime import datetime
from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".avif"}
GPS_IFD = 0x8825
EXIF_IFD = 0x8769


def _deg(vals, ref) -> float:
    d, m, s = (float(v) for v in vals)
    out = d + m / 60 + s / 3600
    return -out if ref in ("S", "W") else out


def read_exif(path: Path) -> dict:
    info = {"file": path.name, "taken": None, "lat": None, "lon": None}
    try:
        with Image.open(path) as im:
            exif = im.getexif()
            ifd = exif.get_ifd(EXIF_IFD)
            raw = ifd.get(0x9003) or exif.get(0x0132)  # DateTimeOriginal / DateTime
            if raw:
                info["taken"] = datetime.strptime(str(raw), "%Y:%m:%d %H:%M:%S").isoformat()
            gps = exif.get_ifd(GPS_IFD)
            if gps.get(2) and gps.get(4):
                info["lat"] = _deg(gps[2], gps.get(1))
                info["lon"] = _deg(gps[4], gps.get(3))
    except Exception as e:
        info["error"] = str(e)
    return info


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--no-geocode", action="store_true")
    ap.add_argument("--lang", default="en")
    args = ap.parse_args()

    photos = [read_exif(p) for p in sorted(args.src.rglob("*")) if p.suffix.lower() in EXTS]
    photos.sort(key=lambda x: (x["taken"] is None, x["taken"] or x["file"]))

    geocode = None
    if not args.no_geocode:
        from geopy.geocoders import Nominatim

        geo = Nominatim(user_agent="lupa-album-studio")
        cache: dict = {}

        def geocode(lat, lon):
            key = (round(lat, 3), round(lon, 3))  # ~100m cell
            if key not in cache:
                try:
                    loc = geo.reverse((lat, lon), language=args.lang, zoom=16)
                    cache[key] = loc.address if loc else None
                except Exception:
                    cache[key] = None
                time.sleep(1.1)  # Nominatim usage policy: 1 req/sec
            return cache[key]

    chapters: dict[str, list] = {}
    for p in photos:
        if geocode and p["lat"] is not None:
            p["place"] = geocode(p["lat"], p["lon"])
        day = p["taken"][:10] if p["taken"] else "unknown"
        chapters.setdefault(day, []).append(p)

    manifest = {
        "total": len(photos),
        "missing_gps": [p["file"] for p in photos if p["lat"] is None],
        "missing_time": [p["file"] for p in photos if p["taken"] is None],
        "chapters": [{"day": d, "photos": ps} for d, ps in chapters.items()],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(photos)} photos, {len(chapters)} chapters -> {args.out}")


if __name__ == "__main__":
    main()
