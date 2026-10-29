"""Variants of the simple node, rendered with one shared ISO framing for side-by-side comparison.

    python variantes.py [salida_combinada.png]     (from cad_final/)
V1: capsules at 30 deg, C hook with strap.  V2: capsules at 45 deg, C hook with strap.
V3: capsules at 30 deg, C hook without strap slot and with a flared mouth (lifts off the ring without the strap).
Outputs: salida/variantes/V1..V3.png and .step (node + test lantern, like ensamble_simple_D200.step) and the combined
image (default salida/variantes/variantes.png).
Only renders: params.py keeps the chosen version; the variant values are set here for each render.
"""
import sys
from pathlib import Path

import cadquery as cq
import numpy as np

import params as P
import simple as SM   # patches the rod out of camara/riel on import, as the simple build does
import camara
import capsula as CP
import fase_a as FA
import layout
from render import render

OUT = SM.MOD / "salida" / "variantes"
VARIANTS = [("V1", "Capsula a 30°, gancho con correa", 30.0, True),
            ("V2", "Capsula a 45°, gancho con correa", 45.0, True),
            ("V3", "Capsula a 30°, gancho abierto sin correa", 30.0, False)]
COLOURS = {"caja": ("#5b8fb9", 0.55), "riel": ("#3a9d7a", 1.0), "lastre": ("#777777", 1.0), "correa": ("#c0504d", 1.0)}


def build(lay, c, an, ch, tilt, strap):
    P.SIMPLE_CAP_TILT = tilt
    half = SM.solid(SM.rail_half(lay, c, P.PLATE_POCKET_LAYERS))
    hk = SM.solid(SM.hook(strap))
    cp = {"M4": CP.capsule_body(), "M6": CP.bezel(), "M7": CP.window_disc(), "lid": CP.lid_plate()}
    ax, az = SM.capsule_pose(c, cp)
    m5s = SM.solid(SM.lid_with_foot(c, cp["lid"], ax, az))
    plates = [SM.solid(p) for p in camara.plates_solid(lay, P.SIMPLE_PLATES)]
    z_rod = c.z_rail - P.HOOK_DROP
    node = SM.assemble(an, ch, half, hk, m5s, SM.solid(ch["tapa_bolsillo_n"]), cp, ax, az, z_rod, plates, strap=strap)
    ring = cq.Solid.makeTorus(SM.R_RING, P.RING_SECTION / 2, cq.Vector(0, 0, z_rod), SM.ZAX)
    items = []
    for sh, g in node.values():
        col, op = COLOURS.get(g, ("#c9a227", 1.0) if g.startswith("gancho") else ("#3a7ca5", 1.0))
        items.append((sh, col, op, True, None))
    items.append((ring, "#8a8a8a", 0.8, False, None))
    # full assembly for the STEP, same content as ensamble_simple_D200.step (lantern, LR1, umbilical)
    z_sep = z_rod + P.SEP_H
    lant, _, buoy_end = SM.lantern(z_rod, z_sep, z_sep + P.APEX_H)
    gland = (lay.lid_gland[0], lay.lid_gland[1], lay.box_outer()[2] + P.BOX_LID_T) if lay.lid_gland else lay.wall_gland
    asm = [sh for sh, _ in node.values()] + list(lant.values()) + [SM.solid(SM.separator(z_sep))]
    asm += SM.umbilical(gland, buoy_end)
    return items, asm


def piece_corners(shape):
    b = shape.BoundingBox()
    return np.array([[x, y, z] for x in (b.xmin, b.xmax) for y in (b.ymin, b.ymax) for z in (b.zmin, b.zmax)])


def combine(paths, labels, out):
    from PIL import Image, ImageDraw, ImageFont
    ims = [Image.open(p).convert("RGB") for p in paths]
    w, h = 1280, 720
    ims = [im.resize((w, h), Image.LANCZOS) for im in ims]
    band = 130
    canvas = Image.new("RGB", (w * len(ims), h + band), "white")
    draw = ImageDraw.Draw(canvas)
    try:
        big, small = ImageFont.truetype("arialbd.ttf", 64), ImageFont.truetype("arial.ttf", 34)
    except OSError:
        big = small = ImageFont.load_default()
    for k, (im, (tag, txt)) in enumerate(zip(ims, labels)):
        canvas.paste(im, (k * w, band))
        draw.text((k * w + 30, 10), tag, fill="black", font=big)
        draw.text((k * w + 30, 82), txt, fill="black", font=small)
        if k:
            draw.line([(k * w, 0), (k * w, h + band)], fill="#bbbbbb", width=3)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    print("written", out)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lay = layout.build(floors=1)
    c = camara.dims(lay)
    an = FA.analyse_box(lay)
    ch = camara.chamber_solid(lay, P.PLATE_POCKET_LAYERS)
    built = {}
    for tag, _, tilt, strap in VARIANTS:
        built[tag], asm = build(lay, c, an, ch, tilt, strap)
        step = OUT / f"{tag}.step"
        SM.E.comp(asm).exportStep(str(step))
        SM.fix_step_stamp(step)
        print("written", step)
    # one framing for all: the corners of every piece of the three variants (the corners of one global box project
    # far outside the node in ISO and leave it small)
    frame = np.vstack([piece_corners(it[0]) for items in built.values() for it in items])
    paths = []
    for tag, txt, _, _ in VARIANTS:
        p = OUT / f"{tag}.png"
        render(built[tag], p, "iso", None, frame=frame)
        paths.append(p)
    combine(paths, [(t, x) for t, x, _, _ in VARIANTS], Path(sys.argv[1]) if len(sys.argv) > 1 else OUT / "variantes.png")


if __name__ == "__main__":
    main()
