"""Slender elements of the node (M1s, M2, M3s, M3f, M4, M5s, hook), read by esbelto.py. Built from params: a param change is checked at once.
Thickness = the thin side (wall, rib, ear, bar). Every value must be >= margen.esbelto_min (5 mm)."""
import params as P


def elementos():
    eye = P.HANDLE_EYE
    bar = P.HANDLE_H - 8.0 - (P.HANDLE_GRIP - P.BRIDGE_MAX) / 2     # bar over the glove window of M2 (wall_h 8 in caja_central.box_lid)
    return [
        ("M1s pared de la caja", P.BOX_WALL),
        ("M1s fondo de la caja", P.BOX_FLOOR),
        ("M2 barra del asa sobre la ventana", bar),
        ("M2 anillo del ojo en la punta de la gota", eye[0] / 2 - eye[1] / 2 * 2 ** 0.5),
        ("M3f pared del bolsillo de lastre", P.PLATE_POCKET_WALL),
        ("M3f oreja de M1s (ancho)", P.FRAME_LUGS["ancho"]),
        ("M3s costilla de apoyo en la cama", P.RAIL_BED_RIBS["ancho"]),
        ("M3s pared del gancho", P.JAW_WALL),
        ("M4 pared de la capsula", P.CAP_WALL),
        ("M11 repisa de la cuna", P.TRAY_CRADLE_T),
    ]
