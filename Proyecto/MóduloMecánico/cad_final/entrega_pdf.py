"""Markdown -> PDF for the team deliverable (docs/LANTERNGUARD_ENTREGA.md -> docs/LANTERNGUARD_ENTREGA.pdf).

    python entrega_pdf.py [docs/LANTERNGUARD_ENTREGA.md]

The Markdown (tables, images with paths relative to the .md) becomes one HTML page with print CSS (A4, 15 mm margins)
and Microsoft Edge prints it headless (--print-to-pdf) with a throwaway profile, so the user's Edge is not touched.
EDGE_EXE overrides the browser path.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

MOD = Path(__file__).resolve().parent.parent
EDGE = Path(os.environ.get("EDGE_EXE", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"))
CSS = """
@page { size: A4; margin: 15mm; }
body { font-family: "Segoe UI", Arial, sans-serif; font-size: 10pt; color: #1b1b1b; line-height: 1.38; }
h1 { font-size: 20pt; margin: 0 0 4pt; } h2 { font-size: 14pt; margin: 16pt 0 5pt; border-bottom: 1px solid #bbb; }
h3 { font-size: 11.5pt; margin: 11pt 0 4pt; }
table { border-collapse: collapse; width: 100%; margin: 5pt 0 9pt; font-size: 8.6pt; page-break-inside: avoid; }
th, td { border: 1px solid #c8c8c8; padding: 2.5pt 4pt; text-align: left; vertical-align: top; }
th { background: #eef2f5; }
img { max-width: 100%; page-break-inside: avoid; } p img { display: block; margin: 4pt auto; }
code { font-family: Consolas, monospace; font-size: 8.8pt; background: #f3f3f3; padding: 0 2pt; }
a { color: #0b5cad; word-break: break-all; }
.pb { page-break-before: always; }
"""


def main(md_path):
    md_path = Path(md_path).resolve()
    html = markdown.markdown(md_path.read_text(encoding="utf-8"), extensions=["tables", "sane_lists"])
    page = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><base href="{md_path.parent.as_uri()}/">'
            f"<style>{CSS}</style></head><body>{html}</body></html>")
    tmp = Path(tempfile.mkdtemp(prefix="entrega_"))
    src = tmp / "entrega.html"
    src.write_text(page, encoding="utf-8")
    out = md_path.with_suffix(".pdf")
    cmd = [str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={tmp / 'perfil'}", "--no-pdf-header-footer",
           f"--print-to-pdf={out}", src.as_uri()]
    subprocess.run(cmd, capture_output=True, timeout=180)
    if not out.exists():
        raise SystemExit("Edge no escribio el PDF")
    print("written", out, f"{out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else MOD / "docs" / "LANTERNGUARD_ENTREGA.md")
