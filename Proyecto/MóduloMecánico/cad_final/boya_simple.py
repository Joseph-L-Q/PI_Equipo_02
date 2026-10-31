"""Our buoy for the simple version (B1s..B6s), from the team decisions of 29/10 (params.py, boya.*).

    python boya_simple.py        (from cad_final/)
Dry sealed box boya.caja_exterior (body + lid; the lid flange sticks out), battery low and centred, tray with the PCB
(Heltec LoRa V3), the Waveshare D and the RTC, the small LoRa antenna inside at the end that is not under the panel,
lid with O-ring, panel 170 x 170 on two rails, umbilical PG7 in the floor, solar PG7 in the -X wall, blind boss for a
future SMA in the +X wall, mooring eye under the +X end (independent of the umbilical), 4 hollow corner floats bolted
with long M5 to inserts in pads of the end walls (the box is never pierced). Every piece fits the 256 bed.
Hydrostatics with seawater (agua.densidad): draft by bisection on the real immersed volume, freeboard, reserve,
KB, BM, KG and GM.
Outputs: salida/simple/boya/ (stl/, step/, ENSAMBLE_boya_simple.step, renders), cad_final/reporte_boya_simple.md and
salida/simple/boya/resultados_boya.json.
Frame: box bottom z = 0, X along the long side, panel offset to -X.
"""
import json
import math
from pathlib import Path

import cadquery as cq

import fase_a as FA
import params as P
from checks import brep_check, export_part, fix_step_stamp, mesh_checks, sanitize

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "salida" / "simple" / "boya"
RHO = P.SEAWATER_DENSITY * 1e-3          # g/mm3
L, Wd, H = P.BUOY_BOX                     # body exterior and total height with the lid
LI, WI = P.BUOY_BOX_IN
WALL = (L - LI) / 2
FLOOR = WALL
LID_T = P.BOX_LID_T
HB = H - LID_T                            # body height
FL_W, FL_T = P.BOX_FLANGE, P.BOX_FLANGE_T
FX, FY, FH = P.BUOY_FLOAT_S
F_WALL, F_GAP = 2.0, 10.0                 # float wall; float to end wall (the M5 pads)
PANEL_X = -30.0                           # panel centre: the +X end of the lid stays free for the antenna
ANT = (12.0, 12.0, 60.0)                  # keep-out of the small Heltec antenna inside (estimated)
M5_INS = (6.4, 10.0)                      # M5 heat insert hole and depth in the float pads
ORIENT = {"sin girar": None, "X180": ("X", 180), "X+90": ("X", 90), "Y+90": ("Y", 90)}


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def cyl(p, d, r, h):
    return cq.Workplane().add(cq.Solid.makeCylinder(r, h, cq.Vector(*p), cq.Vector(*d)))


def rbox(lx, ly, z0, h, r):
    return cq.Workplane("XY").workplane(offset=z0).rect(lx, ly).extrude(h).edges("|Z").fillet(r)


def float_centres():
    xc = L / 2 + F_GAP + FX / 2
    yc = Wd / 2 - FY / 2 + 20.0               # the float sticks out 20 past the long side: corner float
    return [(sx * xc, sy * yc) for sx in (1, -1) for sy in (1, -1)]


def float_bolts():
    """(x pad face, y, z) of the 2 M5 of each float on the end wall."""
    out = []
    for xc, yc in float_centres():
        sx = 1 if xc > 0 else -1
        for dy in (-25.0, 25.0):
            out.append((sx, yc + dy, FH / 2))
    return out


def screw_pts():
    """M3 of the lid on the flange, at most BOX_SCREW_PITCH apart."""
    a, b = L / 2 + FL_W / 2, Wd / 2 + FL_W / 2
    nx, ny = math.ceil(2 * a / P.BOX_SCREW_PITCH), math.ceil(2 * b / P.BOX_SCREW_PITCH)
    pts = {(round(-a + 2 * a * i / nx, 3), sy * b) for i in range(nx + 1) for sy in (1, -1)}
    pts |= {(sx * a, round(-b + 2 * b * j / ny, 3)) for j in range(ny + 1) for sx in (1, -1)}
    return sorted(pts)


