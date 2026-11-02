"""Find freely licensed food photos on Wikimedia Commons."""
from __future__ import annotations

import io
import re
from html import unescape

import requests
from PIL import Image

from .models import RecipeImage

API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "RecipeGeneratorApp/1.0 (open-source Streamlit recipe app)"}
MAX_BYTES = 8_000_000
ALLOWED_LICENCES = ("cc0", "public domain", "pd", "cc by", "cc-by")
BLOCKED_WORDS = {"logo", "map", "diagram", "icon", "chart", "stamp", "drawing", "illustration", "cartoon", "poster"}


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()


def _words(text: str) -> set[str]:
    return {w.rstrip("s") for w in re.findall(r"[a-z]+", text.lower()) if len(w) > 2}


def _prepare(data: bytes) -> bytes:
    img = Image.open(io.BytesIO(data))
    img = img.convert("RGB")
    if min(img.size) < 300:
        raise ValueError("image too small")
    img.thumbnail((1400, 1400))
    out = io.BytesIO()
    img.save(out, "JPEG", quality=85, optimize=True)
    return out.getvalue()


def find_image(term: str, session=None) -> RecipeImage | None:
    """Return the first relevant, freely licensed photo, or None."""
    if not term.strip():
        return None
    http = session or requests
    wanted = _words(term)
    try:
        resp = http.get(API, headers=HEADERS, timeout=20, params={
            "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6, "gsrlimit": 12,
            "gsrsearch": f"{term} filetype:bitmap", "prop": "imageinfo",
            "iiprop": "url|mime|extmetadata", "iiurlwidth": 1200})
        resp.raise_for_status()
        pages = sorted((resp.json().get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 999))
    except (requests.RequestException, ValueError):
        return None
    for page in pages:
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata") or {}
        licence = _clean((meta.get("LicenseShortName") or {}).get("value", ""))
        title_words = _words(page.get("title", ""))
        searchable = title_words | _words(_clean((meta.get("ObjectName") or {}).get("value", "")))
        url = info.get("thumburl") or info.get("url", "")
        if (not licence.lower().startswith(ALLOWED_LICENCES) or title_words & BLOCKED_WORDS
                or not wanted <= searchable or info.get("mime") not in ("image/jpeg", "image/png", "image/webp")
                or not url.startswith("https://upload.wikimedia.org/")):
            continue
        try:
            img_resp = http.get(url, headers=HEADERS, timeout=30)
            img_resp.raise_for_status()
            if len(img_resp.content) > MAX_BYTES:
                continue
            data = _prepare(img_resp.content)
        except (requests.RequestException, OSError, ValueError):
            continue
        artist = _clean((meta.get("Artist") or {}).get("value", "")) or "Unknown author"
        return RecipeImage(data=data, label=term, credit=f"{artist[:90]}, {licence}, via Wikimedia Commons",
                           source_url=info.get("descriptionurl", url))
    return None


def find_recipe_images(dish: str, ingredients: list[str], session=None) -> list[RecipeImage]:
    """Return the dish photo first, when found, then up to 3 ingredient photos."""
    images = []
    for position, term in enumerate([dish, *ingredients[:3]]):
        image = find_image(term, session)
        if image:
            image.is_dish = position == 0
            images.append(image)
    return images
