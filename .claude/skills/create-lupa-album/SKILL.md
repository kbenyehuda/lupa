---
name: create-lupa-album
description: Curate a local photo folder, extract EXIF locations, interview the user on album flavor, select hero shots, and generate a Lupa photo book via MCP.
---

When invoked on a target folder `<album_dir>` (photos live in `<album_dir>/raw`):

1. **Flavor Interview:** Ask 3–4 concise questions about book vibe (family journal vs. editorial gallery), language/direction (Hebrew RTL vs. English LTR), caption tone (warm/funny vs. minimalist), and photo density. Wait for user answers.
2. **Metadata & Geocoding:** Run `python scripts/extract_metadata.py <album_dir>/raw --out <album_dir>/.work/manifest.json` to extract timestamps, reverse-geocode GPS coordinates, and group photos into chronological chapters.
3. **Clarify Unknowns:** Present any clusters missing GPS tags or with ambiguous venues and ask the user to identify them. Update `manifest.json`.
4. **Vision Curation & Hero Picks:** Run `python scripts/make_thumbs.py <album_dir>/raw --out <album_dir>/.work/thumbs`. Inspect thumbnails to drop blurry/duplicate shots, flag top **Hero** shots for full-bleed spreads, and output a chapter-by-chapter proposal with draft captions.
5. **Push to Lupa:** After user approval, call Lupa MCP (`start_album`, upload curated full-res files, configure title/format/direction/theme, and `finish_album`). Confirm explicitly before `finish_album`. Save final page-by-page captions and hero-shot notes to `<album_dir>/captions.md`.
