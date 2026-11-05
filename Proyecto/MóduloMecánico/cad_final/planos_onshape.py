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
    ("B1_casco", 2), ("B2_cubierta_lisa", 1), ("B2_cubierta_mastil", 1), ("B3_caja", 1), ("B4_tapa", 1),
    ("B5_cuna_base", 2), ("B5_cuna_cuello", 2), ("B6_correa", 4))]

# sheet (A3 landscape, mm): drawing frame and the standard Onshape title block measured on the first PDF
SHEET = (420.0, 297.0)
FRAME = (12.0, 12.0, 408.0, 285.0)
TITLE = (190.0, 0.0, 420.0, 64.0)
GAP = 14.0                                    # between views: room for one dimension line and its text
SCALES = [(2, 1), (1, 1), (1, 2), (2, 5), (1, 5), (1, 10)]          # 2:5 = 1:2.5
ISO_SCALES = [(2, 1), (1, 1), (2, 3), (1, 2), (2, 5), (1, 3), (1, 4), (1, 5), (1, 8), (1, 10)]
TEXT_H = 3.5
OFF = 7.0                                     # dimension text distance from the view box
FMT_NAME = "A3"
MARGIN_L = 0.0                                # extra room left of the first column (vertical dimension texts)


def use_format(name):
    """--formato equipo: the team's sheet (Melissa's B1_casco by hand): ISO A4 landscape, standard Onshape title block
    at (125..287, 10..48), frame 10 mm. The layout and dimension helpers read these module globals."""
    global SHEET, FRAME, TITLE, GAP, OFF, TEXT_H, SCALES, FMT_NAME, MARGIN_L
    if name == "equipo":
        SHEET, FRAME, TITLE = (297.0, 210.0), (10.0, 10.0, 287.0, 200.0), (124.0, 0.0, 297.0, 49.0)
        GAP, OFF, TEXT_H, FMT_NAME, MARGIN_L = 13.0, 5.5, 3.2, "A4", 8.0
        SCALES = [(2, 1), (1, 1), (1, 2), (2, 5), (1, 3), (1, 4), (1, 5), (1, 8), (1, 10)]


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
def layout(lo, hi, back=True, right=True):
    """Scale and view centres (sheet mm). First angle: bottom view above the front, top view below it, the right
    view on the left of the front, the left view on its right, the back view at the far right (back=False: no back
    view, the isometric takes its column; right=False: no right view, the front starts at the left margin)."""
    W, D, H = (hi[i] - lo[i] for i in range(3))
    for num, den in SCALES:
        s = num / den
        cw = [s * D if right else 0.0, s * W, s * D, s * W if back else 0.0]   # columns: right, front, left, back
        rh = [s * D, s * H, s * D]                                    # rows: top view, main row, bottom view
        x = [FRAME[0] + GAP + MARGIN_L]
        for i in range(1, 4):
            x.append(x[-1] + cw[i - 1] + (GAP if cw[i - 1] > 0 else 0.0))
        y0 = max(FRAME[1] + GAP, TITLE[3] + 12 - GAP - rh[0])         # main row clear of the quantity note
        if x[1] + cw[1] > TITLE[0] - 4:                               # top view would reach the title block: lift it
            y0 = TITLE[3] + 4
        y = [y0, y0 + rh[0] + GAP, y0 + rh[0] + GAP + rh[1] + GAP]
        xr, top = x[3] + cw[3], y[2] + rh[2]
        if xr > FRAME[2] - 4 or top > FRAME[3] - 4:
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
        for k, on in (("back", back), ("right", right)):
            if not on:
                views.pop(k)
                boxes.pop(k)
        return (num, den), iso_s, views, boxes
    raise SystemExit(f"ninguna escala estandar entra en {FMT_NAME}")


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


def text_box(x, y, txt, vertical=False):
    w = 0.62 * TEXT_H * len(txt) + 2
    if vertical:
        return (x - TEXT_H / 2 - 1, y - w / 2, x + TEXT_H / 2 + 1, y + w / 2)
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


def thickness(vid, geom, box, centre_uv, s, boxes):
    """Thinnest plate (two long horizontal lines from the bottom up) or wall (two long vertical lines from the left)
    of the left view, <= 12 mm. Returns (annotation or None, text for the registry)."""
    segs = []
    for e in geom:
        if e["type"] == "line" and e.get("visible", True):
            (x0, y0), (x1, y1) = (1000 * e["data"]["start"][0], 1000 * e["data"]["start"][1]),                                  (1000 * e["data"]["end"][0], 1000 * e["data"]["end"][1])
            segs.append((e, x0, y0, x1, y1))
    if not segs:
        return None, "sin aristas rectas"
    W = max(max(s_[1], s_[3]) for s_ in segs) - min(min(s_[1], s_[3]) for s_ in segs)
    H = max(max(s_[2], s_[4]) for s_ in segs) - min(min(s_[2], s_[4]) for s_ in segs)
    to_sheet = lambda u, v: ((box[0] + box[2]) / 2 + s * (u - centre_uv[0]), (box[1] + box[3]) / 2 + s * (v - centre_uv[1]))
    best = None
    for k, span in ((1, W), (0, H)):                                  # k = 1: horizontal lines, gap in v
        long_ = [g for g in segs if (abs(g[2] - g[4]) < 1e-3 if k == 1 else abs(g[1] - g[3]) < 1e-3)
                 and (abs(g[1] - g[3]) if k == 1 else abs(g[2] - g[4])) >= 0.3 * span]
        if len(long_) < 2:
            continue
        pos = lambda g: g[2] if k == 1 else g[1]
        long_.sort(key=pos)
        a = long_[0]
        b = next((g for g in long_[1:] if 0.5 <= pos(g) - pos(a) <= 12.0), None)
        if b and (best is None or pos(b) - pos(a) < best[0]):
            best = (pos(b) - pos(a), k, a, b)
    if best is None:
        return None, "sin placa ni pared <= 12 mm en la vista lateral"
    t, k, a, b = best
    if k == 1:                                                        # plate: text left of the view, at its height
        tx, ty = box[0] - 6.0, to_sheet(0, (a[2] + b[2]) / 2)[1]
    else:                                                             # wall: text below the view, at its position
        tx, ty = to_sheet((a[1] + b[1]) / 2, 0)[0], box[1] - 6.0
    txt = f"{t:.1f}"
    tb = text_box(tx, ty, txt)
    others = [TITLE] + [bb for kk, bb in boxes.items() if kk != "left"]
    if clash(tb, others) or tb[0] < FRAME[0] or tb[1] < FRAME[1]:
        return None, f"espesor {txt} mm (choca)"
    return {"type": "Onshape::Dimension::LineToLine", "lineToLineDimension": {
        "edge1": {"type": "Onshape::Reference::Edge", "viewId": vid, "uniqueId": a[0]["uniqueId"]},
        "edge2": {"type": "Onshape::Reference::Edge", "viewId": vid, "uniqueId": b[0]["uniqueId"]},
        "formatting": {"type": "Onshape::Formatting::Dimension", "dimdec": 1}, "textOverride": "",
        "textPosition": {"type": "Onshape::Reference::Point", "coordinate": [tx, ty, 0]}}},         f"{'placa' if k == 1 else 'pared'} {txt} mm"


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
    if not rec.get("autor"):                                          # author field of the title block
        md = c.call("GET", f"/metadata/d/{did}/w/{wid}/e/{deid}")
        pid_by = next((p["propertyId"] for p in md["properties"] if p["name"] == "Drawn by"), None)
        if pid_by:
            c.call("POST", f"/metadata/d/{did}/w/{wid}/e/{deid}",
                   {"properties": [{"propertyId": pid_by, "value": "Equipo 02 UPCH"}]})
            rec["autor"] = "Equipo 02 UPCH"
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
    if "espesor" not in rec:                                          # 3b. plate or wall thickness, left view
        info = {v["viewId"]: v for v in c.call("GET", f"/drawings/d/{did}/w/{wid}/e/{deid}/views")["items"]}
        vid = rec["vistas"]["left"]
        vm = info[vid]["viewMatrix"]
        geom = c.call("GET", f"/drawings/d/{did}/w/{wid}/e/{deid}/views/{vid}/jsongeometry")["bodyData"]
        ctr = [(lo[i] + hi[i]) / 2 / 1000 for i in range(3)]
        ann, why = thickness(vid, geom, boxes["left"], project(vm, ctr), s, boxes)
        rec["espesor"] = why
        if ann:
            res = wait_modify(c, did, wid, deid, [{"messageName": "onshapeCreateAnnotations", "formatVersion": "2021-01-01",
                                                   "annotations": [ann]}], f"espesor {code}")
            r0 = (res.get("results") or [{}])[0]
            if r0.get("status") != "OK":
                rec["espesor"] = f"fallo: {r0.get('errorDescription')}"
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


