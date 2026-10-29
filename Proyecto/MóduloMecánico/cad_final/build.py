"""Single entry point to regenerate the CAD outputs after changing params.py.

    python cad_final/build.py --rapido      riel, lastre, cables, verificacion, tabla de parametros y MEDIDAS.md (~1.5 min)
    python cad_final/build.py --medidas     solo MEDIDAS.md
    python cad_final/build.py --planos      solo los planos de planos/cad_final/
    python cad_final/build.py               todo menos los ensambles por aro (~6 min)
    python cad_final/build.py --todo        todo, con los 4 ensambles en paralelo (~18 min, mucha CPU)

Each step is the existing script run in its own process (same Python), from cad_final/. Exit code 1 if any step fails.
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable
ENV = {**os.environ, "PYTHONUTF8": "1"}  # children write UTF-8 logs on Windows too (cp1252 has no symbols like >=)

STEPS = {
    "parametros": ["-c", "import params as P; print(len(P.REGISTRO), 'parametros cargados')"],
    "caja": ["fase_c_caja.py"],
    "lastre": ["fase_a.py"],
    "riel": ["riel.py"],
    "gancho": ["gancho.py"],
    "capsula": ["capsula.py"],
    "probetas": ["probetas.py"],
    "boya": ["boya.py"],
    "cables": ["cables.py"],
    "verificacion": ["verificacion.py"],
    "simscale": ["simscale.py"],
    "tabla_parametros": ["reporte_parametros.py"],
    "medidas": ["medidas.py"],
    "planos": ["planos_piezas.py"],
}
PLANS = {
    "rapido": ["parametros", "riel", "lastre", "cables", "verificacion", "tabla_parametros", "medidas"],
    "medidas": ["medidas"],
    "planos": ["planos"],
    "normal": ["parametros", "caja", "riel", "gancho", "capsula", "lastre", "probetas", "boya", "cables", "verificacion",
               "simscale", "tabla_parametros", "medidas", "planos"],
}
CASES = ("100", "200", "300", "500")


def run(name, args, log_dir):
    t0 = time.time()
    log = log_dir / f"{name}.log"
    with open(log, "w", encoding="utf-8") as f:
        rc = subprocess.run([PY, "-u", *args], cwd=HERE, env=ENV, stdout=f, stderr=subprocess.STDOUT).returncode
    tail = log.read_text(encoding="utf-8", errors="replace").strip().splitlines()[-1:] or [""]
    ok = rc == 0
    print(f"{'OK   ' if ok else 'FALLA'} {name:18s} {time.time() - t0:6.0f} s   {tail[0][:90]}", flush=True)
    return ok


def ensambles(log_dir):
    if not run("ensambles_piezas", ["ensambles.py", "build"], log_dir):
        return False
    t0 = time.time()
    procs = {c: subprocess.Popen([PY, "-u", "ensambles.py", "case", c], cwd=HERE, env=ENV,
                                 stdout=open(log_dir / f"ensamble_{c}.log", "w", encoding="utf-8"), stderr=subprocess.STDOUT)
             for c in CASES}
    ok = all(p.wait() == 0 for p in procs.values())
    print(f"{'OK   ' if ok else 'FALLA'} {'ensambles 4 aros':18s} {time.time() - t0:6.0f} s", flush=True)
    return run("ensambles_reporte", ["ensambles.py", "report"], log_dir) and ok


def main():
    ap = argparse.ArgumentParser(description="Regenera las salidas del CAD desde params.py")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--rapido", action="store_true", help="riel, lastre, cables, verificacion y MEDIDAS.md")
    g.add_argument("--medidas", action="store_true", help="solo MEDIDAS.md")
    g.add_argument("--planos", action="store_true", help="solo los planos por pieza")
    g.add_argument("--todo", action="store_true", help="todo, incluidos los ensambles por aro")
    a = ap.parse_args()
    plan = "rapido" if a.rapido else "medidas" if a.medidas else "planos" if a.planos else "normal"
    log_dir = HERE.parent / "salida" / "_logs_build"
    log_dir.mkdir(parents=True, exist_ok=True)
    print(f"Python {sys.version.split()[0]} - plan '{plan}{' + ensambles' if a.todo else ''}' - logs en {log_dir}", flush=True)
    t0 = time.time()
    ok = all([run(s, STEPS[s], log_dir) for s in PLANS[plan]])
    if a.todo:
        ok = ensambles(log_dir) and ok
    print(f"{'TODO BIEN' if ok else 'HUBO FALLAS (ver los logs)'} en {time.time() - t0:.0f} s", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
