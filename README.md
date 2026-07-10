# pics

Photo wall at [pics.stimmie.dev](https://pics.stimmie.dev). Just the pictures, full screen, in random order.

## How it works

- `build.py` reads the original photos (JPEG, PNG, WebP, HEIF), fixes EXIF orientation, and writes two WebP renditions per photo into `dist/i/` (640px thumbnails and 1600px full views), plus `dist/manifest.json` with dimensions and dominant color placeholders.
- `dist/index.html` is a single static page: full-bleed masonry grid shuffled on every load, with a keyboard/swipe lightbox. No framework, no build step.
- Deployed on Vercel as a static site (`outputDirectory: dist`).

## Rebuilding

```bash
python3 -m pip install pillow pillow-heif
python3 build.py   # reads originals from the parent directory
```