# ---------------------------------------------------------------- --formato equipo (A4, Melissa's B1 as the model)
SKIN_STEP = MOD / "salida" / "skin" / "P2_robusto" / "concha" / "SKIN_concha.step"
A4_ORDER = ["B1_casco", "B2_cubierta_lisa", "B2_cubierta_mastil", "B3_caja", "B4_tapa", "B5_cuna_base", "B5_cuna_cuello",
            "B6_correa", "M1s_caja_cuerpo", "M2_caja_tapa",
            "M3s_riel_gancho", "M3t_tapa_bolsillo", "M4_capsula_cuerpo", "M5s_capsula_tapa_pie", "M6_capsula_bisel",
            "M11_bandeja", "M11_bandeja_sup", "SKIN_concha"]
MELISSA_B1 = "50788a3701406af8a0f183a5"          # "Drawing 1 B1_casco", drawn by hand: exported as is, never modified
COMPANY = "LANTERNGUARD"
OUT_A4 = OUT / "pdf_a4"
CACHE = OUT / "cache_vistas"
LIMIT_A4 = 2200                                   # of 2500/year (EDU): keeps 300 for November and December
RIB_T = 4.0                                       # gap <= this between two long parallel edges = a wall or a rib
# The title block that the API creates (ISO A4) has the same grid as Melissa's but no labels: her labels are added as
# notes, at her positions and text heights. Onshape places a note by its top-left corner and ignores {\\pxqc;}, so
# the centred ones ("C") are shifted by half their estimated width and long ones are split to fit their cell.
# (L/C, x, y top, text height, cell width, text)
TB_NOTES = [
    ("L", 125.75, 47.00, 1.000, 29.9, "UNLESS OTHERWISE SPECIFIED, DIMENSIONS ARE IN MILLIMETERS"),
    ("L", 130.60, 41.40, 1.097, 15.0, "ANGULAR"), ("L", 125.75, 35.12, 1.219, 16.5, "SURFACE FINISH"),
    ("C", 140.31, 28.84, 1.585, 29.9, "DO NOT SCALE DRAWING"),
    ("C", 140.31, 24.75, 1.219, 29.9, "BREAK ALL SHARP EDGES AND REMOVE BURRS"),
    ("C", 140.31, 19.57, 1.219, 29.9, "FIRST ANGLE PROJECTION"), ("C", 191.75, 47.00, 1.219, 14.9, "SIGNATURE"),
    ("L", 169.56, 47.00, 1.219, 14.9, "NAME"), ("C", 204.13, 47.00, 1.219, 9.3, "DATE"),
    ("L", 156.23, 42.43, 1.219, 13.1, "DRAWN"), ("L", 156.23, 37.86, 1.219, 13.1, "CHECKED"),
    ("L", 156.23, 33.29, 1.219, 13.1, "APPROVED"), ("C", 176.51, 32.10, 1.024, 15.2, "----"),
    ("C", 204.13, 32.10, 1.024, 9.5, "----"), ("L", 156.23, 19.57, 1.219, 26.1, "MATERIAL"),
    ("C", 168.89, 15.33, 1.829, 26.7, "PETG"), ("C", 204.13, 42.43, 1.0, 9.3, "<DATE>"), ("L", 182.90, 19.57, 1.219, 26.1, "FINISH"),
    ("L", 209.57, 37.48, 1.219, 9.3, "TITLE"), ("C", 247.95, 30.73, 2.926, 70.5, "<CODE>"),
    ("L", 209.43, 21.70, 0.975, 9.4, "SIZE"), ("L", 218.96, 21.70, 0.975, 59.7, "DWG NO."),
    ("L", 279.92, 21.70, 0.975, 7.5, "REV."), ("C", 283.57, 18.76, 3.658, 6.9, "-"),
    ("L", 209.43, 14.08, 0.975, 16.4, "SCALE"), ("L", 226.20, 14.08, 0.975, 34.0, "WEIGHT"),
    ("L", 260.87, 14.08, 0.975, 26.1, "SHEET"), ("C", 247.93, 43.50, 2.926, 70.5, COMPANY)]


def text_w(s, h):
    """Estimated width (mm) of s in Onshape's drawing font (Noto Sans) at cap height h."""
    return h * sum(0.92 if ch.isupper() else 0.77 if ch.islower() else 0.8 if ch.isdigit() else
                   0.35 if ch in " .,:" else 0.62 for ch in s)


def title_notes(code):
    out = []
    for mode, x, y, h, cell, txt in TB_NOTES:
        txt = txt.replace("<CODE>", code).replace("<DATE>", time.strftime("%Y-%m-%d"))
        lines, cur = [], ""
        for w in txt.split():
            if cur and text_w(cur + " " + w, h) > min(cell - 0.6, 19.5 * h):     # Onshape wraps a note past ~20 x its height
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        xl = x if mode == "L" else x - max(text_w(ln, h) for ln in lines) / 2      # one note, explicit line breaks
        out.append({"type": "Onshape::Note", "note": {"position": {"type": "Onshape::Reference::Point",
                    "coordinate": [xl, y, 0]}, "contents": "\n".join(lines), "textHeight": h}})
    return out


