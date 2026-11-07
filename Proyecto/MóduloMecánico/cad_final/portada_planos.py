"""Cover page of PLANOS_LanternGuard.pdf (A4 landscape): what is inside and how the drawings are used.

    python portada_planos.py <commit>      -> ../planos/cad_final/_portada.pdf
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "planos" / "cad_final" / "_portada.pdf"
SETS = [("P2", "P2 robusto", "nodo recomendado para las pruebas en piscina (riel en celosía, pared 5, gancho en C)"),
        ("P4", "P4 estético", "nodo recomendado para presentar (caja y riel en una pieza, redondeos, logo en relieve)"),
        ("BP", "Boya PET", "casco central + 2 cunas con 4 botellas de 1 L en cruz + espuma PU, caja seca, cubierta con el panel y el mástil")]


def main(commit="?"):
    fig = plt.figure(figsize=(297 / 25.4, 210 / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 297)
    ax.set_ylim(0, 210)
    ax.axis("off")
    ax.add_patch(Rectangle((8, 8), 281, 194, fill=False, lw=1.2))
    ax.text(24, 180, "LanternGuard: planos de piezas", fontsize=22, weight="bold")
    ax.text(24, 170, "Equipo 02 · Proyecto Integrador · módulo mecánico", fontsize=11, color="#444")
    y = 150
    for code, name, what in SETS:
        n = len(list((OUT.parent / code).glob("*.pdf")))
        ax.text(24, y, f"{name}  ({n} láminas, código {code}_...)", fontsize=12, weight="bold")
        ax.text(24, y - 6, what, fontsize=9.5, color="#333")
        y -= 20
    notes = ["Para imprimir en la Bambu Lab P1P se usan los STL o los 3MF de salida/imprimir_hoy/, no estos planos.",
             "Los planos sirven para verificar las piezas impresas y para el informe.",
             "Cada lámina: frente, planta y lado (primer diedro), isométrica, medidas generales, material, relleno,",
             "orientación de impresión, cantidad y los gramos y horas del slicer (OrcaSlicer, PETG, 0.20 mm).",
             "Las medidas marcadas como estimadas (aro.seccion = 8 mm, KIT A, botellas) se confirman midiendo; ver MEDIDAS.md."]
    y -= 2
    for t in notes:
        ax.text(24, y, t, fontsize=9.5)
        y -= 6.5
    ax.text(24, 18, f"Generado desde el modelo paramétrico (cad_final, params.py), rama cad/version-final, commit {commit}.",
            fontsize=8.5, color="#444")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, metadata={"CreationDate": None})
    plt.close(fig)
    print("written", OUT)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "?")
