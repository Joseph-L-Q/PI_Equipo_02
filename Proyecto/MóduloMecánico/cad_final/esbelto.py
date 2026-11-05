"""Slender-element rule (lab feedback 04/11): every vertical or slender element must be >= margen.esbelto_min (5 mm) thick,
with a 45 degree chamfer at its base. This file ENFORCES the thickness part, from params only (no CadQuery, no ray casting,
runs in milliseconds):

    python esbelto.py            (from cad_final/) exit 1 if any declared element is under the minimum; prints the table

Called from boya_pet.py main() (before the build) and from build.py next to the cama.py check.

REGISTRO   thicknesses of the buoy's slender elements, built from params (a param change is checked at once).
EXCEPCIONES  elements that are deliberately thinner, each with its reason (they are listed, never silently skipped).
NODO       hook for the node: append (name, thickness_mm) with register(), or create cad_final/esbelto_nodo.py with
           ELEMENTOS = [(name, thickness_mm), ...] (or a function elementos() returning that list): it is read here.
The thickness of a post/pillar/column/mast is its diameter (a tube: its wall); of a rib/strap/flange/ear/bar, its thin side.
"""
import importlib
import sys

import params as P

NODO = []


def register(name, t_mm, owner="nodo"):
    """Node (or any other) pipeline declares one slender element."""
    NODO.append((f"{owner}: {name}", float(t_mm)))


def registro():
    """[(element, thickness mm)] of the buoy, from params."""
    mo, mi, _ = P.PET_MAST
    kl, kw, kd = P.PET_KEY
    jf = P.PET_JOINT[0]
    return [
        ("B1/B5 costillas y topes bajos (boya_pet.costilla)", P.PET_RIB),
        ("B1/B5 brida de union por mitad (boya_pet.union[0])", jf),
        ("B1/B5 ancho de columna y almohadilla de union (boya_pet.union[1])", P.PET_JOINT[1]),
        ("B1/B2 pin de alineacion (boya_pet.union[2])", P.PET_JOINT[2]),
        ("B1/B2/B5 lengueta de union, seccion (boya_pet.llave[1])", kw),
        ("B1/B5 pared de fondo de la ranura de la lengueta (2 brida - salida - holgura)", 2 * jf - kl - kd),
        ("B1 postes M3 de la cubierta (boya_pet.poste_D)", P.PET_POST_D),
        ("B1 parche de amarre (boya_pet.ojal[1])", P.PET_EYE[1]),
        ("B5 lengueta de la cuna, ancho (boya_pet.lengueta[0])", P.PET_TONGUE[0]),
        ("B5 lengueta de la cuna, alto (boya_pet.lengueta[1])", P.PET_TONGUE[1]),
        ("B6 correa, espesor (boya_pet.correa[1])", P.PET_STRAP[1]),
        ("B6 correa, ancho (boya_pet.correa[0])", P.PET_STRAP[0]),
        ("B2 barras de la cubierta, espesor (boya_pet.cubierta_espesor)", P.PET_COVER_T),
        ("B2 barras de la cubierta, ancho (boya_pet.barra_ancho)", P.PET_BAR_W),
        ("B2 pilares bajo la caja (boya_pet.pilar[0])", P.PET_PILLAR[0]),
        ("B2 columnas del panel (boya_pet.columna_D)", P.PET_COLUMN_D),
        ("B2 mastil, pared ((D - d) / 2) (boya_pet.mastil)", (mo - mi) / 2),
        ("B3 orejas de la caja (boya_pet.oreja[2])", P.PET_EAR[2]),
        ("B3 brida de la caja (boya_pet.brida[1])", P.PET_FLANGE[1]),
        ("B3 postes de la bandeja (boya.poste_D)", P.BUOY_POST_D),
        ("B3 refuerzos del portabaterias (boya.apoyo_bateria_D)", P.BUOY_STANDOFF_D),
        ("B4 tapa bajo la ranura de la junta (tapa_espesor - ranura_prof)", P.PET_LID_T - P.GROOVE_DEPTH),
    ]


EXCEPCIONES = [
    ("B1/B5 paredes laterales del casco y la cuna (boya_pet.pared)", P.PET_WALL,
     "piel de cierre de 6 perimetros (margen.pared_min), sostenida por 5 costillas de 5 mm cada <= 64 mm y con ventanas; no recibe carga. "
     "Subirla a 5 cambia el ancho del canal y la altura del casco (decision abierta, ver DECISIONES.md)"),
    ("B3 paredes y piso de la caja seca (boya_pet.caja_pared)", P.PET_BOX_WALL,
     "placas apoyadas en sus 4 bordes y en la brida de 7 mm; la caja es el volumen seco (margen.pared_min)"),
    ("B1/B5 patin bajo la botella (boya_pet.pared)", P.PET_WALL, "placa horizontal de 24 mm de ancho sobre la cama; no es un elemento vertical"),
    ("B1/B2/B5 salida de la lengueta (boya_pet.llave[0])", P.PET_KEY[0],
     "es un taco de 4 mm de salida y 6 x 16 de base (relacion 0.7): no es esbelto; su espesor es la seccion, registrada arriba"),
]


def _nodo():
    out = list(NODO)
    try:
        m = importlib.import_module("esbelto_nodo")
    except ModuleNotFoundError:
        return out
    els = m.elementos() if hasattr(m, "elementos") else getattr(m, "ELEMENTOS", [])
    return out + [(f"nodo: {n}", float(t)) for n, t in els]


def check(verbose=True):
    """Returns the list of violations (empty = OK); prints the table when verbose."""
    tmin = P.SLENDER_T_MIN
    rows = registro() + _nodo()
    bad = [(n, t) for n, t in rows if t < tmin - 1e-9]
    if verbose:
        print(f"elementos esbeltos (minimo {tmin:g} mm): {len(rows)} declarados, {len(bad)} por debajo")
        for n, t in rows:
            print(f"  {'FALLA' if t < tmin - 1e-9 else 'ok   '} {t:5.1f}  {n}")
        for n, t, why in EXCEPCIONES:
            print(f"  excep {t:5.1f}  {n}: {why}")
    return bad


if __name__ == "__main__":
    sys.exit(1 if check() else 0)