def best_layout(lo, hi):
    """Largest scale over the optional views (right side, back); at equal scale, the one with more views."""
    best = None
    for right, back in ((True, True), (False, True), (True, False), (False, False)):
        try:
            L = layout(lo, hi, back=back, right=right)
        except SystemExit:
            continue
        if best is None or L[0][0] / L[0][1] > best[0][0] / best[0][1] + 1e-9:
            best = L
    if best is None:
        raise SystemExit(f"ninguna escala estandar entra en {FMT_NAME}")
    return best


def a4_pieces():
    by = {c: (st, q) for c, st, _, q in PIECES}
    by["SKIN_concha"] = (SKIN_STEP, 1)
    return [(c, *by[c]) for c in A4_ORDER]


def m(xyz):
    return [1000 * v for v in xyz]


def view_parts(geom):
    """jsongeometry (view space, m) -> visible lines, circles and arcs in view mm, each with its entity."""
    L, C, A = [], [], []
    for e in geom:
        if not e.get("visible", True):
            continue
        d = e["data"]
        if e["type"] == "line":
            a, b = m(d["start"]), m(d["end"])
            L.append((e, (a[0], a[1]), (b[0], b[1])))
        elif e["type"] == "circle" and "center" in d:
            C.append((e, tuple(m(d["center"])[:2]), 1000 * d["radius"]))
        elif e["type"] == "arc" and "center" in d:
            A.append((e, tuple(m(d["center"])[:2]), 1000 * d["radius"]))
    return L, C, A


def place(cands, txt, taken, blocked, vertical=False):
    """First candidate text position whose box is free and inside the frame; it is reserved."""
    for tx, ty in cands:
        tb = text_box(tx, ty, txt, vertical)
        if not clash(tb, taken + blocked) and tb[0] >= FRAME[0] and tb[2] <= FRAME[2] and tb[1] >= FRAME[1] and tb[3] <= FRAME[3]:
            taken.append(tb)
            return tx, ty
    return None


def pt(xyz):
    return {"type": "Onshape::Reference::Point", "coordinate": [xyz[0], xyz[1], 0]}


def fmt(prefix=""):
    f = {"type": "Onshape::Formatting::Dimension", "dimdec": 1}
    return f


def ann_l2l(vid, e1, e2, txy, prefix=""):
    d = {"edge1": {"type": "Onshape::Reference::Edge", "viewId": vid, "uniqueId": e1["uniqueId"]},
         "edge2": {"type": "Onshape::Reference::Edge", "viewId": vid, "uniqueId": e2["uniqueId"]},
         "formatting": fmt(), "textOverride": "", "textPosition": pt(txy)}
    if prefix:
        d["prefix"] = prefix
    return {"type": "Onshape::Dimension::LineToLine", "lineToLineDimension": d}


def num(v):
    return f"{v:.1f}".rstrip("0").rstrip(".").replace(".", ",")


