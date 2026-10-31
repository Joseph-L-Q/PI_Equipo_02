"""Onshape drawings of every printed piece of P2 + PET buoy (4 x 1 L), in the document LG_IMPRIMIR_P2.

    python planos_onshape.py --documento            # creates LG_IMPRIMIR_P2 (once), folder, link sharing, 00_ENSAMBLE
    python planos_onshape.py --pieza M2_caja_tapa   # one piece: Part Studio tab, properties, Drawing, PDF
    python planos_onshape.py --todas                # every piece still missing in planos_onshape.json
    python planos_onshape.py --unir                 # cover + every PDF -> PLANOS_ONSHAPE_P2.pdf

Per piece: the STEP is imported as a Part Studio tab named with the code; the part gets Name = code, Material = PETG,
Project and Description = PROJECT. The Drawing is A3, first angle, mm, with 7 views laid out by this script (Onshape
places a view by the centre of its bounding box, in sheet mm), and only these dimensions: overall width and height
in the front view, width and depth in the top view, depth and height in the left view, and one diameter per hole size
and view ("n x" when there are several). Hole = concave cylinder closed to a full circle, found in the local STEP and
matched with the circles of the view geometry. A dimension whose text box would fall on another one, on a view, on the
title block or off the sheet is not created and is listed as "a mano" in planos_onshape.json.

The quantity is a note above the title block. Every call goes through onshape_sync.Client (call log and yearly
counter); the run stops before a piece if the year total passes LIMIT.
"""
import argparse
import json
import math
import sys
import time
import urllib.request
from pathlib import Path

import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.BRepGProp import BRepGProp_Face
from OCP.GeomAbs import GeomAbs_Cylinder
from OCP.gp import gp_Pnt, gp_Vec

import onshape_push as OP
import onshape_sync as OS

MOD = Path(__file__).resolve().parent.parent
OUT = MOD / "salida" / "planos_onshape"
REG = OUT / "planos_onshape.json"
DOC = "LG_IMPRIMIR_P2"
FOLDER = "bf32e5647856cd2677198b89"           # LanternGuard folder in Onshape
PROJECT = "LanternGuard – Equipo 02 UPCH"
LIMIT = 1500
P2 = MOD / "salida" / "prototipos" / "P2_robusto"
BOYA = MOD / "salida" / "boya_pet"
# printed pieces (M7 is acrylic): code, STEP, STL, quantity for one node + one buoy
PIECES = [(c, P2 / "step" / f"{c}.step", P2 / "stl" / f"{c}.stl", q) for c, q in (
    ("M1s_caja_cuerpo", 1), ("M2_caja_tapa", 1), ("M3s_riel_gancho", 2), ("M3t_tapa_bolsillo", 2),
    ("M4_capsula_cuerpo", 2), ("M5s_capsula_tapa_pie", 2), ("M6_capsula_bisel", 2), ("M11_bandeja", 1),
    ("M11_bandeja_sup", 1))] + [(c, BOYA / "step" / f"{c}.step", BOYA / "stl" / f"{c}.stl", q) for c, q in (
    ("B1_casco", 1), ("B2_cubierta", 1), ("B3_caja", 1), ("B4_tapa", 1), ("B5_cuna", 2), ("B6_correa", 4))]

# sheet (A3 landscape, mm): drawing frame and the standard Onshape title block measured on the first PDF
SHEET = (420.0, 297.0)
FRAME = (12.0, 12.0, 408.0, 285.0)
TITLE = (190.0, 0.0, 420.0, 64.0)
GAP = 14.0                                    # between views: room for one dimension line and its text
SCALES = [(2, 1), (1, 1), (1, 2), (2, 5), (1, 5), (1, 10)]          # 2:5 = 1:2.5
ISO_SCALES = [(2, 1), (1, 1), (2, 3), (1, 2), (2, 5), (1, 3), (1, 4), (1, 5), (1, 8), (1, 10)]
TEXT_H = 3.5
OFF = 7.0                                     # dimension text distance from the view box


def client():
    OS.API = OP.API_V6
    return OS.Client()


def reg():
    return OS.read_json(REG, {})


def save(r):
    OUT.mkdir(parents=True, exist_ok=True)
    REG.write_text(json.dumps(r, indent=1, ensure_ascii=False), encoding="utf-8")


