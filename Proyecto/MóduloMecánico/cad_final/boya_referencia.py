"""Reference model of the platform buoy of the team's example (not printable, only to compare with ours).

    python boya_referencia.py        (from cad_final/)  -> salida/simple/boya/ENSAMBLE_boya_referencia.step + png
Central sealed box boya.caja_exterior on a square deck, panel 170 x 170 on 4 posts 25 mm above the lid, 4 cylindrical
floats under the deck corners. Named parts (cq.Assembly) so Onshape keeps them apart.
"""
from pathlib import Path

import cadquery as cq

import params as P

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "salida" / "simple" / "boya"

DECK = (420.0, 400.0, 8.0)        # deck plate of the example (estimated from the sketch: floats just outside the box)
FLOAT_D, FLOAT_H = 120.0, 80.0    # cylindrical corner floats of the example
POST_H = 25.0


def build():
    L, Wd, H = P.BUOY_BOX
    dx, dy, dt = DECK
    a = cq.Assembly(name="boya_referencia")
    zd = FLOAT_H * 0.6                              # deck over the float bottom
    a.add(cq.Workplane("XY").box(dx, dy, dt).translate((0, 0, zd + dt / 2)), name="R_cubierta", color=cq.Color(0.8, 0.8, 0.8))
    for sx in (1, -1):
        for sy in (1, -1):
            x, y = sx * (dx / 2 - FLOAT_D / 2), sy * (dy / 2 - FLOAT_D / 2)
            a.add(cq.Workplane("XY").center(x, y).circle(FLOAT_D / 2).extrude(FLOAT_H), name=f"R_flotador_{'+' if sx > 0 else '-'}x{'+' if sy > 0 else '-'}y",
                  color=cq.Color(1.0, 0.55, 0.1))
    zb = zd + dt
    a.add(cq.Workplane("XY").rect(L, Wd).extrude(H).edges("|Z").fillet(10).translate((0, 0, zb)), name="R_caja",
          color=cq.Color(0.3, 0.5, 0.75))
    zp = zb + H + POST_H
    pl, pw, pt = P.BUOY_PANEL
    a.add(cq.Workplane("XY").box(pl, pw, pt).translate((0, 0, zp + pt / 2)), name="R_panel", color=cq.Color(0.1, 0.1, 0.3))
    for sx in (1, -1):
        for sy in (1, -1):
            a.add(cq.Workplane("XY").center(sx * (pl / 2 - 15), sy * (pw / 2 - 15)).circle(5).extrude(POST_H)
                  .translate((0, 0, zb + H)), name=f"R_poste_{'+' if sx > 0 else '-'}x{'+' if sy > 0 else '-'}y")
    return a


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    a = build()
    path = OUT / "ENSAMBLE_boya_referencia.step"
    a.export(str(path))
    from checks import fix_step_stamp
    fix_step_stamp(path)
    from render import render
    items = [(c.obj.val() if hasattr(c.obj, "val") else c.obj, "#8fa8c8", 0.9, True, None)
             for c in a.traverse() for c in [c[1]] if c.obj is not None]
    render([(it[0].moved(loc), *it[1:]) for it, loc in zip(items, [c[1].loc for c in a.traverse() if c[1].obj is not None])],
           OUT / "boya_referencia_iso.png", "iso", "Boya de referencia del equipo (no imprimible)")
    print("written", path)


if __name__ == "__main__":
    main()