def dims_a4(name, vid, geom, box, centre_uv, s, taken, blocked, used):
    """Dimensions of one orthographic view, in the order of Melissa's B1: overall size, wall/rib thickness and the
    spacing between ribs (chain), patterned diameters (n x Ø), patterned radii (n x R) and the position of one hole of
    each size from the left and bottom edges. Returns (annotations, list of what was left for hand)."""
    out, skip = [], []
    L, C, A = view_parts(geom)
    if not L:
        return out, [f"{name}: sin aristas rectas, solo cotas a mano"]
    sx = lambda u: (box[0] + box[2]) / 2 + s * (u - centre_uv[0])
    sy = lambda v: (box[1] + box[3]) / 2 + s * (v - centre_uv[1])
    us = [p[0] for _, a, b in L for p in (a, b)]
    vs = [p[1] for _, a, b in L for p in (a, b)]
    ext = ((min(us), max(us)), (min(vs), max(vs)))
    row = TEXT_H + 5.0
    above = [box[3] + OFF + i * row for i in range(4)]
    below = [box[1] - OFF - i * row for i in range(4)]
    left = [box[0] - OFF - 4 - i * 9 for i in range(3)]
    right = [box[2] + OFF + 4 + i * 9 for i in range(3)]
    edge_at = {}
    for k in (0, 1):                                                   # 1. overall size
        mn, mx = ext[k]
        par = lambda ln, t: abs(ln[1][k] - t) < 0.05 and abs(ln[2][k] - t) < 0.05
        side = lambda t: max((ln for ln in L if par(ln, t)), key=lambda ln: abs(ln[1][1 - k] - ln[2][1 - k]), default=None)
        e1, e2 = side(mn), side(mx)
        edge_at[k] = e1
        txt = num(mx - mn)
        if e1 is None or e2 is None:
            skip.append(f"{name}: {'ancho' if k == 0 else 'alto'} total {txt} (el borde es curvo)")
            continue
        cands = ([(sx((mn + mx) / 2), y) for y in (above[:1] + below[:1])] if k == 0 else
                 [(x, sy((mn + mx) / 2)) for x in (left[:1] + right[:1])])
        p = place(cands, txt, taken, blocked, vertical=k == 1)
        if p is None:
            skip.append(f"{name}: {'ancho' if k == 0 else 'alto'} total {txt} (sin espacio)")
            continue
        out.append(ann_l2l(vid, e1[0], e2[0], p))
    for k in (0, 1):                                                   # 2. walls, ribs and spacing (chain)
        span = ext[1 - k][1] - ext[1 - k][0]
        lng = [ln for ln in L if abs(ln[1][k] - ln[2][k]) < 1e-3 and abs(ln[1][1 - k] - ln[2][1 - k]) >= 0.35 * span]
        pos = {}
        for ln in lng:
            key = round(ln[1][k] / 0.05) * 0.05
            if key not in pos or abs(ln[1][1 - k] - ln[2][1 - k]) > abs(pos[key][1][1 - k] - pos[key][2][1 - k]):
                pos[key] = ln
        P = sorted(pos)
        what = "nervios verticales" if k == 0 else "nervios horizontales"
        if len(P) < 3:
            continue
        if len(P) > 16:
            skip.append(f"{name}: {what} ({len(P)} aristas, demasiadas para encadenar)")
            continue
        gaps = [(P[i + 1] - P[i], i) for i in range(len(P) - 1)]
        thin = [(g, i) for g, i in gaps if 0.3 <= g <= RIB_T]
        wide = [(g, i) for g, i in gaps if g > RIB_T]
        rows_k = (above[1:] + below[1:]) if k == 0 else (left[1:] + right[1:])
        mk = lambda c: [(sx(c), y) for y in rows_k] if k == 0 else [(x, sy(c)) for x in rows_k]
        if thin:
            t = min(g for g, _ in thin)
            same = [i for g, i in thin if abs(g - t) < 0.06]
            i = same[0]
            pre = f"{len(same)}x " if len(same) > 1 else ""
            p = place(mk((P[i] + P[i + 1]) / 2), pre + num(t), taken, blocked, vertical=k == 1)
            if p:
                out.append(ann_l2l(vid, pos[P[i]][0], pos[P[i + 1]][0], p, pre))
            else:
                skip.append(f"{name}: espesor {pre}{num(t)} (sin espacio)")
        if len(wide) >= 2:
            g0 = wide[0][0]
            if all(abs(g - g0) < 0.06 for g, _ in wide):
                todo = [(g0, wide[0][1], f"{len(wide)}x ")]
            else:
                todo = [(g, i, "") for g, i in wide[:6]]
                if len(wide) > 6:
                    skip.append(f"{name}: {len(wide) - 6} separaciones más entre {what}")
            for g, i, pre in todo:
                p = place(mk((P[i] + P[i + 1]) / 2), pre + num(g), taken, blocked, vertical=k == 1)
                if p:
                    out.append(ann_l2l(vid, pos[P[i]][0], pos[P[i + 1]][0], p, pre))
                else:
                    skip.append(f"{name}: separación {pre}{num(g)} entre {what} (sin espacio)")
    groups = {}                                                        # 3. diameters, n x Ø
    for e, c, r in C:
        g = groups.setdefault(round(r, 2), {})
        g.setdefault((round(c[0], 2), round(c[1], 2)), (e, c, r))
    n_d = 0
    for r, g in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        if r in used["d"] or 2 * r < 0.5:
            continue
        if n_d >= 4:
            skip.append(f"{name}: Ø{num(2 * r)} (más de 4 diámetros en la vista)")
            continue
        used["d"].add(r)
        n_d += 1
        hs = list(g.values())
        e, c, rr = min(hs, key=lambda h: (h[1][0] - ext[0][0]) + (h[1][1] - ext[1][0]))     # nearest the bottom-left
        pre = f"{len(hs)}x Ø" if len(hs) > 1 else ""
        label = (pre or "Ø") + num(2 * r)
        cx, cy = sx(c[0]), sy(c[1])
        cands = [(x, cy) for x in (left + right)]
        p = place(sorted(cands, key=lambda q: abs(q[0] - cx) + abs(q[1] - cy)), label, taken, blocked)
        if p is None:
            skip.append(f"{name}: {label} (sin espacio)")
            continue
        c3 = e["data"]["center"]
        rm = e["data"]["radius"]
        d = {"chordPoint": ref_pt(vid, e["uniqueId"], [c3[0] + rm, c3[1], c3[2]], "ModeNear"),
             "farChordPoint": ref_pt(vid, e["uniqueId"], [c3[0] - rm, c3[1], c3[2]], "ModeNear"),
             "formatting": fmt(), "textOverride": "", "textPosition": pt(p)}
        if pre:
            d["prefix"] = pre
        out.append({"type": "Onshape::Dimension::Diametric", "diametricDimension": d})
        for k in (0, 1):                                               # 4. its position from the left / bottom edge
            ed = edge_at.get(k)
            dist = c[k] - ext[k][0]
            if ed is None or dist < 0.5 or n_d > 2:
                continue
            cands = ([(sx(ext[0][0] + dist / 2), y) for y in below[1:] + above[1:]] if k == 0 else
                     [(x, sy(ext[1][0] + dist / 2)) for x in left[1:] + right[1:]])
            p = place(cands, num(dist), taken, blocked, vertical=k == 1)
            if p is None:
                skip.append(f"{name}: posición de {label} a {num(dist)} del borde (sin espacio)")
                continue
            out.append({"type": "Onshape::Dimension::PointToLine", "pointToLineDimension": {
                "point": ref_pt(vid, e["uniqueId"], c3, "ModeCenter"),
                "edge": {"type": "Onshape::Reference::Edge", "viewId": vid, "uniqueId": ed[0]["uniqueId"]},
                "formatting": fmt(), "textOverride": "", "textPosition": pt(p)}})
    rg = {}                                                            # 5. radii, n x R (arcs, not full circles)
    for e, c, r in A:
        if 0.4 <= r <= 60:
            rg.setdefault(round(r, 2), {}).setdefault((round(c[0], 2), round(c[1], 2)), (e, c, r))
    n_r = 0
    for r, g in sorted(rg.items(), key=lambda kv: -len(kv[1])):
        if r in used["r"] or r in used["d"] or n_r >= 3:
            continue
        used["r"].add(r)
        n_r += 1
        e, c, _ = next(iter(g.values()))
        pre = f"{len(g)}x R" if len(g) > 1 else "R"
        label = pre + num(r)
        cx, cy = sx(c[0]), sy(c[1])
        cands = [(x, cy) for x in (left + right)]
        p = place(sorted(cands, key=lambda q: abs(q[0] - cx) + abs(q[1] - cy)), label, taken, blocked)
        if p is None:
            skip.append(f"{name}: {label} (sin espacio)")
            continue
        d = e["data"]
        out.append({"type": "Onshape::Dimension::Radial", "radialDimension": {
            "centerPoint": ref_pt(vid, e["uniqueId"], d["center"], "ModeCenter"),
            "chordPoint": ref_pt(vid, e["uniqueId"], d.get("start", d["center"]), "ModeNear"),
            "formatting": {**fmt(), "dimpost": pre + "<>"}, "prefix": pre, "textOverride": "", "textPosition": pt(p)}})
    return out, skip