def layout():
    """Internal parts (box frame): battery holder, tray, PCB zone, Waveshare, RTC, antenna, glands."""
    bl, bw, bh = P.BUOY_BATT_HOLDER
    zb0 = FLOOR + P.BUOY_BATT_STANDOFF
    zt = zb0 + bh + P.BUOY_TRAY_GAP
    pl, pw, _ = P.BUOY_PCB
    wl, ww, wh = P.BUOY_WAVESHARE
    rl, rw, rh = P.BUOY_RTC
    g = dict(batt=(-bl / 2, bl / 2, -bw / 2, bw / 2, zb0, zb0 + bh), tray_z=(zt, zt + 3.0),
             pcb=(-LI / 2 + 6, -LI / 2 + 6 + pl, -pw / 2, pw / 2, zt + 3, zt + 3 + P.BUOY_TOP_COMP_H),
             ws=(10.0, 10.0 + wl, 20.0, 20.0 + ww, zt + 3, zt + 3 + wh),
             rtc=(10.0, 10.0 + rl, -20.0 - rw, -20.0, zt + 3, zt + 3 + rh),
             ant=(LI / 2 - 8 - ANT[0], LI / 2 - 8, -ANT[1] / 2, ANT[1] / 2, zt + 8.0, zt + 8.0 + ANT[2]),
             umb=(-LI / 2 + 30.0, 0.0), solar=(25.0, 75.0), sma=(-25.0, HB - 25.0))
    return g


