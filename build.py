#!/usr/bin/env python3
"""Build the standalone site for GitHub Pages.

planner.html is the single source: it is published as-is to Claude, where the
viewer adds the document skeleton. This script wraps it in a full document for
GitHub Pages (docs/index.html) and turns on standalone mode with the Google
OAuth client ID from config.json.

    python3 build.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
src = (ROOT / "planner.html").read_text(encoding="utf-8")
config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))

# Everything up to the end of the first <style> block belongs in <head>.
cut = src.index("</style>") + len("</style>")
head, body = src[:cut], src[cut:]

site = {"clientId": config.get("googleClientId", "")}

doc = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#F2F2F3">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Планировщик">
<link rel="manifest" href="manifest.webmanifest">
<style>
:root {{ color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }}
body {{ margin: 0; }}
img {{ max-width: 100%; }}
[hidden] {{ display: none !important; }}
</style>
<script>window.PLANNER_SITE = {json.dumps(site)};</script>
{head}
</head>
<body>
{body}
</body>
</html>
"""

out = ROOT / "docs"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(doc, encoding="utf-8")
(out / ".nojekyll").write_text("", encoding="utf-8")
(out / "manifest.webmanifest").write_text(json.dumps({
    "name": "Мой планировщик",
    "short_name": "Планировщик",
    "start_url": "./",
    "display": "standalone",
    "background_color": "#F2F2F3",
    "theme_color": "#F2F2F3",
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"docs/index.html built ({len(doc) // 1024} KB), Google sign-in {'on' if site['clientId'] else 'not configured'}")