def piece_a4(code, step, qty, c, ctx, redo=False, chamfer=None):
    n0 = OS.year_total()
    if chamfer is None:
        chamfer = chamfer_for(code)
    if n0 > LIMIT_A4:
        raise SystemExit(f"cupo: {n0} llamadas en el año, por encima de {LIMIT_A4}; paro antes de {code}")
    t0 = time.time()
    R = reg()
    did, wid = R["documento"]["did"], R["documento"]["wid"]
    rec = R.setdefault("piezas", {}).setdefault(code, {})
    a4 = rec.setdefault("a4", {})

    def keep():
        R["piezas"][code] = rec
        save(R)

    if redo and a4.get("drawing"):                                    # a previous A4 try: renamed, never deleted
        n_try = len(rec.get("a4_pruebas", [])) + 1
        c.call("POST", f"/metadata/d/{did}/w/{wid}/e/{a4['drawing']}",
               {"properties": [{"propertyId": ctx["name_pid"], "value": f"zz_A4_prueba{n_try}_{code}"}]})
        rec["a4_pruebas"] = rec.get("a4_pruebas", []) + [a4["drawing"]]
        a4.clear()
        keep()
    if rec.get("drawing") and not rec.get("a3_renombrado"):           # the A3 drawing of last night: renamed, kept
        if rec["drawing"] in ctx["elements"]:
            c.call("POST", f"/metadata/d/{did}/w/{wid}/e/{rec['drawing']}",
                   {"properties": [{"propertyId": ctx["name_pid"], "value": f"zz_A3_PLANO_{code}"}]})
            rec["a3_renombrado"] = f"zz_A3_PLANO_{code}"
        else:
            rec["a3_renombrado"] = "ya no estaba en el documento"
        keep()
    if "partstudio" not in rec:
        name, made = OP.push(step, code, did=did, wid=wid, client=c)
        rec["partstudio"] = next(u for n, typ, u in made if typ == "PARTSTUDIO").rsplit("/e/", 1)[1]
        rec["pestana"] = name
    eid = rec["partstudio"]
    if "pid" not in rec:
        rec["pid"] = c.call("GET", f"/parts/d/{did}/w/{wid}/e/{eid}")[0]["partId"]
    if "propiedades" not in rec:
        rec["propiedades"] = set_props(c, did, wid, eid, rec["pid"], code)
    keep()
    lo, hi = bbox(step)
    (num_, den), iso_s, centres, boxes = best_layout(lo, hi)
    with_back = "back" in centres
    s = num_ / den
    if "drawing" not in a4:
        d = c.call("POST", f"/drawings/d/{did}/w/{wid}/create", {
            "drawingName": f"PLANO_A4_{code}", "elementId": eid, "partId": rec["pid"], "views": "zero",
            "titleblock": True, "border": True, "units": "MILLIMETER", "projection": "First", "size": "A4",
            "standard": "ISO", "decimalSeparator": "COMMA"})
        a4["drawing"] = d["id"]
        keep()
    deid = a4["drawing"]
    if "cajetin" not in a4:
        md = c.call("GET", f"/metadata/d/{did}/w/{wid}/e/{deid}")
        ids = {p["name"]: p["propertyId"] for p in md.get("properties", [])}
        want = {k: v for k, v in CAJETIN(code).items() if k in ids}
        c.call("POST", f"/metadata/d/{did}/w/{wid}/e/{deid}",
               {"properties": [{"propertyId": ids[k], "value": v} for k, v in want.items()]})
        a4["cajetin"] = want
        a4["props_disponibles"] = sorted(ids)
        keep()
    if "vistas" not in a4:
        views = []
        for o, (x, y) in centres.items():
            sn, sd = iso_s if o == "isometric" else (num_, den)
            views.append({"viewType": "TopLevel", "position": {"x": x, "y": y}, "orientation": o,
                          "scale": {"scaleSource": "Custom", "numerator": sn, "denumerator": sd},
                          "reference": {"elementId": eid}})
        res = wait_modify(c, did, wid, deid, [{"messageName": "onshapeCreateViews", "formatVersion": "2021-01-01",
                                               "views": views}], f"vistas A4 {code}")
        a4["vistas"] = {o: r.get("viewId") for o, r in zip(centres, res.get("results", []))}
        keep()
    if "cotas" not in a4:
        info = {v["viewId"]: v for v in c.call("GET", f"/drawings/d/{did}/w/{wid}/e/{deid}/views")["items"]}
        anns, skipped, taken, used, vdata = [], [], [], {"d": set(), "r": set()}, {}
        ctr = [(lo[i] + hi[i]) / 2 / 1000 for i in range(3)]
        for o in ("front", "top", "left"):
            vid = a4["vistas"][o]
            vm = info[vid]["viewMatrix"]
            geom = c.call("GET", f"/drawings/d/{did}/w/{wid}/e/{deid}/views/{vid}/jsongeometry")["bodyData"]
            CACHE.mkdir(parents=True, exist_ok=True)               # to tune the placement offline, at no API cost
            (CACHE / f"{code}_{o}.json").write_text(json.dumps({"vm": vm, "geom": geom}), encoding="utf-8")
            blocked = [TITLE] + list(boxes.values())
            a, sk = dims_a4(o, vid, geom, boxes[o], project(vm, ctr), s, taken, blocked, used)
            anns += a
            skipped += sk
            vdata[o] = (vid, geom, boxes[o], project(vm, ctr))
        if chamfer:
            qn = f"Cantidad: {qty}   ·   Material: PETG   ·   Cotas en mm"
            qbox = (TITLE[0] + 1, TITLE[3] + 4 - TEXT_H - 1.5, TITLE[0] + 4 + text_w(qn, TEXT_H), TITLE[3] + 5)
            a, txt = chamfer_dim(vdata, s, chamfer, taken, [TITLE, qbox] + list(boxes.values()))
            anns += a
            a4["chaflan"] = txt
        anns += title_notes(code)
        note = f"Cantidad: {qty}   ·   Material: PETG   ·   Cotas en mm"
        anns.append({"type": "Onshape::Note", "note": {"position": {"type": "Onshape::Reference::Point",
                     "coordinate": [TITLE[0] + 2, TITLE[3] + 4, 0]}, "contents": note, "textHeight": TEXT_H}})
        res = wait_modify(c, did, wid, deid, [{"messageName": "onshapeCreateAnnotations", "formatVersion": "2021-01-01",
                                               "annotations": anns}], f"cotas A4 {code}")
        results = res.get("results", [])
        failed = [(a["type"].split("::")[-1], r.get("errorDescription")) for a, r in zip(anns, results) if r.get("status") != "OK"]
        sent = sum(1 for a in anns if "Dimension" in a["type"])
        a4["cotas"] = {"creadas": sum(1 for a, r in zip(anns, results) if r.get("status") == "OK" and "Dimension" in a["type"])
                       if results else sent, "fallidas": failed, **({} if results else {"sin_confirmacion": True}),
                       "a_mano": skipped}
        keep()
    pdf = OUT_A4 / f"PLANO_A4_{code}.pdf"
    OUT_A4.mkdir(parents=True, exist_ok=True)
    export_pdf(c, did, wid, deid, pdf)
    a4.update(escala=f"{num_}:{den}", escala_iso=f"{iso_s[0]}:{iso_s[1]}", posterior=with_back, cantidad=qty,
              pdf=str(pdf.relative_to(MOD)), url=f"https://cad.onshape.com/documents/{did}/w/{wid}/e/{deid}",
              llamadas=OS.year_total() - n0, segundos=round(time.time() - t0))
    keep()
    print(code, json.dumps({k: a4[k] for k in ("escala", "posterior", "cotas", "llamadas", "segundos")}, ensure_ascii=False))
    return a4


CHAMFERS = MOD / "salida" / "correccion_chaflan" / "chaflanes.json"


