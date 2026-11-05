"""Support material per piece, measured with OrcaSlicer (block 1.3 of 04/11 night).

    python soportes.py <folder_with_oriented_stl> <out.json>        # e.g. ../salida/_soportes_antes ../salida/soportes_antes.json
    python soportes.py --comparar ../salida/soportes_antes.json ../salida/soportes_despues.json   # markdown table

Each STL (already in print orientation, as in salida/imprimir_hoy/) is sliced alone with supports FORCED ON, tree(auto),
same profile as slicer.py (watertight pieces with impresion.estanca). The G-code is split by Orca's feature comments
("; FEATURE: Support", "Support interface", "Support transition"): support grams = piece grams x (support extrusion /
total extrusion). Percent = support g / model g (model = total - support). A piece that needs none gives 0 %.
"""
import json
import re
import sys
from pathlib import Path

import slicer as SL

SUPPORT_FEATURES = ("support", "support interface", "support transition", "support material")


def split_extrusion(gcode):
    """(total E, support E) from a G-code with feature comments; handles M82 (absolute) and M83 (relative)."""
    rel, e_last, feat = False, 0.0, ""
    tot = sup = 0.0
    for line in Path(gcode).read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith(";"):
            m = re.match(r";\s*(?:FEATURE|TYPE)\s*:\s*(.+)", line)
            if m:
                feat = m.group(1).strip().lower()
            continue
        if line.startswith("M83"):
            rel = True
        elif line.startswith("M82"):
            rel = False
        elif line.startswith("G92"):
            m = re.search(r"E(-?[\d.]+)", line)
            if m:
                e_last = float(m.group(1))
        elif line.startswith(("G1", "G2", "G3")):
            m = re.search(r"E(-?[\d.]+)", line)
            if not m:
                continue
            e = float(m.group(1))
            d = e if rel else e - e_last
            e_last = e if not rel else e_last
            if d > 0:
                tot += d
                if feat in SUPPORT_FEATURES or feat.startswith("support"):
                    sup += d
    return tot, sup


def measure(folder, out_json):
    prof = SL.profiles()
    work = Path(out_json).with_suffix("")
    work.mkdir(parents=True, exist_ok=True)
    res = {}
    for stl in sorted(Path(folder).glob("*.stl")):
        stem = re.sub(r"^\d+_", "", stl.stem)
        stem = re.sub(r"_x\d+$", "", stem)
        proc = work / f"proceso_{stem}.json"
        SL.process_for(prof["process"], True, proc, None, SL.sealed(stem))
        d = json.loads(proc.read_text(encoding="utf-8"))
        d.update(support_type="tree(auto)", support_on_build_plate_only="0")
        proc.write_text(json.dumps(d, indent=1), encoding="utf-8")
        rc, gc, log = SL.slice_one(prof, stl, proc, work / stem)
        got = SL.read_gcode(gc) if gc else None
        if not got:
            res[stem] = dict(error=f"rc={rc} {log.strip()[-160:]}")
            print("FALLA", stem, flush=True)
            continue
        tot, sup = split_extrusion(gc)
        g_sup = got[0] * sup / tot if tot else 0.0
        g_mod = got[0] - g_sup
        res[stem] = dict(g_total=round(got[0], 1), g_soporte=round(g_sup, 1), g_pieza=round(g_mod, 1),
                         pct=round(100 * g_sup / g_mod, 1) if g_mod else 0.0, h=round(got[1], 2))
        print(f"{stem:26s} pieza {g_mod:7.1f} g  soporte {g_sup:6.1f} g  {res[stem]['pct']:5.1f} %", flush=True)
        for f in (work / stem).glob("*.gcode"):
            f.unlink()
    Path(out_json).write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return 0


def compare(before, after):
    a = json.loads(Path(before).read_text(encoding="utf-8"))
    b = json.loads(Path(after).read_text(encoding="utf-8"))
    rows = ["| Pieza | Soporte antes (g) | % antes | Soporte después (g) | % después |", "|---|---|---|---|---|"]
    for k in sorted(set(a) | set(b)):
        x, y = a.get(k, {}), b.get(k, {})
        f = lambda r, key: "—" if key not in r else f"{r[key]:g}"
        rows.append(f"| {k} | {f(x, 'g_soporte')} | {f(x, 'pct')} | {f(y, 'g_soporte')} | {f(y, 'pct')} |")
    print("\n".join(rows))
    return 0


if __name__ == "__main__":
    if sys.argv[1] == "--comparar":
        sys.exit(compare(sys.argv[2], sys.argv[3]))
    sys.exit(measure(sys.argv[1], sys.argv[2]))
