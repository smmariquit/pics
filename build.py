#!/usr/bin/env python3
"""Build script: optimize photos into dist/ and emit manifest.json.

Sources: image files in parent dir (../*.jpg|jpeg|png|webp|heif|heic).
Outputs: dist/i/t/<name>.webp (thumb 640w), dist/i/f/<name>.webp (large 1600w),
dist/manifest.json with [{id, w, h, color, date}] sorted newest-first.
"""
import json, re, sys
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()

SRC = Path(__file__).resolve().parent.parent
DIST = Path(__file__).resolve().parent / "dist"
THUMB_W, FULL_W = 640, 1600
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heif", ".heic"}

def file_date(p: Path, img) -> str | None:
    # EXIF DateTimeOriginal first
    try:
        exif = img.getexif()
        dt = exif.get(36867) or exif.get(306)
        if dt:
            return datetime.strptime(str(dt)[:19], "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d")
    except Exception:
        pass
    m = re.search(r"(20\d{2})[-_]?(\d{2})[-_]?(\d{2})", p.stem)
    if m:
        y, mo, d = m.groups()
        if 1 <= int(mo) <= 12 and 1 <= int(d) <= 31:
            return f"{y}-{mo}-{d}"
    m = re.search(r"_(1[5-9]\d{11})", p.stem)  # ms epoch (FB_IMG)
    if m:
        return datetime.fromtimestamp(int(m.group(1)) / 1000).strftime("%Y-%m-%d")
    return None

def dominant(img) -> str:
    small = img.convert("RGB").resize((1, 1), Image.LANCZOS)
    r, g, b = small.getpixel((0, 0))
    return f"#{r:02x}{g:02x}{b:02x}"

def main():
    (DIST / "i" / "t").mkdir(parents=True, exist_ok=True)
    (DIST / "i" / "f").mkdir(parents=True, exist_ok=True)
    items, seen = [], set()
    files = sorted(p for p in SRC.iterdir() if p.suffix.lower() in EXTS)
    for n, p in enumerate(files):
        pid = re.sub(r"[^a-zA-Z0-9]+", "-", p.stem).strip("-").lower()
        if pid in seen:
            pid += f"-{n}"
        seen.add(pid)
        try:
            img = Image.open(p)
            img = ImageOps.exif_transpose(img)
            date = file_date(p, img)
            img = img.convert("RGB")
            w, h = img.size
            for width, sub, q in ((THUMB_W, "t", 72), (FULL_W, "f", 82)):
                out = DIST / "i" / sub / f"{pid}.webp"
                if not out.exists():
                    r = img.copy()
                    if r.width > width:
                        r.thumbnail((width, width * 4), Image.LANCZOS)
                    r.save(out, "WEBP", quality=q, method=4)
            items.append({"id": pid, "w": w, "h": h, "color": dominant(img), "date": date})
            print(f"[{n+1}/{len(files)}] {p.name} ok", flush=True)
        except Exception as e:
            print(f"[{n+1}/{len(files)}] {p.name} FAILED: {e}", flush=True)
    items.sort(key=lambda i: (i["date"] or "0000", i["id"]), reverse=True)
    (DIST / "manifest.json").write_text(json.dumps(items, separators=(",", ":")))
    print(f"done: {len(items)} images")

if __name__ == "__main__":
    sys.exit(main())
