"""Real printed mass and time with OrcaSlicer (CLI) for every printed piece of the simple version.

    python slicer.py            (from cad_final/; or: python build.py --slicer, which then rebuilds the bitacora)

Profiles: three flat JSON in cad_final/orca/ (printer Bambu Lab P1P 0.4 nozzle with the Textured PEI Plate, process
0.20mm Standard @BBL P1P, filament Bambu PETG Basic); each file is recognised by its "type" key and its "_origen" key
says where it came from. Every piece: 0.2 mm layers, 3 walls, gyroid with the infill of the piece (resultados.json;
a mixed "riel 40 %, gancho 100 %" is sliced at the highest), supports only where the bitacora says so (overhang over
simple.SUPPORT_MM2 in the print orientation). Each printed piece of resultados.json (not the bought acrylic M7) is turned
to its print orientation and sliced alone; the G-code goes to salida/<version>/gcode/ (ignored by git; version = simple or prototipos/<P..>) and
"; filament used [g]" and the estimated time are read from it into <version>/slicer.json. ORCA_EXE overrides the
slicer path.

The nightly portable has no BBL machine/process presets on disk (they are packed in resources/profiles/BBL.opc), so a
preset that keeps an "inherits" does not resolve ("can not resolve preset ... system"). The JSON in orca/ are flattened
from the OrcaSlicer repo (resources/profiles/BBL/, inherits and include merged, commit 304924a, 30/10). The stable 2.4.2
does not slice from the CLI. If cad_final/orca/ is empty, the JSON of Downloads/orca_perfiles/ are copied there first.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
SAL = MOD / "salida"
import params as P  # noqa: E402  (VERSION / LG_VERSION decide the output folder)
VER = SAL / P.SALIDA_REL
GCODE = VER / "gcode"
PROFILES = HERE / "orca"
ORCA = Path(os.environ.get("ORCA_EXE", Path.home() / "Downloads" / "OrcaSlicer_Windows_x64_nightly_portable"
                           / "OrcaSlicer" / "orca-slicer.exe"))
OVERRIDES = {"layer_height": "0.2", "wall_loops": "3", "sparse_infill_density": "20%", "sparse_infill_pattern": "gyroid"}
STL_DIRS = (VER / "stl", SAL / "linterna_prueba" if P.VERSION == "simple" else VER / "lr1")


def pieces(res):
    """(folder, stem) of every printed piece in resultados.json (relleno None = bought, e.g. the acrylic window M7)."""
    out = []
    for stem, info in res["piezas"].items():
        if info.get("relleno") is None:
            continue
        folder = next((d for d in STL_DIRS if (d / f"{stem}.stl").exists()), None)
        if folder is None:
            raise SystemExit(f"no encuentro {stem}.stl en {', '.join(str(d) for d in STL_DIRS)}")
        out.append((folder, stem))
    return out


def profiles(folder=PROFILES):
    """{'machine': path, 'process': path, 'filament': path} from the exported JSON (by their "type")."""
    found = {}
    for f in sorted(folder.glob("*.json")):
        try:
            t = json.loads(f.read_text(encoding="utf-8")).get("type")
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if t in ("machine", "process", "filament") and t not in found:
            found[t] = f
    missing = {"machine", "process", "filament"} - set(found)
    if missing:
        raise SystemExit(f"faltan perfiles en {folder}: {', '.join(sorted(missing))} (ver ONSHAPE/CAMBIOS: exportar desde la GUI)")
    return found


def oriented_stl(src, orient, dst):
    """STL turned to its print orientation and laid on the bed (min z = 0, centred on the bed)."""
    import math
    import trimesh
    import params as P
    from capsula import ORIENTS
    m = trimesh.load(src)
    o = ORIENTS.get(orient)
    if o:
        ax, ang = o
        vec = {"X": [1, 0, 0], "Y": [0, 1, 0], "Z": [0, 0, 1]}[ax]
        m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(ang), vec))
    lo, hi = m.bounds
    m.apply_translation([P.PRINT_BED[0] / 2 - (lo[0] + hi[0]) / 2, P.PRINT_BED[1] / 2 - (lo[1] + hi[1]) / 2, -lo[2]])
    m.export(dst)


def infill_pct(relleno):
    """Infill of the piece from resultados.json: 1.0 / 0.4, or a mixed text ("riel 40 %, gancho 100 %") -> the highest,
    so the mass and time stay on the safe side."""
    if isinstance(relleno, (int, float)):
        return round(relleno * 100)
    vals = [int(v) for v in re.findall(r"(\d+)\s*%", str(relleno))]
    return max(vals) if vals else None


def process_for(base, supports, dst, infill=None):
    data = json.loads(Path(base).read_text(encoding="utf-8"))
    data.update(OVERRIDES)
    if infill is not None:
        data["sparse_infill_density"] = f"{infill}%"
    data["enable_support"] = "1" if supports else "0"
    data["name"] = f"{data.get('name', 'proceso')} LanternGuard {'con' if supports else 'sin'} soportes"
    Path(dst).write_text(json.dumps(data, indent=1), encoding="utf-8")


def read_gcode(path):
    """(grams, hours) from the G-code comments; None if missing. Time from "; estimated printing time (normal mode) = ..."
    or from the nightly header "; model printing time: ...; total estimated time: ..."."""
    txt = Path(path).read_text(encoding="utf-8", errors="replace")
    g = re.search(r";\s*filament used \[g\]\s*=\s*([\d.]+)", txt)
    t = re.search(r";[^\n]*?(?:total estimated time|estimated printing time(?: \(normal mode\))?)\s*[:=]\s*([^;\n]+)", txt)
    if not (g and t):
        return None
    secs = 0
    for val, unit in re.findall(r"(\d+)\s*([dhms])", t.group(1)):
        secs += int(val) * {"d": 86400, "h": 3600, "m": 60, "s": 1}[unit]
    return float(g.group(1)), secs / 3600


def slice_one(prof, stl, process, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.gcode"):
        old.unlink()
    cmd = [str(ORCA), "--load-settings", f"{prof['machine']};{process}", "--load-filaments", str(prof["filament"]),
           "--slice", "0", "--outputdir", str(out_dir), str(stl)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    gc = sorted(out_dir.glob("*.gcode"))
    return r.returncode, gc[0] if gc else None, (r.stdout + r.stderr)[-500:]


EXPORTED = Path.home() / "Downloads" / "orca_perfiles"


def main(profile_dir=PROFILES):
    if not ORCA.exists():
        raise SystemExit(f"no encuentro OrcaSlicer en {ORCA}")
    if profile_dir == PROFILES and not list(PROFILES.glob("*.json")) and EXPORTED.exists():
        import shutil
        PROFILES.mkdir(exist_ok=True)
        for f in EXPORTED.rglob("*.json"):
            shutil.copy2(f, PROFILES / f.name)
        print(f"perfiles copiados de {EXPORTED} a {PROFILES}")
    prof = profiles(profile_dir)
    res = json.loads((VER / "resultados.json").read_text(encoding="utf-8"))
    work = GCODE / "_trabajo"
    work.mkdir(parents=True, exist_ok=True)
    out, fails = {}, []
    for folder, stem in pieces(res):
        info = res["piezas"][stem]
        stl = work / f"{stem}.stl"
        oriented_stl(folder / f"{stem}.stl", info["orient"], stl)
        proc = work / f"proceso_{stem}.json"
        infill = infill_pct(info.get("relleno"))
        process_for(prof["process"], info["soportes"], proc, infill)
        rc, gc, log = slice_one(prof, stl, proc, work / stem)
        got = read_gcode(gc) if gc else None
        if not got:
            fails.append(f"{stem}: rc={rc}, sin G-code o sin datos ({log.strip()[-200:]})")
            print("FALLA", stem, rc, flush=True)
            continue
        dst = GCODE / f"{stem}.gcode"
        gc.replace(dst)
        out[stem] = dict(g=got[0], h=got[1], soportes=info["soportes"], relleno_pct=infill,
                         gcode=dst.relative_to(MOD).as_posix())
        print(f"OK    {stem:24s} {got[0]:7.1f} g  {got[1]:5.2f} h  relleno {infill} %  "
              f"soportes {'si' if info['soportes'] else 'no'}", flush=True)
    if out:
        (VER / "slicer.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("FALLAS:", fails if fails else "ninguna")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else PROFILES))
