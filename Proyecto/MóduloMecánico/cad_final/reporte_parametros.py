"""Fase H: the params.py registry as tables for REPORTE_CAD.md: what changed (anterior -> nuevo, origen, razon) and
what still has to be measured or confirmed (estado por_verificar), grouped by origen.

    python reporte_parametros.py    (from cad_final/)   -> cad_final/reporte_parametros.md
"""
from collections import Counter
from pathlib import Path

import params as P

HERE = Path(__file__).resolve().parent


def fmt(v):
    if isinstance(v, float):
        return f"{v:g}"
    if isinstance(v, (tuple, list)):
        return " × ".join(fmt(x) for x in v)
    if isinstance(v, dict):
        return ", ".join(f"{k}: {fmt(x)}" for k, x in v.items())
    return str(v)


def cell(s):
    return str(s).replace("|", "/").replace("\n", " ")


def main():
    reg = list(P.REGISTRO.values())
    cnt = Counter((x.origen, x.estado) for x in reg)
    r = ["# Parámetros (generado por `reporte_parametros.py` desde `params.py`)", "",
         f"{len(reg)} parámetros. Por origen y estado: " +
         "; ".join(f"{o} / {e}: {n}" for (o, e), n in sorted(cnt.items())) + ".", "",
         "## 1. Qué cambió (tienen valor anterior)", "",
         "| Parámetro | Anterior | Nuevo | Origen | Estado | Razón |", "|---|---|---|---|---|---|"]
    for x in reg:
        if x.anterior is not None and x.anterior != x.value:
            r.append(f"| `{x.key}` | {cell(fmt(x.anterior))} | {cell(fmt(x.value))} | {x.origen} | {x.estado} | {cell(x.razon)} |")
    r += ["", "## 2. Qué hay que medir o confirmar (estado por_verificar)", ""]
    for origen in ("medido", "fabricante", "equipo", "estimado"):
        rows = [x for x in reg if x.estado != "confirmado" and x.origen == origen]
        if not rows:
            continue
        r += [f"### Origen {origen} ({len(rows)})", "", "| Parámetro | Valor | Razón |", "|---|---|---|"]
        r += [f"| `{x.key}` | {cell(fmt(x.value))} | {cell(x.razon)} |" for x in rows]
        r.append("")
    (HERE / "reporte_parametros.md").write_text("\n".join(r) + "\n", encoding="utf-8")
    print("written reporte_parametros.md", len(reg), dict(cnt))


if __name__ == "__main__":
    main()
