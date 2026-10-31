"""Print plates: groups STL already turned to their print orientation into plates of the Bambu P1P, slices every plate
with the OrcaSlicer CLI into a 3MF (G-code inside, opens in Orca or Bambu Studio and prints as is) and saves the slicer
previews for the report.

    python placas.py <plan.json>

plan.json: {"salida": "salida/imprimir_hoy/3mf", "capturas": "salida/capturas_slicer",
            "placas": [{"nombre": "01_probetas", "relleno": 40, "soportes": false, "paredes": 3,
                        "piezas": [["salida/imprimir_hoy/01_PB7_peine_holguras_x1.stl", 1], ...]}, ...]}
(paths relative to the module folder). One plate = one infill and one support setting (the CLI cannot set them per
object), so pieces are grouped by those. Orca arranges the copies (--arrange 1); a plate that does not fit fails and is
reported. Per plate: <salida>/<nombre>.3mf; in <capturas>/: <nombre>_placa.png and <nombre>_arriba.png (the 512 px
thumbnails Orca stores in Metadata/) and <nombre>_trayectoria.png (the toolpaths of the G-code by feature type, side and
top views, supports in red). Totals in <salida>/placas.json. Profiles and executable as in slicer.py.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import slicer as SL

MOD = SL.MOD
COLORS = {"Outer wall": "#d9822b", "Inner wall": "#f2b36b", "Sparse infill": "#9aa5b1", "Internal solid infill": "#7d8a96",
          "Solid infill": "#7d8a96", "Top surface": "#c0392b", "Bottom surface": "#5d6d7e", "Support": "#2e86de",
          "Support interface": "#1b4f72", "Support transition": "#2e86de", "Bridge": "#8e44ad", "Overhang wall": "#e67e22",
          "Gap infill": "#b2babb", "Skirt": "#cccccc", "Brim": "#cccccc"}


def toolpaths(gcode_txt):
    """{type: [(x0, y0, z, x1, y1), ...]} of the extruding moves (absolute XY, E > 0)."""
    segs, kind, x, y, z = {}, "?", 0.0, 0.0, 0.0
    num = re.compile(r"([XYZE])(-?[\d.]+)")
    for line in gcode_txt.splitlines():
        if line.startswith((";TYPE:", "; FEATURE:")):          # PrusaSlicer style / Bambu-Orca style
            kind = line.split(":", 1)[1].strip()
            continue
        if not line.startswith(("G1 ", "G0 ")):
            continue
        v = dict((k, float(n)) for k, n in num.findall(line.split(";")[0]))
        nx, ny, z = v.get("X", x), v.get("Y", y), v.get("Z", z)
        if v.get("E", 0) > 0 and line.startswith("G1") and (nx != x or ny != y):
            segs.setdefault(kind, []).append((x, y, z, nx, ny))
        x, y = nx, ny
    return segs


def draw_paths(segs, title, dst):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.2), gridspec_kw={"width_ratios": [1.25, 1]})
    for kind, ss in segs.items():
        if kind in ("Custom", "?", "Skirt", "Brim", "Prime tower", "Wipe tower"):
            continue
        c = COLORS.get(kind, "#7f8c8d")
        step = max(1, len(ss) // 60000)            # keep the PNG light on big plates
        ss = ss[::step]
        a1.add_collection(LineCollection([((s[0], s[2]), (s[3], s[2])) for s in ss], colors=c, linewidths=0.25))
        a2.add_collection(LineCollection([((s[0], s[1]), (s[3], s[4])) for s in ss], colors=c, linewidths=0.15,
                                         label=kind))
    for a, t in ((a1, "de costado (X-Z)"), (a2, "desde arriba (X-Y)")):
        a.autoscale()
        a.set_aspect("equal")
        a.set_title(t, fontsize=9)
        a.tick_params(labelsize=7)
    h, lab = a2.get_legend_handles_labels()
    if h:
        leg = a2.legend(h, lab, fontsize=6.5, loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False)
        for lh in leg.legend_handles:
            lh.set_linewidth(3)
    fig.suptitle(title, fontsize=10)
    fig.tight_layout()
    fig.savefig(dst, dpi=140, facecolor="white")
    plt.close(fig)


def slice_plate(prof, plate, out_dir, cap_dir):
    work = Path(tempfile.mkdtemp(prefix="placa_"))
    proc = work / "proceso.json"
    SL.process_for(prof["process"], plate.get("soportes", False), proc, plate.get("relleno"))
    if plate.get("paredes"):
        d = json.loads(proc.read_text(encoding="utf-8"))
        d["wall_loops"] = str(plate["paredes"])
        proc.write_text(json.dumps(d, indent=1), encoding="utf-8")
    stls = []
    for path, n in plate["piezas"]:
        stls += [str(MOD / path)] * int(n)
    name = plate["nombre"]
    cmd = [str(SL.ORCA), "--load-settings", f"{prof['machine']};{proc}", "--load-filaments", str(prof["filament"]),
           "--arrange", "1", "--slice", "0", "--export-3mf", f"{name}.3mf", "--outputdir", str(work)] + stls
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, cwd=work)   # Orca drops 00000.log in cwd
    mf = work / f"{name}.3mf"
    if r.returncode != 0 or not mf.exists():
        return None, (r.stdout + r.stderr)[-300:]
    z = zipfile.ZipFile(mf)
    names = z.namelist()
    gcs = sorted(n for n in names if re.fullmatch(r"Metadata/plate_\d+\.gcode", n))
    if len(gcs) != 1:
        return None, f"{len(gcs)} placas en el 3MF: no entra en una sola placa"
    gtxt = z.read(gcs[0]).decode("utf-8", errors="replace")
    gpath = work / "placa.gcode"
    gpath.write_text(gtxt, encoding="utf-8")
    got = SL.read_gcode(gpath)
    if not got:
        return None, "sin gramos ni tiempo en el G-code"
    out_dir.mkdir(parents=True, exist_ok=True)
    cap_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mf, out_dir / mf.name)
    for src, suf in (("Metadata/plate_1.png", "placa"), ("Metadata/top_1.png", "arriba")):
        if src in names:
            (cap_dir / f"{name}_{suf}.png").write_bytes(z.read(src))
    draw_paths(toolpaths(gtxt), f"{name}: {got[0]:.0f} g, {got[1]:.2f} h, relleno {plate.get('relleno')} %, "
               f"{'con' if plate.get('soportes') else 'sin'} soportes", cap_dir / f"{name}_trayectoria.png")
    z.close()
    shutil.rmtree(work, ignore_errors=True)
    return dict(g=round(got[0], 1), h=round(got[1], 2), relleno=plate.get("relleno"), soportes=plate.get("soportes", False),
                piezas=plate["piezas"], tresmf=(out_dir / mf.name).relative_to(MOD).as_posix()), None


def main(plan_path):
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    prof = SL.profiles()
    out_dir, cap_dir = MOD / plan["salida"], MOD / plan["capturas"]
    res, fails = {}, []
    for plate in plan["placas"]:
        r, err = slice_plate(prof, plate, out_dir, cap_dir)
        if err:
            fails.append(f"{plate['nombre']}: {err}")
            print("FALLA", plate["nombre"], err, flush=True)
            continue
        res[plate["nombre"]] = r
        print(f"OK    {plate['nombre']:34s} {r['g']:7.1f} g  {r['h']:6.2f} h", flush=True)
    if res:
        tot = dict(g=round(sum(v["g"] for v in res.values()), 1), h=round(sum(v["h"] for v in res.values()), 2))
        (out_dir / "placas.json").write_text(json.dumps(dict(placas=res, total=tot), indent=1, ensure_ascii=False),
                                             encoding="utf-8")
        print(f"total {tot['g']} g, {tot['h']} h en {len(res)} placas")
    print("FALLAS:", fails if fails else "ninguna")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
