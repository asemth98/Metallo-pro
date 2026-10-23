#!/usr/bin/env python3
"""
يبني ملفاً واحداً مستقلاً MetalloPro_v6_single.html من index.html والملفات المرتبطة به.
الاستخدام:  python3 scripts/build.py
الناتج يعمل بدون أي ملفات خارجية، فيكفي رفعه وحده على GitHub Pages أو فتحه مباشرة.
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
html = (ROOT / "index.html").read_text(encoding="utf-8")

def inline_css(m):
    path = ROOT / m.group(1)
    return "<style>\n" + path.read_text(encoding="utf-8") + "\n</style>"

def inline_js(m):
    path = ROOT / m.group(1)
    code = path.read_text(encoding="utf-8")
    if "</script" in code.lower():
        sys.exit(f"ERROR: {path} contains '</script' and would break the bundle")
    return "<script>\n/* ---- " + m.group(1) + " ---- */\n" + code + "\n</script>"

html = re.sub(r'<link rel="stylesheet" href="([^"]+)">', inline_css, html)
html = re.sub(r'<script src="((?:js)/[^"]+)"></script>', inline_js, html)

out = ROOT / "MetalloPro_v6_single.html"
out.write_text(html, encoding="utf-8")
print(f"built {out.name}: {len(html.splitlines())} lines, {len(html.encode())//1024} KB")
