# kodakan

Personal photo archive at [pics.stimmie.dev](https://pics.stimmie.dev). An unedited gallery of wherever the camera pointed: street corners, breakfasts, ruins, friends, and everything in between.

## How it works

- `build.py` reads the original photos (JPEG, PNG, WebP, HEIF), fixes EXIF orientation, and writes two WebP renditions per photo into `dist/i/` (640px thumbnails and 1600px full views), plus `dist/manifest.json` with dimensions, dominant color, and date.
- `dist/index.html` is a single static page: month-grouped masonry grid, year navigation, and a keyboard/swipe lightbox. No framework, no build step.
- Deployed on Vercel as a static site (`outputDirectory: dist`).

## Rebuilding

```bash
python3 -m pip install pillow pillow-heif
python3 build.py   # reads originals from the parent directory
```