def quota_ok():
    n = OS.year_total()
    if n > LIMIT:
        raise SystemExit(f"cupo: {n} llamadas en el año, por encima de {LIMIT}; paro aquí")
    return n


# ---------------------------------------------------------------- local geometry
def holes(step):
    """Concave cylinders that close a full circle: [(centre mm, axis, radius mm)] (one entry per hole)."""
    shape = cq.importers.importStep(str(step)).val()
    groups = {}
    for f in shape.Faces():
        s = BRepAdaptor_Surface(f.wrapped)
        if s.GetType() != GeomAbs_Cylinder:
            continue
        cyl = s.Cylinder()
        ax, loc, r = cyl.Axis().Direction(), cyl.Axis().Location(), cyl.Radius()
        u0, u1, v0, v1 = s.FirstUParameter(), s.LastUParameter(), s.FirstVParameter(), s.LastVParameter()
        p, n = gp_Pnt(), gp_Vec()
        BRepGProp_Face(f.wrapped).Normal((u0 + u1) / 2, (v0 + v1) / 2, p, n)
        a = cq.Vector(ax.X(), ax.Y(), ax.Z())
        c0 = cq.Vector(loc.X(), loc.Y(), loc.Z())
        pv = cq.Vector(p.X(), p.Y(), p.Z())
        foot = c0 + a * (pv - c0).dot(a)
        if cq.Vector(n.X(), n.Y(), n.Z()).dot(foot - pv) <= 0:        # normal away from the axis: a boss, not a hole
            continue
        if abs(a.x) + abs(a.y) + abs(a.z) - max(abs(a.x), abs(a.y), abs(a.z)) > 1e-6:
            continue                                                  # oblique axis: no view sees it as a circle
        k = max(range(3), key=lambda i: abs((a.x, a.y, a.z)[i]))
        c = [round(v, 2) for v in foot.toTuple()]
        c[k] = 0.0
        key = (k, tuple(c), round(r, 3))
        groups[key] = groups.get(key, 0.0) + abs(u1 - u0)
    return [((list(c)), k, r) for (k, c, r), span in groups.items() if span >= 2 * math.pi - 0.05]


def bbox(step):
    b = cq.importers.importStep(str(step)).val().BoundingBox()
    return (b.xmin, b.ymin, b.zmin), (b.xmax, b.ymax, b.zmax)


# ---------------------------------------------------------------- layout
def layout(lo, hi):
    """Scale and view centres (sheet mm). First angle: bottom view above the front, top view below it, the right
    view on the left of the front, the left view on its right, the back view at the far right."""
    W, D, H = (hi[i] - lo[i] for i in range(3))
    for num, den in SCALES:
        s = num / den
        cw = [s * D, s * W, s * D, s * W]                             # columns: right, front, left, back
        rh = [s * D, s * H, s * D]                                    # rows: top view, main row, bottom view
        x = [FRAME[0] + GAP]
        for i in range(1, 4):
            x.append(x[-1] + cw[i - 1] + GAP)
        y0 = max(FRAME[1] + GAP, TITLE[3] + 12 - GAP - rh[0])         # main row clear of the quantity note
        if x[1] + cw[1] > TITLE[0] - 4:                               # top view would reach the title block: lift it
            y0 = TITLE[3] + 4
        y = [y0, y0 + rh[0] + GAP, y0 + rh[0] + GAP + rh[1] + GAP]
        right, top = x[3] + cw[3], y[2] + rh[2]
        if right > FRAME[2] - 4 or top > FRAME[3] - 4:
            continue
        c = lambda i, j: (x[i] + cw[i] / 2, y[j] + rh[j] / 2)
        views = {"right": c(0, 1), "front": c(1, 1), "left": c(2, 1), "back": c(3, 1), "top": c(1, 0), "bottom": c(1, 2)}
        boxes = {k: (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2) for k, (cx, cy), (w, h) in (
            (k, views[k], wh) for k, wh in (("right", (cw[0], rh[1])), ("front", (cw[1], rh[1])), ("left", (cw[2], rh[1])),
                                            ("back", (cw[3], rh[1])), ("top", (cw[1], rh[0])), ("bottom", (cw[1], rh[2]))))}
        # isometric: free box above the left and back views, at this scale or smaller
        ix0, iy0, ix1, iy1 = x[2], y[1] + rh[1] + GAP, FRAME[2] - 4, FRAME[3] - 4
        iso_s = None
        for n2, d2 in ISO_SCALES:
            si = n2 / d2
            if si <= s and 0.71 * si * (W + D) <= ix1 - ix0 and si * (0.82 * H + 0.41 * (W + D)) <= iy1 - iy0:
                iso_s = (n2, d2)
                break
        if iso_s is None:                                             # below the title block row is full: use the corner
            continue
        si = iso_s[0] / iso_s[1]
        iw, ih = 0.71 * si * (W + D), si * (0.82 * H + 0.41 * (W + D))
        views["isometric"] = ((ix0 + ix1) / 2, (iy0 + iy1) / 2)
        boxes["isometric"] = ((ix0 + ix1 - iw) / 2, (iy0 + iy1 - ih) / 2, (ix0 + ix1 + iw) / 2, (iy0 + iy1 + ih) / 2)
        return (num, den), iso_s, views, boxes
    raise SystemExit("ninguna escala estandar entra en A3")