def chamfer_for(code):
    """Chamfer callout data. 04/11 night: built from params (chaflan.*, riel.canal_chaflan_techo, caja.ventana_chaflan)
    instead of the 01/11 list, which described the old supports. Only pieces that carry such a chamfer get one: buoy
    B1, B2, B3, B5 (base of the slender elements, 45 deg, chaflan.base_boya, up to its _max where it fits), M1s (base of
    the supports + window to the rail channel) and M3s (rail channel top corners). The others get no callout."""
    import params as PR
    def grp(c, groups, lines):
        return {"c": float(c), "texto": "Chaflanes a 45° (mm)", "grupos": groups, "lineas": ["Chaflanes a 45°:"] + lines}
    f = lambda v: f"{v:g}".replace(".", ",")
    if code.startswith(("B1_", "B2_", "B3_", "B5_")):
        c, cm = PR.PET_CHAMFER, PR.PET_CHAMFER_MAX
        return grp(c, {"base de los elementos esbeltos": [c, cm]}, [f"base de elementos esbeltos: {f(c)}", f"(hasta {f(cm)} donde cabe)"])
    if code == "M1s_caja_cuerpo":
        c, cm, w = PR.CHAMFER_BASE, PR.CHAMFER_BASE_MAX, PR.BOX_WINDOW_CHAMFER
        return grp(w, {"ventana al canal del riel (2 esquinas de arriba)": [w, w], "base de los soportes": [cm, c]},
                   [f"ventana al canal: {f(w)}", f"base de soportes: {f(c)} a {f(cm)}"])
    if code == "M3s_riel_gancho":
        t = PR.RAIL_CHAMFER_TOP
        return grp(t, {"canal del riel (2 esquinas de arriba)": [t, t]}, [f"esquinas del canal: {f(t)}"])
    if code in ("M5s_capsula_tapa_pie", "M3f_marco_bolsillo", "M11_bandeja"):
        c, cm = PR.CHAMFER_BASE, PR.CHAMFER_BASE_MAX
        return grp(c, {"base de los soportes": [c, cm]}, [f"base de soportes: {f(c)} a {f(cm)}"])
    return None


def chamfer_dim(vdata, s, ch, taken, blocked):
    """The chamfer callout 'Chaflán c x 45°', where the chamfer is seen:
    1. edge on in an elevation (a visible 45 deg segment of length c*sqrt2): aligned PointToPoint on its ends; Onshape
       writes the text along the segment, so its rotated box is tested against the lines of the views;
    2. from above (top view: the strip between a wall / post line and the foot line, two parallel lines c apart):
       LineToLine with the text beside it, in a free spot that crosses no line;
    3. otherwise only the note. A multi-line note with the size of every joint is always added in a free spot.
    Returns (annotations, what was done)."""
    from shapely.geometry import LineString, Polygon, box as sbox
    from shapely.strtree import STRtree
    sizes = sorted({v for vs in ch["grupos"].values() for v in vs if v > 0}, key=lambda v: (v != ch["c"], -v))
    segs_sheet, maps = [], {}
    for o, (vid, geom, vbox, cuv) in vdata.items():
        sx = lambda u, vb=vbox, cv=cuv: (vb[0] + vb[2]) / 2 + s * (u - cv[0])
        sy = lambda v, vb=vbox, cv=cuv: (vb[1] + vb[3]) / 2 + s * (v - cv[1])
        maps[o] = (sx, sy)
        L, C, A = view_parts(geom)
        segs_sheet += [LineString([(sx(a[0]), sy(a[1])), (sx(b[0]), sy(b[1]))]) for _, a, b in L]
        segs_sheet += [sbox(sx(cc[0]) - s * r, sy(cc[1]) - s * r, sx(cc[0]) + s * r, sy(cc[1]) + s * r).exterior for _, cc, r in C + A]
    tree = STRtree(segs_sheet)
    others = [b for b in blocked if b not in [v[2] for v in vdata.values()]]     # title block + views without geometry

    def free(poly):
        x0, y0, x1, y1 = poly.bounds
        if x0 < FRAME[0] + 1 or y0 < FRAME[1] + 1 or x1 > FRAME[2] - 1 or y1 > FRAME[3] - 1:
            return False
        if clash((x0, y0, x1, y1), taken + others):
            return False
        return not any(poly.intersects(segs_sheet[i]) for i in tree.query(poly))

    def rect(cx, cy, w, h, ang):
        ca, sa = math.cos(ang), math.sin(ang)
        return Polygon([(cx + ca * dx - sa * dy, cy + sa * dx + ca * dy) for dx, dy in
                        ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))])

    for c in sizes:
        lab = f"Chaflán {num(c)}x45°"
        w, h = text_w(lab, TEXT_H) + 2, TEXT_H + 2
        for o in ("front", "left", "top"):                                 # 1. edge on
            if o not in vdata:
                continue
            vid, geom = vdata[o][:2]
            sx, sy = maps[o]
            for e, a, b in view_parts(geom)[0]:
                if not (abs(abs(b[0] - a[0]) - abs(b[1] - a[1])) < 0.05 and abs(math.hypot(b[0] - a[0], b[1] - a[1]) - c * math.sqrt(2)) < 0.08):
                    continue
                p, q = (sx(a[0]), sy(a[1])), (sx(b[0]), sy(b[1]))
                ux, uy = (q[0] - p[0]), (q[1] - p[1])
                ln = math.hypot(ux, uy)
                ux, uy = ux / ln, uy / ln
                ang = math.atan2(uy, ux)
                if ang > math.pi / 2 or ang < -math.pi / 2:
                    ang -= math.copysign(math.pi, ang)
                mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
                for d in (6, 9, 12, 16, 20, 25, 30):
                    for sg in (1, -1):
                        for t in (0, 6, -6, 12, -12, 18, -18):
                            cx, cy = mx - sg * uy * d + ux * t, my + sg * ux * d + uy * t
                            if free(rect(cx, cy, w, h, ang)):
                                taken.append(rect(cx, cy, w, h, ang).bounds)
                                dd = e["data"]
                                return [{"type": "Onshape::Dimension::PointToPoint", "pointToPointDimension": {
                                    "point1": ref_pt(vid, e["uniqueId"], dd["start"], "ModeStart"),
                                    "point2": ref_pt(vid, e["uniqueId"], dd["end"], "ModeEnd"),
                                    "formatting": fmt(), "textOverride": lab, "textPosition": pt((cx, cy))}},
                                    note_free(ch["lineas"], 1.8, taken, blocked)], f"cota en la vista {o} (de canto): {lab}"
        if "top" in vdata:                                                   # 2. from above: strip of width c
            vid, geom = vdata["top"][:2]
            sx, sy = maps["top"]
            L = view_parts(geom)[0]
            for k in (0, 1):                                                 # k = 0: vertical lines (gap along u)
                ax = [ln for ln in L if abs(ln[1][k] - ln[2][k]) < 1e-3 and abs(ln[1][1 - k] - ln[2][1 - k]) > 3]
                pairs = []
                for i, l1 in enumerate(ax):
                    for l2 in ax[i + 1:]:
                        if abs(abs(l1[1][k] - l2[1][k]) - c) > 0.03:
                            continue
                        lo = max(min(l1[1][1 - k], l1[2][1 - k]), min(l2[1][1 - k], l2[2][1 - k]))
                        hi = min(max(l1[1][1 - k], l1[2][1 - k]), max(l2[1][1 - k], l2[2][1 - k]))
                        if hi - lo > 3:
                            pairs.append((hi - lo, l1, l2, lo, hi))
                pairs.sort(key=lambda g: -g[0])
                for _, l1, l2, lo, hi in pairs[:20]:
                    xs = sorted((l1[1][k], l2[1][k]))
                    for t in [0.5, 0.3, 0.7, 0.15, 0.85, -0.3, 1.3, -0.8, 1.8]:
                        along = lo + t * (hi - lo)
                        for d in (3, 6, 10, 14, 20, 26):
                            for sg in (-1, 1):
                                edge = xs[0] - d / s if sg < 0 else xs[1] + d / s
                                if k == 0:
                                    cx, cy = sx(edge) + sg * w / 2, sy(along)
                                    poly = rect(cx, cy, w, h, 0.0)
                                else:
                                    cx, cy = sx(along), sy(edge) + sg * w / 2
                                    poly = rect(cx, cy, w, h, math.pi / 2)
                                if free(poly):
                                    taken.append(poly.bounds)
                                    d2 = {"edge1": {"type": "Onshape::Reference::Edge", "viewId": vid, "uniqueId": l1[0]["uniqueId"]},
                                          "edge2": {"type": "Onshape::Reference::Edge", "viewId": vid, "uniqueId": l2[0]["uniqueId"]},
                                          "formatting": fmt(), "textOverride": lab, "textPosition": pt((cx, cy))}
                                    return [{"type": "Onshape::Dimension::LineToLine", "lineToLineDimension": d2},
                                            note_free(ch["lineas"], 1.8, taken, blocked)], f"cota en la vista superior (franja del chaflán): {lab}"
    return [note_free(ch["lineas"], 1.8, taken, blocked)], "solo nota (el chaflán no se encontró de canto ni desde arriba)"


