"""Fase D: how much rail each ring needs beyond the ring radius, along X only (no CAD, seconds). The hook sits with its
flange and knob inboard of the rod (gancho.py frame, as ensambles.py places it); the carriage sleeve must start
outboard of the hook flange, and the capsule at any tilt must stay outboard of the jaw. Compared with the rail tip of
the current assembly and of the prepared switches (RAIL_EXT_PITCH_MODE, RAIL_EXT_RULE), none applied by default.

    python largo_riel.py        (from cad_final/)   -> printed table; imported by verificacion.py and FASE_D.md
"""
import capsula as CP
import gancho as G
from params import (CARRIAGE_L, CARRIAGE_TRAVEL, FIT_CLEAR, LANTERN_ROD_D, RAIL_CENTRAL_L, RAIL_DOVETAIL, RAIL_EXT_L,
                    RAIL_EXT_PER_RING, RAIL_LAYOUT_GAP, RING_DIAMETERS)


def tip(n, mode):
    step = RAIL_EXT_L if mode == "paso_100" else RAIL_EXT_L - RAIL_DOVETAIL
    return RAIL_CENTRAL_L / 2 + n * step


def needs():
    """Distances beyond R (rod centre) that the node occupies on the +X side."""
    L = G.hook_layout()
    d = L["d"]
    fl_out = L["fx1"]                                      # hook flange outboard end, from the rod centre
    jaw_out = d["x_end"]                                   # jaw (strap slot side) outboard end
    ax = CP.carriage_axis()[0]
    _, _, _, fl_h, _, _, _ = CP.cap_dims()
    sleeve_min = fl_out + RAIL_LAYOUT_GAP + CARRIAGE_L    # sleeve front, from the rod, if the sleeve clears the flange
    cap_back = ax - fl_h / 2                               # capsule rearmost x at tilt 90, from the sleeve front
    cap_min = jaw_out + FIT_CLEAR + LANTERN_ROD_D / 2 - cap_back   # sleeve front so the capsule clears the jaw
    need0 = max(sleeve_min, cap_min)
    return dict(fl_out=fl_out, jaw_out=jaw_out, sleeve_min=sleeve_min, cap_min=cap_min, need0=need0,
                need_full=need0 + 2 * CARRIAGE_TRAVEL)


def table():
    nd = needs()
    rows = []
    for D in RING_DIAMETERS:
        R = D / 2
        n_team = RAIL_EXT_PER_RING[D]
        row = dict(D=D, need0=R + nd["need0"], need_full=R + nd["need_full"])
        for mode in ("solape", "paso_100"):
            t = tip(n_team, mode)
            n_auto = next(k for k in range(10) if tip(k, mode) >= R + nd["need0"])
            row[mode] = dict(tip=t, short=R + nd["need0"] - t, s_max=t - (R + nd["need0"]), n_auto=n_auto,
                             tip_auto=tip(n_auto, mode), s_auto=tip(n_auto, mode) - (R + nd["need0"]))
        rows.append(row)
    return nd, rows


if __name__ == "__main__":
    nd, rows = table()
    print({k: round(v, 1) for k, v in nd.items()})
    for r in rows:
        print(r["D"], round(r["need0"], 1), {m: {k: round(v, 1) for k, v in r[m].items()} for m in ("solape", "paso_100")})