# ---------------------------------------------------------------- Onshape
def wait_modify(c, did, wid, eid, reqs, desc):
    r = c.call("POST", f"/drawings/d/{did}/w/{wid}/e/{eid}/modify", {"description": desc, "jsonRequests": reqs})
    for i in range(12):
        time.sleep(4 + 3 * i)
        s = c.call("GET", f"/drawings/modify/status/{r['id']}")
        if s.get("requestState") != "ACTIVE":
            return json.loads(s["output"]) if s.get("output") else s
    raise OS.OnshapeError(f"modify {desc} sigue ACTIVE")


def set_props(c, did, wid, eid, pid, code):
    """Name, Material (PETG), Project and Description of the part, by property name as Onshape reports them."""
    md = c.call("GET", f"/metadata/d/{did}/w/{wid}/e/{eid}/p/{pid}")
    ids = {p["name"]: p["propertyId"] for p in md.get("properties", [])}
    want = {"Name": code, "Description": PROJECT, "Project": PROJECT,
            "Material": {"displayName": "PETG", "id": "PETG", "libraryName": "LanternGuard",
                         "properties": [{"name": "Density", "type": "REAL", "units": "g/cm^3", "value": "1.27"}]}}
    props = [{"propertyId": ids[k], "value": v} for k, v in want.items() if k in ids]
    c.call("POST", f"/metadata/d/{did}/w/{wid}/e/{eid}/p/{pid}", {"properties": props})
    return sorted(k for k in want if k in ids)


def project(vm, p):
    """Model point (m) -> view (u, v) in mm, from the viewMatrix rows (sheet x and y axes in model space)."""
    return (1000 * (vm[0] * p[0] + vm[1] * p[1] + vm[2] * p[2]), 1000 * (vm[4] * p[0] + vm[5] * p[1] + vm[6] * p[2]))


def text_box(x, y, txt):
    w = 0.62 * TEXT_H * len(txt) + 2
    return (x - w / 2, y - TEXT_H / 2 - 1, x + w / 2, y + TEXT_H / 2 + 1)


def clash(b, others):
    return any(b[0] < o[2] and o[0] < b[2] and b[1] < o[3] and o[1] < b[3] for o in others)


def ref_pt(vid, uid, xyz, snap):
    return {"type": "Onshape::Reference::Point", "uniqueId": uid, "viewId": vid, "snapPointType": snap, "coordinate": list(xyz)}