def b1_casco():
    c = rbox(L, Wd, 0, HB, 10).cut(rbox(LI, WI, FLOOR, HB, 6))
    c = c.union(rbox(L + 2 * FL_W, Wd + 2 * FL_W, HB - FL_T, FL_T, 12).cut(rbox(LI, WI, HB - FL_T - 1, FL_T + 2, 6)))
    for x, y in screw_pts():
        c = c.cut(cyl((x, y, HB - P.M3_INSERT_DEPTH), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
    g = layout()
    # 4 M3 standoffs of the battery holder, 4 tray posts
    hx, hy = P.BUOY_HOLDER_HOLES
    for sx in (1, -1):
        for sy in (1, -1):
            c = c.union(cyl((sx * hx / 2, sy * hy / 2, FLOOR - 0.1), (0, 0, 1), 4.5, P.BUOY_BATT_STANDOFF + 0.1))
            c = c.cut(cyl((sx * hx / 2, sy * hy / 2, FLOOR + P.BUOY_BATT_STANDOFF - P.M3_INSERT_DEPTH), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
            px, py = sx * (LI / 2 - P.BUOY_POST_D / 2 - P.BUOY_POST_WALL_GAP), sy * (WI / 2 - P.BUOY_POST_D / 2 - P.BUOY_POST_WALL_GAP)
            c = c.union(cyl((px, py, FLOOR - 0.1), (0, 0, 1), P.BUOY_POST_D / 2, g["tray_z"][0] - FLOOR + 0.1))
            c = c.cut(cyl((px, py, g["tray_z"][0] - P.M3_INSERT_DEPTH), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
    # umbilical PG7 in the floor, solar PG7 in the -X wall, blind SMA boss in the +X wall (not drilled through)
    ux, uy = g["umb"]
    c = c.cut(cyl((ux, uy, -1), (0, 0, 1), P.PG7_HOLE / 2, FLOOR + 2))
    sy_, sz_ = g["solar"]
    c = c.cut(cyl((-L / 2 - 1, sy_, sz_), (1, 0, 0), P.PG7_HOLE / 2, WALL + 2))
    smy, smz = g["sma"]
    c = c.union(cyl((L / 2 - 0.1, smy, smz), (1, 0, 0), 7.0, 4.1))
    c = c.cut(cyl((L / 2 + 4.0 + 0.01, smy, smz), (-1, 0, 0), P.BUOY_SMA_HOLE / 2, 4.0 + WALL - 1.2))
    # float pads on the end walls: M5 inserts, 2 per float
    for sx, y, z in float_bolts():
        x0 = sx * L / 2
        c = c.union(cyl((x0 - sx * 0.5, y, z), (sx, 0, 0), 7.0, F_GAP + 0.5))
        c = c.cut(cyl((x0 + sx * (F_GAP + 0.01), y, z), (-sx, 0, 0), M5_INS[0] / 2, M5_INS[1]))
    # mooring boss under the +X end: M5 insert from below
    c = c.union(cyl((L / 2 - 30, 0, -10), (0, 0, 1), 9.0, 10.1))
    c = c.cut(cyl((L / 2 - 30, 0, -10.01), (0, 0, 1), M5_INS[0] / 2, M5_INS[1]))
    return c


def b2_tapa():
    t = rbox(L + 2 * FL_W, Wd + 2 * FL_W, HB, LID_T, 12)
    for x, y in screw_pts():
        t = t.cut(cyl((x, y, HB - 1), (0, 0, 1), P.M3_CLEAR / 2, LID_T + 2))
    cl_l, cl_w = (LI + L) / 2, (WI + Wd) / 2
    groove = rbox(cl_l + P.GROOVE_WIDTH, cl_w + P.GROOVE_WIDTH, HB, P.GROOVE_DEPTH, 8).cut(
        rbox(cl_l - P.GROOVE_WIDTH, cl_w - P.GROOVE_WIDTH, HB - 0.1, P.GROOVE_DEPTH + 0.2, 5))
    t = t.cut(groove)
    for x, y in rail_feet():
        t = t.union(cyl((x, y, HB + LID_T - 0.1), (0, 0, 1), 5.0, 4.1))
        t = t.cut(cyl((x, y, HB + LID_T + 4.0 - P.M3_INSERT_DEPTH), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
    return t


def rail_x():
    pl = P.BUOY_PANEL[0]
    return [PANEL_X - pl / 2 + 15.0, PANEL_X + pl / 2 - 15.0]


def rail_feet():
    return [(x, sy * 60.0) for x in rail_x() for sy in (1, -1)]


def b3_larguero(x):
    """Rail along Y under the panel: 2 legs on the lid bosses (M3 into inserts), top with 2 M3 inserts for the panel."""
    w = P.BUOY_RAIL[0]
    ln = P.BUOY_PANEL[1]
    z0 = HB + LID_T + 4.0
    lift = P.BUOY_PANEL_LIFT_USED - 4.0
    top = box(x - w / 2, x + w / 2, -ln / 2, ln / 2, z0 + lift - 6.0, z0 + lift)
    for sy in (1, -1):
        top = top.union(cyl((x, sy * 60.0, z0), (0, 0, 1), P.BUOY_LEG_D / 2, lift - 5.9))
        top = top.cut(cyl((x, sy * 60.0, z0 - 1), (0, 0, 1), P.M3_CLEAR / 2, lift + 2))
        top = top.cut(cyl((x, sy * 60.0, z0 + lift - P.BUOY_CBORE[1]), (0, 0, 1), P.BUOY_CBORE[0] / 2, P.BUOY_CBORE[1] + 0.1))
        top = top.cut(cyl((x, sy * P.BUOY_PANEL_HOLE_Y, z0 + lift - P.M3_INSERT_DEPTH), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
    return top


def b1b_bandeja():
    g = layout()
    z0, z1 = g["tray_z"]
    t = rbox(LI - 2 * P.GAP_WALL, WI - 2 * P.GAP_WALL, z0, z1 - z0, 4)
    for sx in (1, -1):
        for sy in (1, -1):
            px, py = sx * (LI / 2 - P.BUOY_POST_D / 2 - P.BUOY_POST_WALL_GAP), sy * (WI / 2 - P.BUOY_POST_D / 2 - P.BUOY_POST_WALL_GAP)
            t = t.cut(cyl((px, py, z0 - 1), (0, 0, 1), P.M3_CLEAR / 2, z1 - z0 + 2))
    ux, uy = g["umb"]
    return t.cut(cyl((ux, uy, z0 - 1), (0, 0, 1), 14.0, z1 - z0 + 2))       # cable of the umbilical goes up here


def b5_flotador(xc, yc):
    """Hollow corner float, sealed (printed closed with a Ø10 fill hole plugged after; foam optional), 2 sealed tubes
    for the M5 bolts across it along X."""
    sx = 1 if xc > 0 else -1
    f = rbox(FX, FY, 0, FH, 10).translate((xc, yc, 0)).cut(rbox(FX - 2 * F_WALL, FY - 2 * F_WALL, F_WALL, FH - 2 * F_WALL, 8).translate((xc, yc, 0)))
    for dy in (-25.0, 25.0):
        f = f.union(cyl((xc - FX / 2, yc + dy, FH / 2), (1, 0, 0), 5.0, FX))
        f = f.cut(cyl((xc - FX / 2 - 1, yc + dy, FH / 2), (1, 0, 0), 2.9, FX + 2))
    return f.cut(cyl((xc, yc, FH - F_WALL - 0.5), (0, 0, 1), 5.0, F_WALL + 1))


def b6_ojal():
    e = box(L / 2 - 45, L / 2 - 15, -12, 12, -16, -10).union(
        cq.Workplane("XZ").workplane(offset=-6).center(L / 2 - 30, -24).circle(12).circle(6).extrude(12))
    e = e.union(box(L / 2 - 38, L / 2 - 22, -6, 6, -24, -16))
    return e.cut(cyl((L / 2 - 30, 0, -17), (0, 0, 1), 2.75, 8))


def dummies():
    g = layout()
    pl, pw, pt = P.BUOY_PANEL
    out = {k: box(*g[k]) for k in ("batt", "pcb", "ws", "rtc", "ant")}
    out["panel"] = box(PANEL_X - pl / 2, PANEL_X + pl / 2, -pw / 2, pw / 2, HB + LID_T + 4 + P.BUOY_PANEL_LIFT_USED - 4,
                       HB + LID_T + 4 + P.BUOY_PANEL_LIFT_USED - 4 + pt)
    return out


def process(name, stem, wp, qty):
    shp = sanitize(wp)
    chk = brep_check(shp)
    export_part(shp, stem, OUT / "stl", OUT / "step")
    best = None
    for on, o in ORIENT.items():
        mc = mesh_checks(str(OUT / "stl" / f"{stem}.stl"), P.PRINT_BED, o)
        if mc["fits_bed"] and (best is None or mc["overhang_mm2"] < best[1]["overhang_mm2"]):
            best = (on, mc)
    if best is None:
        best = ("no cabe", mesh_checks(str(OUT / "stl" / f"{stem}.stl"), P.PRINT_BED, None))
    return dict(name=name, stem=stem, shape=shp, chk=chk, orient=best[0], mc=best[1], qty=qty)


def immersed(envs, T):
    hs = box(-2000, 2000, -2000, 2000, -500, T).val()
    v, mz = 0.0, 0.0
    for e in envs:
        i = e.intersect(hs)
        vi = i.Volume()
        if vi > 0:
            v += vi
            mz += vi * i.Center().z
    return v, (mz / v if v else 0.0)


def main():
    for d in (OUT / "stl", OUT / "step"):
        d.mkdir(parents=True, exist_ok=True)
    fails = []
    infill = {"B1s": 1.0, "B2s": 1.0, "B1bs": 0.4, "B3s": 0.4, "B5s": 1.0, "B6s": 1.0}
    rows = [process("B1s casco", "B1s_casco", b1_casco(), 1), process("B2s tapa", "B2s_tapa", b2_tapa(), 1),
            process("B1bs bandeja", "B1bs_bandeja", b1b_bandeja(), 1),
            process("B3s larguero del panel", "B3s_larguero", b3_larguero(rail_x()[0]), 2),
            process("B5s flotador de esquina", "B5s_flotador", b5_flotador(*float_centres()[0]), 4),
            process("B6s ojal de amarre", "B6s_ojal", b6_ojal(), 1)]
    for r in rows:
        ok = r["chk"]["ok"] and r["mc"]["watertight"] and r["mc"]["bodies"] == 1 and r["mc"]["fits_bed"]
        if not ok:
            fails.append(f"{r['stem']}: brep={r['chk']} estanco={r['mc']['watertight']} cama={r['mc']['fits_bed']}")
        print(f"{r['stem']:16s} ok={ok} or={r['orient']} bbox={tuple(round(v, 1) for v in r['mc']['bbox'])}", flush=True)
    S = {r["stem"]: r["shape"] for r in rows}
    floats = [S["B5s_flotador"]] + [sanitize(b5_flotador(*c)) for c in float_centres()[1:]]
    rails = [S["B3s_larguero"], sanitize(b3_larguero(rail_x()[1]))]
    parts = {"B1s casco": S["B1s_casco"], "B2s tapa": S["B2s_tapa"], "B1bs bandeja": S["B1bs_bandeja"], "B6s ojal": S["B6s_ojal"]}
    parts.update({f"B3s larguero {i + 1}": r for i, r in enumerate(rails)})
    parts.update({f"B5s flotador {i + 1}": f for i, f in enumerate(floats)})
    dm = {k: v.val() for k, v in dummies().items()}

    # interferences (pieces and dummies)
    allp = {**parts, **{f"dummy {k}": v for k, v in dm.items()}}
    names = list(allp)
    inter = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if a.startswith("dummy") and b.startswith("dummy"):
                continue
            v = allp[a].intersect(allp[b]).Volume()
            if v > P.INTERF_TOL:
                inter.append((a, b, v))
    for a, b, v in inter:
        fails.append(f"interferencia {a} / {b}: {v:.2f} mm3")

    # masses with their z
    bm = P.BUOY_MASS
    m_pts = []
    for k, sh in parts.items():
        key = k.split()[0]
        m_pts.append((k, FA.mass_g(sh, infill[key]), sh.Center().z))
    g = layout()
    comp = [("3 x celdas 18650", P.BUOY_CELLS * bm["celda_18650"], (g["batt"][4] + g["batt"][5]) / 2),
            ("portabaterias", bm["portabaterias"], (g["batt"][4] + g["batt"][5]) / 2),
            ("PCB + Heltec", bm["pcb_heltec"], (g["pcb"][4] + g["pcb"][5]) / 2),
            ("Waveshare D", bm["waveshare"], (g["ws"][4] + g["ws"][5]) / 2), ("RTC", bm["rtc"], (g["rtc"][4] + g["rtc"][5]) / 2),
            ("panel solar", bm["panel"], dm["panel"].Center().z), ("antena LoRa (dentro)", bm["antena"], (g["ant"][4] + g["ant"][5]) / 2),
            ("cables y fusible", bm["cables_fusible"], 50.0), ("2 PG7", bm["prensaestopas"], 30.0),
            ("tornilleria (M3, 8 M5 largos, insertos)", bm["tornilleria"] + 8 * 6.0, 50.0)]
    m_pts += comp
    M = sum(m for _, m, _ in m_pts)
    KG = sum(m * z for _, m, z in m_pts) / M
    # hydrostatics: sealed envelopes = box body + flange + lid, and the 4 floats
    env_box = rbox(L, Wd, 0, HB, 10).union(rbox(L + 2 * FL_W, Wd + 2 * FL_W, HB - FL_T, FL_T + LID_T, 12)).val()
    env_f = [rbox(FX, FY, 0, FH, 10).translate((xc, yc, 0)).val() for xc, yc in float_centres()]
    envs = [env_box] + env_f
    lo, hi = 0.0, H
    for _ in range(40):
        T = (lo + hi) / 2
        v, _ = immersed(envs, T)
        lo, hi = (T, hi) if RHO * v < M else (lo, T)
    T = (lo + hi) / 2
    V, KB = immersed(envs, T)
    V_tot = sum(e.Volume() for e in envs)
    fb = H - T
    if fb < P.BUOY_FREEBOARD_MIN:
        fails.append(f"francobordo {fb:.1f} mm < {P.BUOY_FREEBOARD_MIN:g}")
    # waterplane inertia (rectangles; rounded corners ignored)
    rects = [(0.0, 0.0, L, Wd)] + [(xc, yc, FX, FY) for xc, yc in float_centres()] if T < FH else [(0.0, 0.0, L, Wd)]
    Ixx = sum(b * h ** 3 / 12 + b * h * y ** 2 for x, y, b, h in rects)
    Iyy = sum(h * b ** 3 / 12 + b * h * x ** 2 for x, y, b, h in rects)
    BMr, BMp = Ixx / V, Iyy / V
    GMr, GMp = KB + BMr - KG, KB + BMp - KG
    if min(GMr, GMp) <= 0:
        fails.append(f"GM negativo ({GMr:.0f} / {GMp:.0f})")
    res_node = json.loads((HERE.parent / "salida" / "simple" / "resultados.json").read_text(encoding="utf-8"))
    node_g = res_node["peso"]["40"]["aire_g"]
    total = node_g + M
    over = total - P.AIR_MASS_MAX_KG * 1000

    # assembly STEP (named) and renders
    asm = cq.Assembly(name="boya_simple")
    for k, sh in parts.items():
        asm.add(sh, name=k.replace(" ", "_"))
    for k, sh in dm.items():
        asm.add(sh, name=f"ref_{k}")
    asm.export(str(OUT / "ENSAMBLE_boya_simple.step"))
    fix_step_stamp(OUT / "ENSAMBLE_boya_simple.step")
    from render import render
    col = lambda k: "#3a7ca5" if k.startswith("B1s") else "#9fb7cc" if k.startswith("B2s") else "#e07b39" if k.startswith("B5s") else "#3a9d7a"  # noqa: E731
    items = [(sh, col(k), 0.5 if k.startswith("B2s") else 1.0, True, None) for k, sh in parts.items()]
    items += [(sh, "#1d1d3a" if k == "panel" else "#c9a227", 1.0, True, None) for k, sh in dm.items()]
    water = box(-300, 300, -200, 200, T - 0.5, T).val()
    render(items + [(water, "#7fb3d5", 0.25, False, None)], OUT / "boya_simple_iso.png", "iso",
           f"Boya simple: calado {T:.0f} mm, francobordo {fb:.0f} mm, {M:.0f} g")
    cut = box(-400, 400, -400, 0, -100, 400).val()      # keep y > 0: the front view looks at the cut face
    render([(sh.cut(cut), c, 1.0, True, None) for sh, c, *_ in items if sh.cut(cut).Volume() > 1e-3]
           + [(water.cut(cut), "#7fb3d5", 0.25, False, None)], OUT / "boya_simple_corte.png", "frontal",
           "Corte en y = 0 de la boya simple con la linea de agua")

    res = dict(masa_g=M, KG=KG, calado=T, francobordo=fb, V=V / 1000, V_sellado=V_tot / 1000, reserva=(V_tot - V) / V,
               KB=KB, BM=[BMr, BMp], GM=[GMr, GMp], nodo_g=node_g, total_g=total, exceso_g=max(0.0, over),
               piezas={r["stem"]: dict(nombre=r["name"], qty=r["qty"], orient=r["orient"], bbox=list(r["mc"]["bbox"]),
                                       voladizo_mm2=r["mc"]["overhang_mm2"], volumen_cm3=r["shape"].Volume() / 1000,
                                       relleno=infill[r["stem"].split("_")[0]],
                                       masa_g=FA.mass_g(r["shape"], infill[r["stem"].split("_")[0]])) for r in rows},
               fallas=fails)
    (OUT / "resultados_boya.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    write_report(rows, m_pts, res, inter, fails)
    print(f"boya {M:.0f} g, calado {T:.1f}, francobordo {fb:.1f}, reserva {res['reserva'] * 100:.0f} %, GM {GMr:.0f}/{GMp:.0f}, "
          f"nodo+boya {total:.0f} g ({'+' if over > 0 else ''}{over:.0f} sobre 3 kg)")
    print("FALLAS:", fails if fails else "ninguna")
    return 1 if fails else 0


def write_report(rows, m_pts, r, inter, fails):
    Ls = ["# Boya de la version simple, B1s..B6s (generado por `boya_simple.py`)", "",
          "Decisiones del equipo del 29/10 (chat de Melissa, `params.py` boya.*): caja hermetica de "
          f"{L:g} × {Wd:g} × {H:g} exterior (cuerpo; la brida de la tapa sale {FL_W:g} por lado: {L + 2 * FL_W:g} × {Wd + 2 * FL_W:g}), "
          f"{LI:g} × {WI:g} interior, pared {WALL:g}; panel {P.BUOY_PANEL[0]:g} × {P.BUOY_PANEL[1]:g} a {P.BUOY_PANEL_LIFT_USED:g} sobre la tapa, "
          f"corrido a -X para que la antena LoRa (dentro, en el extremo +X) no quede bajo el panel; {P.BUOY_CORNER_FLOATS} flotadores "
          f"huecos de {FX:g} × {FY:g} × {FH:g} en las esquinas, atornillados con 2 M5 largos cada uno a insertos en cojines de las "
          "paredes extremas (la caja no se perfora); PG7 del umbilical en el piso (-X), PG7 del panel en la pared -X, agujero "
          f"ciego Ø{P.BUOY_SMA_HOLE:g} para un SMA futuro en la pared +X (lejos de los cables), ojal de amarre bajo el extremo +X.", "",
          "## Piezas", "", "| Pieza | Cant. | Bbox en impresion | Orientacion | Volumen cm³ | Relleno | Masa g | BRep | Estanco |",
          "|---|---|---|---|---|---|---|---|---|"]
    for row in rows:
        p = r["piezas"][row["stem"]]
        Ls.append(f"| {row['name']} | {row['qty']} | {' x '.join(f'{v:.1f}' for v in row['mc']['bbox'])} | {row['orient']} | "
                  f"{p['volumen_cm3']:.1f} | {p['relleno'] * 100:.0f} % | {p['masa_g']:.0f} | {'ok' if row['chk']['ok'] else 'FALLA'} | "
                  f"{'si' if row['mc']['watertight'] else 'NO'} |")
    Ls += ["", "Interferencias (piezas y maquetas de bateria, PCB, Waveshare, RTC, antena y panel): " +
           ("ninguna." if not inter else "; ".join(f"{a}/{b} {v:.1f} mm³" for a, b, v in inter)), "",
           "## Masa", "", "| Elemento | g | z mm |", "|---|---|---|"]
    Ls += [f"| {k} | {m:.0f} | {z:.0f} |" for k, m, z in m_pts]
    Ls += [f"| **Total boya** | **{r['masa_g']:.0f}** | KG = {r['KG']:.1f} |", "",
           "## Hidrostatica (agua de mar {:g} kg/m³)".format(P.SEAWATER_DENSITY * 1000), "",
           "| Magnitud | Valor |", "|---|---|",
           f"| Calado | {r['calado']:.1f} mm |",
           f"| Francobordo (hasta la tapa) | **{r['francobordo']:.1f} mm** (minimo {P.BUOY_FREEBOARD_MIN:g}: {'CUMPLE' if r['francobordo'] >= P.BUOY_FREEBOARD_MIN else 'NO CUMPLE'}) |",
           f"| Volumen sumergido / sellado | {r['V']:.0f} / {r['V_sellado']:.0f} cm³ |",
           f"| Reserva de flotacion | {r['reserva'] * 100:.0f} % |",
           f"| KB / KG | {r['KB']:.1f} / {r['KG']:.1f} mm |",
           f"| BM balanceo / cabeceo | {r['BM'][0]:.0f} / {r['BM'][1]:.0f} mm |",
           f"| **GM balanceo / cabeceo** | **{r['GM'][0]:.0f} / {r['GM'][1]:.0f} mm** |", "",
           f"**Peso total nodo + boya: {r['total_g']:.0f} g** (nodo {r['nodo_g']:.0f} g, boya {r['masa_g']:.0f} g) contra 3 kg: "
           + (f"**se pasa por {r['exceso_g']:.0f} g**." if r["exceso_g"] > 0 else "cumple."), "",
           "Estimacion de geometria, no certificacion: masas de componentes estimadas (`boya.masas`, el panel es la mayor "
           "incertidumbre), sin oleaje, viento ni tension del umbilical.", "",
           "## Chequeos que fallaron", ""] + ([f"- {f}" for f in fails] if fails else ["- ninguno"])
    (HERE / "reporte_boya_simple.md").write_text("\n".join(Ls) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
