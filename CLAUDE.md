# Lupa Album Studio

## Workflow Rules
- Never upload raw photos to Lupa before completing the 4-stage editorial review (Flavor Interview -> EXIF & Geocoding -> Unknowns Clarification -> Vision Hero Curation).
- Always generate 512px thumbnails via `scripts/make_thumbs.py` into `<album_dir>/.work/thumbs/` before visually inspecting photos. Never inspect full-resolution photos directly in context.
- Handle `.heic` / `.heif` files natively via `pillow-heif` (Lupa MCP accepts JPG, PNG, WebP, HEIC, HEIF, AVIF up to 15 MB per file).

## Lupa Platform Constraints
- Album names must be 2–28 characters.
- Mini Lupa caps at 144 photos; Regular photo books allow custom size, density, reading direction (RTL for Hebrew, LTR for English), and theme.
- Always pause and ask for explicit confirmation before calling `finish_album`.

## Layout
- `albums/<name>/raw/` — original photos (gitignored)
- `albums/<name>/.work/` — thumbnails, manifest cache (gitignored)
- `albums/<name>/captions.md` — final captions and hero notes (committed)
- Run scripts with `uv run` or inside `.venv` (see `pyproject.toml`).