def dims_for_view(name, vid, vm, geom, box, centre_uv, s, lo, hi, hole_list, taken, view_boxes):
    """Annotations for one view and the list of what was skipped."""
    out, skipped = [], []
    to_sheet = lambda uv: (box[0] + (box[2] - box[0]) / 2 + s * (uv[0] - centre_uv[0]),
                           box[1] + (box[3] - box[1]) / 2 + s * (uv[1] - centre_uv[1]))
    lines = []
    for e in geom:
        if e["type"] == "line" and e.get("visible", True):
            a = (1000 * e["data"]["start"][0], 1000 * e["data"]["start"][1])        # jsongeometry is in view space
            b = (1000 * e["data"]["end"][0], 1000 * e["data"]["end"][1])
            lines.append((e, a, b))
    pts = [p for _, a, b in lines for p in (a, b)]
    for e in geom:                                                    # circles and arcs reach the extremes too
        if e["type"] in ("circle", "arc") and "center" in e["data"]:
            cx0, cy0, r0 = 1000 * e["data"]["center"][0], 1000 * e["data"]["center"][1], 1000 * e["data"]["radius"]
            pts += [(cx0 - r0, cy0), (cx0 + r0, cy0), (cx0, cy0 - r0), (cx0, cy0 + r0)] if e["type"] == "circle" else                 [(1000 * e["data"][k][0], 1000 * e["data"][k][1]) for k in ("start", "end") if k in e["data"]]
    us = [p[0] for p in pts]
    vs = [p[1] for p in pts]
    wanted = {"front": ("u", "v"), "top": ("u", "v"), "left": ("u", "v")}.get(name, ())
    blocked = [TITLE] + [vb for k, vb in view_boxes.items()]
    for axis in wanted:
        k = 0 if axis == "u" else 1
        vals = us if k == 0 else vs
        if not vals:
            skipped.append(f"{name}: general {axis} (sin aristas rectas)")
            continue
        mn, mx = min(vals), max(vals)
        # extreme edges perpendicular to the axis, the longest at each side
        side = lambda target: max((ln for ln in lines if abs(ln[1][k] - target) < 0.05 and abs(ln[2][k] - target) < 0.05),
                                  key=lambda ln: abs(ln[1][1 - k] - ln[2][1 - k]), default=None)
        e1, e2 = side(mn), side(mx)
        if e1 is None or e2 is None or abs(mx - mn) < 0.5:
            skipped.append(f"{name}: {'ancho' if k == 0 else 'alto'} general {mx - mn:.1f} mm (el extremo es curvo)")
            continue
        txt = f"{mx - mn:.1f}".rstrip("0").rstrip(".")
        if k == 0:                                                    # width: above the view (below for the top view)
            ty = box[3] + OFF if name != "top" else box[1] - OFF
            tx = (box[0] + box[2]) / 2
        else:                                                         # height/depth: left side (right for the left view)
            tx = box[0] - OFF if name != "left" else box[2] + OFF
            ty = (box[1] + box[3]) / 2
        tb = text_box(tx, ty, txt)
        if clash(tb, taken + blocked) or tb[0] < FRAME[0] or tb[2] > FRAME[2] or tb[1] < FRAME[1] or tb[3] > FRAME[3]:
            skipped.append(f"{name}: general {txt} mm (choca)")
            continue
        taken.append(tb)
        out.append({"type": "Onshape::Dimension::LineToLine", "lineToLineDimension": {
            "edge1": {"type": "Onshape::Reference::Edge", "viewId": vid, "uniqueId": e1[0]["uniqueId"]},
            "edge2": {"type": "Onshape::Reference::Edge", "viewId": vid, "uniqueId": e2[0]["uniqueId"]},
            "formatting": {"type": "Onshape::Formatting::Dimension", "dimdec": 1},
            "textOverride": "", "textPosition": {"type": "Onshape::Reference::Point", "coordinate": [tx, ty, 0]}}})
    # holes whose axis is the view direction: one diameter per radius
    axis_k = {"front": 1, "top": 2, "left": 0}.get(name)
    if axis_k is not None:
        mine = [h for h in hole_list if h[1] == axis_k]
        by_r = {}
        for h in mine:
            by_r.setdefault(round(h[2], 3), []).append(h)
        circles = [e for e in geom if e["type"] == "circle" and e.get("visible", True)]
        for r, hs in sorted(by_r.items()):
            hit = None
            for h in sorted(hs, key=lambda h: -abs(h[0][0]) - abs(h[0][1]) - abs(h[0][2])):
                for e in circles:
                    hu, hv = project(vm, [v / 1000 for v in h[0]])
                    d = (1000 * e["data"]["center"][0] - hu, 1000 * e["data"]["center"][1] - hv)
                    if abs(1000 * e["data"]["radius"] - r) < 0.01 and math.hypot(*d) < 0.05:
                        hit = (h, e)
                        break
                if hit:
                    break
            label = f"{len(hs)}x Ø{2 * r:.1f}" if len(hs) > 1 else f"Ø{2 * r:.1f}"
            if not hit:
                skipped.append(f"{name}: {label} (no encontré el círculo en la vista)")
                continue
            h, e = hit
            cx, cy = to_sheet((1000 * e["data"]["center"][0], 1000 * e["data"]["center"][1]))
            # text outside the view, on the side of the nearest box edge, 45 degrees from the centre
            dx = -1 if cx - box[0] < box[2] - cx else 1
            dy = -1 if cy - box[1] < box[3] - cy else 1
            tx = (box[0] - OFF - 6) if dx < 0 else (box[2] + OFF + 6)
            ty = cy + dy * (abs(tx - cx) * 0.5)
            tb = text_box(tx, ty, label)
            if clash(tb, taken + blocked) or tb[0] < FRAME[0] or tb[2] > FRAME[2] or tb[1] < FRAME[1] or tb[3] > FRAME[3]:
                skipped.append(f"{name}: {label} (choca)")
                continue
            taken.append(tb)
            rr = e["data"]["radius"]
            c3 = e["data"]["center"]
            p1 = [c3[0] + rr, c3[1], c3[2]]
            p2 = [c3[0] - rr, c3[1], c3[2]]
            out.append({"type": "Onshape::Dimension::Diametric", "diametricDimension": {
                "chordPoint": ref_pt(vid, e["uniqueId"], p1, "ModeNear"),
                "farChordPoint": ref_pt(vid, e["uniqueId"], p2, "ModeNear"),
                "formatting": {"type": "Onshape::Formatting::Dimension", "dimdec": 1},
                **({"prefix": f"{len(hs)}x Ø"} if len(hs) > 1 else {}),     # a prefix replaces the Ø sign
                "textOverride": "", "textPosition": {"type": "Onshape::Reference::Point", "coordinate": [tx, ty, 0]}}})
    return out, skipped