NL = chr(10)


def note_free(lines, h, taken, blocked):
    """Multi-line note in the first free spot of the frame, scanning from the bottom-left corner (Onshape anchors a note
    at its top-left corner)."""
    w = max(text_w(ln, h) for ln in lines) + 2
    hh = len(lines) * 1.6 * h + 2
    for y in [FRAME[1] + 2 + hh + 4 * k for k in range(40)]:
        for x in [FRAME[0] + 3 + 6 * k for k in range(40)]:
            bx = (x, y - hh, x + w, y)
            if bx[2] <= FRAME[2] - 2 and bx[3] <= FRAME[3] - 2 and not clash(bx, taken + blocked):
                taken.append(bx)
                return {"type": "Onshape::Note", "note": {"position": pt((x, y)), "contents": NL.join(lines), "textHeight": h}}
    return {"type": "Onshape::Note", "note": {"position": pt((TITLE[0] + 2, TITLE[3] + 2 + hh)), "contents": NL.join(lines),
                                              "textHeight": h}}


def CAJETIN(code):
    """Drawing properties that fill the ISO title block (names as Onshape reports them; missing ones are ignored)."""
    # Onshape fills "Date drawn" with the creation time when "Drawn by" is set and prints it in the DATE cell; a plain
    # yyyy-mm-dd string is not a valid date for the API, so it clears the field, and the date is then a note (title_notes)
    # in the same cell: one date only, as Melissa's drawings show.
    return {"Title 1": code, "Drawn by": "Equipo 02 UPCH", "Description": f"{COMPANY} - {code}",
            "Date drawn": time.strftime("%Y-%m-%d")}


def a4_context(c):
    R = reg()
    did, wid = R["documento"]["did"], R["documento"]["wid"]
    els = {e["id"]: e["name"] for e in c.call("GET", f"/documents/d/{did}/w/{wid}/elements")}
    md = c.call("GET", f"/metadata/d/{did}/w/{wid}/e/{next(iter(els))}")
    name_pid = next(p["propertyId"] for p in md["properties"] if p["name"] == "Name")
    return {"elements": els, "name_pid": name_pid}


def melissa_b1(c):
    """Her B1_casco drawing exported as it is (read only: the PDF is not stored in the document)."""
    R = reg()
    did, wid = R["documento"]["did"], R["documento"]["wid"]
    OUT_A4.mkdir(parents=True, exist_ok=True)
    pdf = OUT_A4 / "PLANO_A4_B1_casco.pdf"
    export_pdf(c, did, wid, MELISSA_B1, pdf)
    return pdf


def merge_a4(melissa=None, tag="v4"):
    """Cover + the current A4 drawings -> PLANOS_A4_LanternGuard_<tag>.pdf. Pieces drawn by this script use their own PDF;
    those in `melissa` ({code: (pdf path, label)}) are unchanged pieces and keep their earlier PDF. The cover lists,
    per piece, the dimensions that the script could not place."""
    import html
    import subprocess
    import tempfile
    from pypdf import PdfReader, PdfWriter
    from entrega_pdf import EDGE
    R = reg()
    melissa = melissa or {}
    rows, files, md = [], [], ["# Cotas que no se pudieron poner automáticamente (planos A4)", ""]
    order = [(cd, q) for cd, _, q in a4_pieces()]
    for code, q in order:
        a4 = R.get("piezas", {}).get(code, {}).get("a4", {})
        if code in melissa:
            f = melissa[code][0]
            esc, n, mano = "-", "-", f"pieza sin cambios: se conserva su plano ({melissa[code][1]})"
        else:
            f = MOD / a4["pdf"] if a4.get("pdf") else None
            esc = {"2:5": "1:2,5"}.get(a4.get("escala"), a4.get("escala", "-"))
            n = a4.get("cotas", {}).get("creadas", "-")
            mano = "; ".join(a4.get("cotas", {}).get("a_mano", []) + [f"falló {t}: {e}" for t, e in a4.get("cotas", {}).get("fallidas", [])]) or "ninguna"
        ok = f is not None and Path(f).exists()
        if ok:
            files.append(f)
        md += [f"## {code} (escala {esc}, {n} cotas automáticas)", ""] + [f"- {x}" for x in mano.split("; ")] + [""]
        rows.append(f"<tr><td class=c>{len(files) if ok else '-'}</td><td><b>{html.escape(code)}</b></td>"
                    f"<td class=c>{q}</td><td class=c>{esc}</td><td class=c>{n}</td>"
                    f"<td>{html.escape(mano) if ok else 'plano no generado'}</td></tr>")
    page = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
