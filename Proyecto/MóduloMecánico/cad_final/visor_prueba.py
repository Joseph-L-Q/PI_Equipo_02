"""Headless check of the 3D manual (system Python with Playwright; chromium installed):

    python visor_prueba.py

Serves docs/visor with `python -m http.server` on a free port (stopped through the handle it returned, never by name), opens
index.html (desktop 1366x800 and phone 390x844) and the single file by file://, clicks every tab, saves screenshots in
salida/_tmp/visor_capturas/ and fails on any console error or page error. Prints the load times.
"""
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

MOD = Path(__file__).resolve().parent.parent
DIR = MOD / "docs" / "visor"
CAP = MOD / "salida" / "_tmp" / "visor_capturas"
TABS = ["piezas", "juntas", "ensamble", "impresion", "pruebas", "resultados"]
VIEWS = {"desktop": dict(width=1366, height=800), "movil": dict(width=390, height=844)}


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def run_page(pw, url, tag, errors, times):
    for vname, vp in VIEWS.items():
        b = pw.chromium.launch(args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        ctx = b.new_context(viewport=vp, has_touch=vname == "movil", is_mobile=vname == "movil", device_scale_factor=1)
        pg = ctx.new_page()
        pg.on("console", lambda m, t=f"{tag}/{vname}": errors.append(f"[{t}] console.{m.type}: {m.text}") if m.type in ("error",) else None)
        pg.on("pageerror", lambda e, t=f"{tag}/{vname}": errors.append(f"[{t}] pageerror: {e}"))
        pg.on("requestfailed", lambda r, t=f"{tag}/{vname}": errors.append(f"[{t}] requestfailed: {r.url}"))
        t0 = time.time()
        pg.goto(url, wait_until="load")
        pg.wait_for_function("window.__lg && window.__lg.loadMs !== null", timeout=30000)
        dt = time.time() - t0
        times[f"{tag}/{vname}"] = (round(dt, 2), pg.evaluate("window.__lg.loadMs"))
        pg.wait_for_timeout(600)
        for t in TABS:
            pg.evaluate(f"window.__lg.goTab('{t}')")
            if t == "juntas":
                pg.evaluate("window.__lg.openSeal(1)")
            if t == "ensamble":
                pg.evaluate("window.__lg.goStep(4)")
            if t == "resultados":
                pg.click("[data-act=case]")
            pg.wait_for_timeout(1300)
            pg.screenshot(path=str(CAP / f"{tag}_{vname}_{t}.png"))
        pg.evaluate("window.__lg.goTab('piezas'); window.__lg.select('M1s_caja_cuerpo', true)")
        pg.wait_for_timeout(1300)
        pg.screenshot(path=str(CAP / f"{tag}_{vname}_ficha.png"))
        pg.evaluate("window.__lg.setTheme('dark')")
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(CAP / f"{tag}_{vname}_oscuro.png"))
        b.close()


def main():
    CAP.mkdir(parents=True, exist_ok=True)
    port = free_port()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", str(DIR)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    errors, times = [], {}
    try:
        time.sleep(1.0)
        with sync_playwright() as pw:
            run_page(pw, f"http://127.0.0.1:{port}/index.html", "http", errors, times)
            run_page(pw, (DIR / "LanternGuard_visor.html").as_uri(), "file", errors, times)
    finally:
        srv.terminate()
        srv.wait(timeout=10)
    print(json.dumps(times, indent=1))
    print("errores:", len(errors))
    for e in errors:
        print("  ", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
