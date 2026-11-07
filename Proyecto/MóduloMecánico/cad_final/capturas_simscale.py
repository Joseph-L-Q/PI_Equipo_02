"""Captures of the PUBLIC page of a SimScale project (no login, no API download): docs/ENCARGO_SIMSCALE_2026-11-07.md §2.

    python capturas_simscale.py <pid> <out_dir> [--titulo "Von Mises"]

1. /api/v3/projects/<pid>/ (anonymous, public projects) gives ownerName + publicProjectName -> the public page URL.
2. Playwright opens it at 1920 x 1080; every result card of the page is a post-processing model (CUG). For each one it clicks
   the card, waits for the model, switches the viewer to full screen and saves a 1920 x 1080 PNG.
3. The CUG modelInfo of each card (fetched by the page itself) carries the legend title and the exact min/max of the field:
   saved to <out_dir>/vistas.json. That is where sigma max comes from.
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (LanternGuard report)"}


def public_url(pid):
    req = urllib.request.Request(f"https://www.simscale.com/api/v3/projects/{pid}/", headers=UA)
    d = json.loads(urllib.request.urlopen(req, timeout=60).read().decode("utf-8"))
    return f"https://www.simscale.com/projects/{d['ownerName']}/{d['publicProjectName']}/", d


def capture(pid, out_dir, wait_s=45, rot=(200, 150)):
    from playwright.sync_api import sync_playwright
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    url, meta = public_url(pid)
    infos = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080})

        def on_resp(r):
            if r.url.endswith("/data/modelInfo"):
                try:
                    infos.append(dict(cug=r.url.split("/models/")[1].split("/")[0], info=json.loads(r.text())))
                except Exception:          # noqa: BLE001
                    pass
        pg.on("response", on_resp)
        pg.goto(url, wait_until="domcontentloaded", timeout=180000)
        time.sleep(wait_s)
        for sel in ("button[aria-label='Close this consent banner']",):
            try:
                pg.click(sel, timeout=2000)
            except Exception:              # noqa: BLE001
                pass
        pg.screenshot(path=str(out / "00_pagina_publica.png"))
        shots = []
        n_cards = len(pg.query_selector_all("text=3D"))
        for k in range(n_cards):
            chip = pg.query_selector_all("text=3D")[k].bounding_box()
            n0 = len(infos)
            pg.mouse.click(chip["x"] - 50, chip["y"] + 45)          # the thumbnail, left of its "3D" chip
            t0 = time.time()
            while len(infos) == n0 and time.time() - t0 < 60:
                time.sleep(1)
            time.sleep(20)
            cug = infos[-1]["cug"] if infos else None
            pg.mouse.click(1313, 297)                                # full screen (top right of the viewer)
            time.sleep(6)
            raw = out / f"vista_{k + 1:02d}_guardada.png"
            pg.screenshot(path=str(raw))
            pg.mouse.move(960, 540)                                  # turn the saved view into an ISO view from above
            pg.mouse.down()
            pg.mouse.move(960 - rot[0], 540, steps=25)
            pg.mouse.move(960 - rot[0], 540 + rot[1], steps=25)
            pg.mouse.up()
            time.sleep(5)
            iso = out / f"vista_{k + 1:02d}_iso.png"
            pg.screenshot(path=str(iso))
            pg.keyboard.press("Escape")
            time.sleep(3)
            shots.append(dict(guardada=raw.name, iso=iso.name, cug=cug))
        b.close()
    seen, views = set(), []
    for it in infos:
        if it["cug"] in seen:
            continue
        seen.add(it["cug"])
        mi = it["info"]
        leg = (mi.get("colorLegendArr") or [{}])[0]
        res = (mi.get("resultInfoArr") or [{}])[0]
        views.append(dict(cug=it["cug"], titulo=leg.get("title"), campo=res.get("idString"), minimo=res.get("minimumValue"),
                          maximo=res.get("maximumValue"), partes=[q.get("name") for q in mi.get("partInfoArr", [])],
                          bbox=mi.get("boundingBox")))
    rep = dict(pid=str(pid), url=url, owner=meta.get("ownerName"), nombre=meta.get("projectName"), vistas=views, capturas=shots)
    (out / "vistas.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return rep


if __name__ == "__main__":
    rot = tuple(int(v) for v in sys.argv[3].split(",")) if len(sys.argv) > 3 else (200, 150)
    r = capture(sys.argv[1], sys.argv[2], rot=rot)
    print(r["url"])
    for v in r["vistas"]:
        print(v["cug"], v["titulo"], v["minimo"], v["maximo"])
    print(r["capturas"])