@page {{ size: A4 landscape; margin: 10mm; }}
body {{ font-family: "Segoe UI", Arial, sans-serif; font-size: 8.5pt; color: #1b1b1b; }}
h1 {{ font-size: 18pt; margin: 0; }} .sub {{ font-size: 10pt; color: #444; margin: 2pt 0 8pt; }}
table {{ border-collapse: collapse; width: 100%; }} th, td {{ border: 1px solid #bbb; padding: 2pt 4pt; vertical-align: top; }}
th {{ background: #e8eef3; text-align: left; }} .c {{ text-align: center; }}
</style></head><body>
<h1>LANTERNGUARD · planos de fabricación (formato del equipo)</h1>
<div class="sub">Equipo 02 UPCH · PETG · ISO A4 horizontal, primer diedro, cotas en mm · {time.strftime('%d/%m/%Y')} ·
documento Onshape LG_IMPRIMIR_P2: {html.escape(R['documento']['url'])}</div>
<table><tr><th>Hoja</th><th>Pieza</th><th>Cant.</th><th>Escala</th><th>Cotas auto</th>
<th>Cotas que no se pudieron poner automáticamente (completar a mano en Onshape)</th></tr>{''.join(rows)}</table>
</body></html>"""
    tmp = Path(tempfile.mkdtemp(prefix="portada_a4_"))
    (tmp / "p.html").write_text(page, encoding="utf-8")
    cover = OUT_A4 / "portada_A4.pdf"
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={tmp / 'perfil'}",
                    "--no-pdf-header-footer", f"--print-to-pdf={cover}", (tmp / "p.html").as_uri()], capture_output=True, timeout=180)
    w = PdfWriter()
    for f in [cover] + files:
        for pg in PdfReader(str(f)).pages:
            w.add_page(pg)
    (OUT / f"COTAS_A_MANO_A4_{tag}.md").write_text("\n".join(md), encoding="utf-8")
    out = OUT / f"PLANOS_A4_LanternGuard_{tag}.pdf"
    with open(out, "wb") as fh:
        w.write(fh)
    print(out, len(w.pages), "paginas,", len(files), "planos")
    return out


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


BUOY_NAMES = {"B1_casco": "B1 casco de la boya", "B2_cubierta": "B2 cubierta de la boya",
              "B3_caja": "B3 caja de electrónica", "B4_tapa": "B4 tapa de la caja", "B5_cuna": "B5 cuna de las botellas",
              "B6_correa": "B6 correa de las botellas"}


def merge():
    """Cover (index of pieces, quantities, scale, dimensions left for hand) + every drawing PDF, in PIECES order."""
    import html
    import subprocess
    import tempfile
    from pypdf import PdfReader, PdfWriter
    from entrega_pdf import EDGE
    R = reg()
    names = json.loads((P2 / "resultados.json").read_text(encoding="utf-8"))["piezas"]
    rows, files = [], []
    for i, (code, _, _, q) in enumerate(PIECES, 1):
        rec = R.get("piezas", {}).get(code, {})
        pdf = MOD / rec["pdf"] if rec.get("pdf") else None
        ok = pdf is not None and pdf.exists()
        if ok:
            files.append(pdf)
        desc = names[code]["nombre"] if code in names else BUOY_NAMES.get(code, "boya PET 4 x 1 L")
        esc = {"2:5": "1:2.5"}.get(rec.get("escala"), rec.get("escala", "-"))
        mano = "; ".join(rec.get("cotas", {}).get("a_mano", [])) or "ninguna"
        rows.append(f"<tr><td>{len(files) + 1 if ok else '-'}</td><td><b>{html.escape(code)}</b></td><td>{html.escape(desc)}</td>"
                    f"<td class=c>{q}</td><td class=c>{esc}</td>"
                    f"<td class=c>{rec.get('cotas', {}).get('creadas', '-')}</td><td>{html.escape(rec.get('espesor', '-'))}</td>"
                    f"<td>{html.escape(mano) if ok else 'plano no generado'}</td></tr>")
    doc = R["documento"]["url"]
    page = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
@page {{ size: A3 landscape; margin: 14mm; }}
body {{ font-family: "Segoe UI", Arial, sans-serif; font-size: 10.5pt; color: #1b1b1b; }}
h1 {{ font-size: 26pt; margin: 0; }} .sub {{ font-size: 13pt; color: #444; margin: 2pt 0 14pt; }}
table {{ border-collapse: collapse; width: 100%; }} th, td {{ border: 1px solid #bbb; padding: 4pt 6pt; vertical-align: top; }}
th {{ background: #e8eef3; text-align: left; }} .c {{ text-align: center; }} .n {{ font-size: 9.5pt; color: #333; margin-top: 12pt; }}
</style></head><body>
<h1>LanternGuard: planos de impresión de P2 + boya PET 4 x 1 L</h1>
<div class="sub">Equipo 02 UPCH · material PETG · A3, primer diedro, cotas en mm · generado desde Onshape el {time.strftime('%d/%m/%Y')}</div>
<table><tr><th>Hoja</th><th>Pieza</th><th>Descripción</th><th>Cantidad</th><th>Escala</th><th>Cotas</th><th>Espesor</th>
<th>Cotas que faltan (a mano)</th></tr>{''.join(rows)}</table>
<p class="n">Cantidades para un nodo P2 y una boya. "Hoja" es la página de este PDF. M7 (ventana) no está:
es de acrílico, no se imprime. Las cotas son automáticas y solo cubren medidas generales, diámetros de agujeros, alto total y
un espesor; lo que falta para fabricar se mide en el modelo de Onshape: {html.escape(doc)}</p>
</body></html>"""
    tmp = Path(tempfile.mkdtemp(prefix="portada_"))
    (tmp / "p.html").write_text(page, encoding="utf-8")
    cover = OUT / "portada.pdf"
    subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", f"--user-data-dir={tmp / 'perfil'}",
                    "--no-pdf-header-footer", f"--print-to-pdf={cover}", (tmp / "p.html").as_uri()], capture_output=True, timeout=180)
    w = PdfWriter()
    for f in [cover] + files:
        for pg in PdfReader(str(f)).pages:
            w.add_page(pg)
    out = OUT / "PLANOS_ONSHAPE_P2.pdf"
    with open(out, "wb") as fh:
        w.write(fh)
    print(out, len(w.pages), "paginas,", len(files), "planos")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--documento", action="store_true")
    ap.add_argument("--pieza")
    ap.add_argument("--todas", action="store_true")
    ap.add_argument("--unir", action="store_true")
    ap.add_argument("--rehacer", action="store_true", help="renombra el Drawing anterior a zz_obsoleto_ y hace uno nuevo")
    ap.add_argument("--formato", choices=["a3", "equipo"], default="a3",
                    help="equipo: ISO A4 horizontal como el B1_casco de Melissa, pestañas PLANO_A4_<pieza>")
    ap.add_argument("--melissa", action="store_true", help="con --formato equipo: exporta el B1 de Melissa tal cual")
    a = ap.parse_args()
    if a.formato == "equipo":
        use_format("equipo")
        c = client() if (a.pieza or a.todas or a.melissa) else None
        ctx = a4_context(c) if (a.pieza or a.todas) else None
        todo = [p for p in a4_pieces() if a.todas or p[0] in (a.pieza or "").split(",")]
        for code, step, q in todo:
            if a.todas and reg().get("piezas", {}).get(code, {}).get("a4", {}).get("pdf"):
                continue
            try:
                piece_a4(code, step, q, c, ctx, redo=a.rehacer)
            except (OS.OnshapeError, KeyError, IndexError, StopIteration) as e:   # a stuck piece stays as it is
                print(code, "FALLO:", str(e)[:300])
        if a.melissa:
            print(melissa_b1(c))
        if a.unir:
            merge_a4()
        return 0
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
    if a.unir:
        merge()
    return 0


if __name__ == "__main__":
    sys.exit(main())
