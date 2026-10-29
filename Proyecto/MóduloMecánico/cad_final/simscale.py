"""Fase F: STEP simplificados para SimScale en ../salida/simscale/ (4 casos). Los pasos de simplificacion se hacen con
parches temporales de funciones de los modulos de pieza (sin editarlos); el detalle de cada caso esta en ../SIMSCALE.md.
Cada solido se valida con checks.brep_check; los casos de varios cuerpos se guardan como solidos separados en un STEP.
Run from cad_final/:  python simscale.py
"""
import json
from pathlib import Path

import cadquery as cq

import camara
import caja_central as CC
import capsula
import gancho
import layout
import riel
from checks import brep_check, sanitize
from params import (HINGE_DISC_D, HINGE_EAR_T, HINGE_GAP, HINGE_TEETH_RIN, HINGE_TOOTH_H, LATCH_BUMP, RAIL_CENTRAL_L,
                    RAIL_EXT_L)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "salida" / "simscale"

# valores propios de este script (no estan en params.py)
CENTRAL_X0 = 10.0       # el central se corta en |x| = 10: queda su tramo exterior de 60 mm hasta la punta (x = 70)
PIN_D = 4.0             # pasador M4 de la bisagra, cilindro liso (rosca no modelada)
HOOK_PAD_W = 3.0        # franja de la cara superior de la brida, en el extremo del lado de la perilla, donde apoya el fondo del riel
SKIP_DUMMY = (1e4, 1e4, 1e4)


def _far_box():
    return cq.Workplane("XY").box(0.1, 0.1, 0.1).translate(SKIP_DUMMY)


# ------------------------------------------------------------------ parches (se aplican en build_all y se deshacen al salir)
def _flat_serration(r_in, r_out, n, h, offset_deg=0.0):
    """Reemplaza los dientes de 1.2 mm por un anillo plano de h/2: tronco y orejas se tocan en el plano medio del dd hueco."""
    ring = cq.Solid.makeCylinder(r_out, h / 2, cq.Vector(0, 0, 0), cq.Vector(0, 1, 0)).cut(
        cq.Solid.makeCylinder(r_in, h / 2, cq.Vector(0, 0, 0), cq.Vector(0, 1, 0)))
    return cq.Workplane().add(ring)


_orig_xz_prism = gancho._xz_prism


def _xz_prism_no_ridge(pts, y0, y1):
    if len(pts) == 4 and abs((pts[1][1] - pts[0][1]) - (LATCH_BUMP + 0.01)) < 1e-6:   # cresta de traba del pestillo
        return _far_box_inside()
    return _orig_xz_prism(pts, y0, y1)


def _far_box_inside():
    d = gancho.jaw_dims()   # caja dentro del macizo de la mandibula (pared inferior), no cambia el solido
    xm = (d["x0"] + d["x_end"]) / 2
    return gancho._box(xm - 1, xm + 1, -1, 1, d["z_bot"] + 1, d["z_bot"] + 2)


class Patched:
    def __enter__(self):
        self.s = [(capsula, "serration", capsula.serration), (capsula, "_bezel_pts", capsula._bezel_pts),
                  (capsula, "_ring_yz", capsula._ring_yz), (CC, "tray_boss_pts", CC.tray_boss_pts),
                  (CC, "GROOVE_DEPTH", CC.GROOVE_DEPTH), (gancho, "_xz_prism", gancho._xz_prism)]
        capsula.serration = _flat_serration
        capsula._bezel_pts = lambda: []                                   # sin pilotos M2 en la capsula ni el bisel
        capsula._ring_yz = lambda *a, **k: _far_box()                     # sin ranura de junta en la tapa de la capsula
        CC.tray_boss_pts = lambda lay: []                                 # sin postes de bandeja ni sus insertos M3
        CC.GROOVE_DEPTH = -1.0                                            # extrusion hacia afuera de la tapa: no corta
        gancho._xz_prism = _xz_prism_no_ridge
        return self

    def __exit__(self, *a):
        for mod, name, val in self.s:
            setattr(mod, name, val)


# ------------------------------------------------------------------ casos
def S(wp_or_shape):
    wp = wp_or_shape if isinstance(wp_or_shape, cq.Workplane) else cq.Workplane().add(wp_or_shape)
    return sanitize(wp)