def export_pdf(c, did, wid, eid, dst):
    t = c.call("POST", f"/drawings/d/{did}/w/{wid}/e/{eid}/translations",
               {"formatName": "PDF", "storeInDocument": False, "showOverriddenDimensions": True})
    for i in range(12):
        time.sleep(4 + 3 * i)
        t = c.call("GET", f"/translations/{t['id']}")
        if t.get("requestState") != "ACTIVE":
            break
    if t.get("requestState") != "DONE":
        raise OS.OnshapeError(f"PDF: {t.get('requestState')} {t.get('failureReason')}")
    xid = t["resultExternalDataIds"][0]
    req = urllib.request.Request(OS.API + f"/documents/d/{did}/externaldata/{xid}", headers={"Authorization": c.auth})
    with urllib.request.urlopen(req, timeout=120) as r:
        OS.log_call("GET", f"/documents/d/{did}/externaldata/{xid}", r.status)
        dst.write_bytes(r.read())


def piece(code, step, qty, c=None, redo=False):
    c = c or client()
    n0 = quota_ok()
    R = reg()
    doc = R["documento"]
    did, wid = doc["did"], doc["wid"]
    rec = R.setdefault("piezas", {}).get(code, {})
    if redo and "drawing" in rec:                                     # nothing is deleted: the old drawing is renamed
        old = rec["drawing"]
        md = c.call("GET", f"/metadata/d/{did}/w/{wid}/e/{old}")
        nid = next(p["propertyId"] for p in md["properties"] if p["name"] == "Name")
        n_old = len(rec.get("obsoletos", [])) + 1
        c.call("POST", f"/metadata/d/{did}/w/{wid}/e/{old}",
               {"properties": [{"propertyId": nid, "value": f"zz_obsoleto_PLANO_{code}_v{n_old}"}]})
        rec["obsoletos"] = rec.get("obsoletos", []) + [old]
        for k in ("drawing", "vistas", "cotas", "cajetin", "pdf"):
            rec.pop(k, None)
    if "partstudio" not in rec:                                       # 1. Part Studio tab with the code as name
        name, made = OP.push(step, code, did=did, wid=wid, client=c)
        ps = next(u for n, typ, u in made if typ == "PARTSTUDIO")
        rec["partstudio"] = ps.rsplit("/e/", 1)[1]
        rec["pestana"] = name
    eid = rec["partstudio"]
    parts = c.call("GET", f"/parts/d/{did}/w/{wid}/e/{eid}")
    pid = parts[0]["partId"]
    rec["propiedades"] = set_props(c, did, wid, eid, pid, code)
    lo, hi = bbox(step)
    (num, den), iso_s, centres, boxes = layout(lo, hi)
    s = num / den
    if "drawing" not in rec:                                          # 2. Drawing, empty, then the 7 views
        d = c.call("POST", f"/drawings/d/{did}/w/{wid}/create", {
            "drawingName": f"PLANO_{code}", "elementId": eid, "partId": pid, "views": "zero", "titleblock": True,
            "border": True, "units": "MILLIMETER", "projection": "First", "size": "A3", "standard": "ISO"})
        rec["drawing"] = d["id"]
        R["piezas"][code] = rec
        save(R)
    deid = rec["drawing"]
    if not rec.get("cajetin"):                                        # title block: drawing properties
        md = c.call("GET", f"/metadata/d/{did}/w/{wid}/e/{deid}")
        ids = {p["name"]: p["propertyId"] for p in md.get("properties", [])}
        want = {"Title 1": code, "Title 2": f"Material: PETG   ·   Cantidad: {qty}", "Title 3": PROJECT,
                "Part number": code, "Description": PROJECT}
        c.call("POST", f"/metadata/d/{did}/w/{wid}/e/{deid}",
               {"properties": [{"propertyId": ids[k], "value": v} for k, v in want.items() if k in ids]})
        rec["cajetin"] = sorted(k for k in want if k in ids)
    if "vistas" not in rec:
        views = []
        for o, (x, y) in centres.items():
            sn, sd = iso_s if o == "isometric" else (num, den)
            views.append({"viewType": "TopLevel", "position": {"x": x, "y": y}, "orientation": o,
                          "scale": {"scaleSource": "Custom", "numerator": sn, "denumerator": sd},
                          "reference": {"elementId": eid}})
        res = wait_modify(c, did, wid, deid, [{"messageName": "onshapeCreateViews", "formatVersion": "2021-01-01",
                                               "views": views}], f"vistas {code}")
        rec["vistas"] = {o: r.get("viewId") for o, r in zip(centres, res.get("results", []))}
        R["piezas"][code] = rec
        save(R)
    if "cotas" not in rec:                                            # 3. dimensions + quantity note
        info = {v["viewId"]: v for v in c.call("GET", f"/drawings/d/{did}/w/{wid}/e/{deid}/views")["items"]}
        hole_list = holes(step)
        anns, skipped, taken = [], [], []
        ctr = [(lo[i] + hi[i]) / 2 / 1000 for i in range(3)]
        for o in ("front", "top", "left"):
            vid = rec["vistas"][o]
            vm = info[vid]["viewMatrix"]
            geom = c.call("GET", f"/drawings/d/{did}/w/{wid}/e/{deid}/views/{vid}/jsongeometry")["bodyData"]
            a, sk = dims_for_view(o, vid, vm, geom, boxes[o], project(vm, ctr), s, lo, hi, hole_list, taken,
                                  {k: b for k, b in boxes.items() if k != o})
            anns += a
            skipped += sk
        note = f"Cantidad: {qty}   ·   Material: PETG   ·   {PROJECT}"
        anns.append({"type": "Onshape::Note", "note": {"position": {"type": "Onshape::Reference::Point",
                     "coordinate": [TITLE[0] + 2, TITLE[3] + 8, 0]}, "contents": note, "textHeight": TEXT_H}})
        res = wait_modify(c, did, wid, deid, [{"messageName": "onshapeCreateAnnotations", "formatVersion": "2021-01-01",
                                               "annotations": anns}], f"cotas {code}")
        results = res.get("results", [])
        failed = [(a["type"], r.get("errorDescription")) for a, r in zip(anns, results) if r.get("status") != "OK"]
        rec["cotas"] = {"creadas": sum(1 for r in results if r.get("status") == "OK"), "fallidas": failed,
                        "a_mano": skipped, "agujeros": len(hole_list)}
        R["piezas"][code] = rec
        save(R)
    pdf = OUT / "pdf" / f"PLANO_{code}.pdf"                         # 4. PDF
    pdf.parent.mkdir(parents=True, exist_ok=True)
    export_pdf(c, did, wid, deid, pdf)
    rec.update(escala=f"{num}:{den}", escala_iso=f"{iso_s[0]}:{iso_s[1]}", cantidad=qty, pdf=str(pdf.relative_to(MOD)),
               url=f"https://cad.onshape.com/documents/{did}/w/{wid}/e/{deid}", llamadas=OS.year_total() - n0)
    R["piezas"][code] = rec
    save(R)
    print(code, json.dumps({k: rec[k] for k in ("escala", "cotas", "llamadas", "url")}, ensure_ascii=False))
    return rec


