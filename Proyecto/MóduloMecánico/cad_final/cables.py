"""Cat5e run per camera and per ring (prompt v2 point 7, C6), along the real path of the revision 28/10:
box slack + gland + (90 deg bend R in the chamber + straight to the end of the central piece + extensions up to
the exit slot) + loop to the capsule + inside the capsule + spare. Runs > SPI_TEST_LIMIT are flagged.
The loop is the larger of CABLE_ALLOW["bucle"] and the straight distance from the exit to the capsule PG7, worst case
over the carriage travel and the tilt 0..90 (capsula.py geometry): a lower bound, the cable also bends.

    python cables.py            (from cad_final/)   -> cad_final/reporte_cables.md
"""
import math
from pathlib import Path

import capsula as CP
import camara as CH
import layout as LY
from params import (CABLE_ALLOW, CAMERA_CABLE, CAP_GLAND_X, CARRIAGE_STEPS, CARRIAGE_TRAVEL, RAIL_CENTRAL_L,
                    RAIL_EXIT_SLOT, RAIL_EXT_L, RAIL_EXT_PER_RING, RAIL_SECTION, RING_DIAMETERS, SPI_TEST_LIMIT)
from riel import EXIT_SLOT_ZC

HERE = Path(__file__).resolve().parent


def loop_distance(side_slot):
    """Worst straight distance exit -> capsule PG7 over carriage positions and tilts (carriage frame of capsula.py)."""
    _, out_h, _, _, _, x0, _ = CP.cap_dims()
    gx, gz = x0 + CAP_GLAND_X, -out_h / 2
    ax, az = CP.carriage_axis()
    _, slot_l, slot_tip = RAIL_EXIT_SLOT
    worst = 0.0
    for k in range(CARRIAGE_STEPS):
        tip = 2 * CARRIAGE_TRAVEL * k / (CARRIAGE_STEPS - 1)
        ex = (tip - slot_tip - slot_l / 2, RAIL_SECTION / 2, EXIT_SLOT_ZC) if side_slot else (tip, 0.0, EXIT_SLOT_ZC)
        for t in range(0, 100, 10):
            a = math.radians(t)
            g = (ax + gx * math.cos(a) + gz * math.sin(a), 0.0, az - gx * math.sin(a) + gz * math.cos(a))
            worst = max(worst, math.dist(ex, g))
    return worst


def runs(lay):
    c = CH.dims(lay)
    gx = max(abs(x) for x, _ in lay.floor_glands)
    bend = math.pi / 2 * c.bend_r
    straight = RAIL_CENTRAL_L / 2 - (gx + c.bend_r)
    _, slot_l, slot_tip = RAIL_EXIT_SLOT
    a = CABLE_ALLOW
    out = []
    for D in RING_DIAMETERS:
        n = RAIL_EXT_PER_RING[D]
        # with extensions the cable leaves through the side slot of the last one; without, through the open end
        rail = bend + straight + (n * RAIL_EXT_L - (slot_tip + slot_l / 2) if n else 0.0)
        loop = max(a["bucle"], loop_distance(n > 0))
        total = a["caja"] + a["prensaestopas"] + rail + loop + a["capsula"] + a["holgura"]
        out.append(dict(D=D, n=n, rail=rail, loop=loop, total=total, spi=total > SPI_TEST_LIMIT,
                        stock=total <= CAMERA_CABLE))
    return out, dict(bend=bend, straight=straight, gx=gx, R=c.bend_r)


def main():
    lay = LY.build(floors=1)
    rows, g = runs(lay)
    a = CABLE_ALLOW
    r = ["# Recorrido del Cat5e por cámara (generado por `cables.py`)", "",
         f"Por cámara: {a['caja']:g} de holgura en la caja + {a['prensaestopas']:g} de prensaestopas + tramo por el riel "
         f"+ bucle hasta el PG7 de la cápsula + {a['capsula']:g} dentro de la cápsula + {a['holgura']:g} de holgura. "
         f"El bucle es el mayor entre {a['bucle']:g} y la distancia en línea recta de la salida al PG7 de la cápsula, en el peor caso "
         f"del recorrido del carro (±{CARRIAGE_TRAVEL:g}) y de la inclinación (0 a 90°): es un mínimo, el cable además se curva. "
         f"Tramo por el riel: curva de 90° con R{g['R']:g} en la cámara ({g['bend']:.1f}) + recto hasta la punta del tramo "
         f"central ({g['straight']:.1f}) + extensiones hasta la ranura de salida (a {RAIL_EXIT_SLOT[2] + RAIL_EXIT_SLOT[1] / 2:g} "
         "de la punta). Sin extensiones sale por la punta abierta del tramo central.", "",
         "| Aro | Extensiones por lado | Tramo por el riel mm | Bucle mm | Total por cámara mm | Cable de fábrica (300) alcanza | Nota |",
         "|---|---|---|---|---|---|---|"]
    for row in rows:
        r.append(f"| Ø{row['D']:g} | {row['n']} | {row['rail']:.0f} | {row['loop']:.0f} | {row['total']:.0f} | "
                 f"{'sí' if row['stock'] else 'no'} | "
                 f"{'requiere prueba en banco SPI a 8 y 4 MHz' if row['spi'] else ''} |")
    r += ["", "Medidas estimadas: diámetro del Cat5e, radio de curvatura (se usa el mayor entre 4 × D y 25) y largo del "
          "domo del PG7, que fija dónde empieza la curva.", ""]
    (HERE / "reporte_cables.md").write_text("\n".join(r), encoding="utf-8")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