def case_union(lay, c):
    xj = c.x_joint
    cen = riel.central(lay, c)
    zr = c.z_rail
    keep = cq.Workplane("XY").box(RAIL_CENTRAL_L / 2 - CENTRAL_X0, 400, 400, centered=False).translate(
        (CENTRAL_X0, -200, zr - 100))
    cen = cen.intersect(keep)
    ext = riel.ext(c).translate((xj, 0, 0))
    return {"riel_central_x10a70": S(cen), "riel_ext": S(ext)}


def case_gancho():
    """Gancho con la cara superior de la brida dividida en x = fx0 + HOOK_PAD_W (franja de apoyo contra el riel).
    La division se hace al final con fuse(glue) sin clean() para que la cara no se vuelva a unir."""
    g = S(gancho.gancho())
    x_cut = gancho.hook_layout()["fx0"] + HOOK_PAD_W
    big = 400.0
    a = g.intersect(cq.Workplane().box(big, big, big, centered=False).translate((x_cut - big, -big / 2, -big / 2)).val())
    b = g.intersect(cq.Workplane().box(big, big, big, centered=False).translate((x_cut, -big / 2, -big / 2)).val())
    return {"gancho": a.fuse(b, glue=True)}


def case_caja(lay):
    return {"caja_cuerpo": S(CC.box_body(lay)), "caja_tapa": S(CC.box_lid(lay))}


def case_carro():
    out = {"carro": S(capsula.carriage())}
    for k, fn in (("cap_cuerpo_M4", capsula.capsule_body), ("cap_tapa_M5", capsula.capsule_lid),
                  ("cap_bisel_M6", capsula.bezel), ("cap_ventana_M7", capsula.window_disc)):
        out[k] = S(capsula.place_capsule(fn().val(), 0))
    ax, az = capsula.carriage_axis()
    L = HINGE_GAP + 2 * HINGE_EAR_T
    pin = cq.Workplane("XZ").center(ax, az).circle(PIN_D / 2).extrude(L / 2, both=True)
    out["pasador_M4_acero"] = S(pin)
    return out


def export(name, parts, log):
    OUT.mkdir(parents=True, exist_ok=True)
    comp = cq.Compound.makeCompound(list(parts.values()))
    path = OUT / f"{name}.step"
    cq.exporters.export(cq.Workplane().add(comp), str(path))
    back = cq.importers.importStep(str(path)).val()
    v0, v1 = comp.Volume(), back.Volume()
    n_back = len(back.Solids())
    row = {"archivo": path.name, "volumen_ok": abs(v0 - v1) < 1e-3 * v0, "solidos_leidos": n_back,
           "solidos_esperados": len(parts), "piezas": {}}
    for k, sh in parts.items():
        bc = brep_check(sh)
        bb = sh.BoundingBox()
        row["piezas"][k] = {"ok": bc["ok"], "brep": bc["brep"], "bop": bc["bop"], "solidos": bc["solids"],
                            "min_edge": round(bc["min_edge"], 3), "min_face": round(bc["min_face"], 3),
                            "vol_cm3": round(sh.Volume() / 1000, 3), "caras": len(sh.Faces()),
                            "bbox": [round(v, 2) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)]}
    log[name] = row
    flag = "OK" if all(p["ok"] for p in row["piezas"].values()) and row["volumen_ok"] and n_back == len(parts) else "REVISAR"
    print(name, flag, f"vol {v0 / 1000:.2f} cm3", "solidos", n_back)
    for k, p in row["piezas"].items():
        print("   ", k, p)


def main():
    lay = layout.build(floors=1)
    c = camara.dims(lay)
    log = {"z_rail": c.z_rail, "x_joint": c.x_joint}
    ax, az = capsula.carriage_axis()
    log["eje_bisagra_carro"] = [ax, az]
    with Patched():
        export("simscale_1_union_riel", case_union(lay, c), log)
        export("simscale_2_gancho", case_gancho(), log)
        export("simscale_3_caja_tapa", case_caja(lay), log)
        export("simscale_4_carro_capsula", case_carro(), log)
    d = gancho.hook_layout()
    log["gancho"] = {"xk": d["xk"], "fx0": d["fx0"], "fx1": d["fx1"], "z_top_jaw": d["d"]["z_top"] - gancho.HOOK_DROP}
    log["caja_outer"] = list(lay.box_outer())
    log["caja_screws"] = len(CC.screw_pts(lay))
    (OUT / "resumen.json").write_text(json.dumps(log, indent=1, default=float), encoding="utf-8")
    print("resumen.json escrito")


if __name__ == "__main__":
    main()