def document():
    c = client()
    quota_ok()
    doc = OP.ensure_document(c, DOC)
    did, wid = doc["did"], doc["wid"]
    c.call("POST", f"/documents/{did}", {"parentId": FOLDER, "description": f"Planos de impresion de P2 + boya PET 4 x 1 L. {PROJECT}"})
    R = reg()
    try:                                                              # link sharing (view + export)
        c.call("POST", f"/documents/{did}/acl/anonymousAccess", {"anonymousAccessAllowed": True, "anonymousAllowsExport": True})
        R["link_sharing"] = "ok"
    except OS.OnshapeError as e:                                      # 403: the API key has no share scope
        R["link_sharing"] = f"a mano en Onshape (Share > Link): {str(e)[:80]}"
    R["documento"] = {**doc, "url": f"https://cad.onshape.com/documents/{did}/w/{wid}"}
    save(R)
    if "ensamble" not in R:
        step = assembly()
        name, made = OP.push(step, "00_ENSAMBLE", did=did, wid=wid, client=c)
        R["ensamble"] = {"pestana": name, "pestanas": made}
        save(R)
    print(json.dumps(R["documento"], ensure_ascii=False))


def assembly():
    """Node P2 and the PET buoy as built, without REF_ (lantern, cords, electronics, bottles) and without ballast; the
    buoy is drawn 150 mm above the handle of the node (in the water it floats at the end of the umbilical)."""
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "ENSAMBLE_P2_boya_impresas.step"
    asm = cq.Assembly(name="LG_IMPRIMIR_P2")
    node = cq.Assembly.importStep(str(P2 / "ensamble_simple_D200_v2_nombres.step"))
    buoy = cq.Assembly.importStep(str(BOYA / "ENSAMBLE_boya_pet_v2_nombres.step"))
    keep = lambda n: not n.lower().startswith(("ref_", "lastre", "lr"))      # the buoy STEP keeps ref_ in its usage names
    ztop = None
    for name, a in node.traverse():
        if a.obj is not None and keep(name):
            sh = a.obj.val() if hasattr(a.obj, "val") else a.obj
            sh = sh.moved(a.loc) if a.loc else sh
            ztop = max(ztop or -1e9, sh.BoundingBox().zmax)
            asm.add(sh, name=name)
    bz = None
    items = []
    for name, a in buoy.traverse():
        if a.obj is not None and keep(name):
            sh = a.obj.val() if hasattr(a.obj, "val") else a.obj
            sh = sh.moved(a.loc) if a.loc else sh
            bz = min(bz or 1e9, sh.BoundingBox().zmin)
            items.append((name, sh))
    for name, sh in items:
        asm.add(sh.moved(cq.Location(cq.Vector(0, 0, ztop + 150 - bz))), name=name)
    asm.save(str(out), exportType="STEP")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--documento", action="store_true")
    ap.add_argument("--pieza")
    ap.add_argument("--todas", action="store_true")
    ap.add_argument("--rehacer", action="store_true", help="renombra el Drawing anterior a zz_obsoleto_ y hace uno nuevo")
    a = ap.parse_args()
    if a.documento:
        document()
    if a.pieza:
        code, step, _, q = next(p for p in PIECES if p[0] == a.pieza)
        piece(code, step, q, redo=a.rehacer)
    if a.todas:
        c = client()
        done = reg().get("piezas", {})
        for code, step, _, q in PIECES:
            if "pdf" not in done.get(code, {}):
                piece(code, step, q, c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
