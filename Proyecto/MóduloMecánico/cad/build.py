"""Build every part, the assembly and the verification report.

    python build.py            # parts + assemblies + checks
Outputs (relative to Proyecto/MóduloMecánico/):
    step/*.step, stl/*.stl, cad/reporte_verificacion.md
"""
import math
import sys
from pathlib import Path

import cadquery as cq
import numpy as np
import trimesh
from OCP.BOPAlgo import BOPAlgo_ArgumentAnalyzer
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.ShapeFix import ShapeFix_Shape
from OCP.ShapeUpgrade import ShapeUpgrade_UnifySameDomain

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import parts as P  # noqa: E402
from params import *  # noqa: E402,F403

MOD = HERE.parent
STEP_DIR, STL_DIR = MOD / "step", MOD / "stl"
STEP_DIR.mkdir(exist_ok=True)
STL_DIR.mkdir(exist_ok=True)

ACRYLIC_DENSITY = 1.19   # g/cm3
HARDWARE_G = 60.0        # [sup] M3/M4 screws, nuts, inserts, 3 glands

# part id, file stem, builder, material, qty, print orientation (rotation applied before the bed check)
PARTS = [
    ("M1", "M1_caja_central_cuerpo", P.box_body, "PETG", 1, ("X", 0)),
    ("M2", "M2_caja_central_tapa", P.box_lid, "PETG", 1, ("X", 0)),
    ("M3", "M3_brazo", P.arm, "PETG", 2, ("Y", -90)),        # standing on the root flange
    ("M4", "M4_capsula_cuerpo_P4revB", P.capsule_body, "PETG", 2, ("Y", -90)),   # standing on the rear flange
    ("M5", "M5_capsula_tapa", P.capsule_lid, "PETG", 2, ("Y", 90)),       # inner face (groove) down
    ("M6", "M6_bisel_ventana", P.bezel, "PETG", 2, ("Y", -90)),
    ("M7", "M7_ventana", P.window_disc, "acrílico 3 mm (comprado, cortado)", 2, None),
    ("M8", "M8_marco_malla_prueba", P.mesh_frame, "PETG", 1, ("X", 0)),
]


def loc(t=(0, 0, 0), axis=(0, 0, 1), ang=0.0):
    return cq.Location(cq.Vector(*t), cq.Vector(*axis), ang)


MIN_EDGE, MIN_FACE = 0.05, 0.01   # mm, mm²: below this Parasolid (Onshape) tends to flag slivers


def sanitize(wp):
    """clean() + ShapeFix_Shape + UnifySameDomain + ShapeFix_Shape, before any export."""
    sf = ShapeFix_Shape(wp.clean().val().wrapped)
    sf.SetPrecision(1e-6)
    sf.SetMaxTolerance(1e-3)
    sf.Perform()
    u = ShapeUpgrade_UnifySameDomain(sf.Shape(), True, True, True)
    u.Build()
    sf2 = ShapeFix_Shape(u.Shape())
    sf2.Perform()
    return cq.Shape.cast(sf2.Shape())


def brep_check(stem, shape):
    """BRepCheck + BOPAlgo_ArgumentAnalyzer + sliver scan. Aborts the build on any fault."""
    aa = BOPAlgo_ArgumentAnalyzer()
    aa.SetShape1(shape.wrapped)
    for m in ("SelfInterMode", "SmallEdgeMode", "RebuildFaceMode", "TangentMode", "MergeVertexMode",
              "MergeEdgeMode", "ContinuityMode", "CurveOnSurfaceMode"):
        setattr(aa, m, True)
    aa.Perform()
    c = dict(brep=BRepCheck_Analyzer(shape.wrapped, True).IsValid(), bop=not aa.HasFaulty(),
             solids=len(shape.Solids()), min_edge=min(e.Length() for e in shape.Edges()),
             min_face=min(f.Area() for f in shape.Faces()))
    ok = c["brep"] and c["bop"] and c["solids"] == 1 and c["min_edge"] >= MIN_EDGE and c["min_face"] >= MIN_FACE
    if not ok:
        raise SystemExit(f"B-rep check failed for {stem}: {c}")
    return c


def export_part(stem, wp):
    shape = sanitize(wp)
    check = brep_check(stem, shape)
    out = cq.Workplane().add(shape)
    cq.exporters.export(out, str(STEP_DIR / f"{stem}.step"))
    cq.exporters.export(out, str(STL_DIR / f"{stem}.stl"), tolerance=0.05, angularTolerance=0.2)
    # round trip: the STEP written to disk must read back as the same valid solid
    back = cq.importers.importStep(str(STEP_DIR / f"{stem}.step")).val()
    if not (BRepCheck_Analyzer(back.wrapped, True).IsValid() and abs(back.Volume() - shape.Volume()) < 1e-3 * shape.Volume()):
        raise SystemExit(f"STEP round trip failed for {stem}")
    return shape, check


def mesh_checks(stem, orient):
    m = trimesh.load(STL_DIR / f"{stem}.stl")
    res = {"watertight": bool(m.is_watertight), "bodies": len(m.split(only_watertight=False)),
           "vol_cm3": m.volume / 1000.0}
    if orient:
        ax, ang = orient
        vec = {"X": [1, 0, 0], "Y": [0, 1, 0], "Z": [0, 0, 1]}[ax]
        m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(ang), vec))
    ext = m.bounds[1] - m.bounds[0]
    res["bbox"] = ext
    res["fits_bed"] = bool(ext[0] <= PRINT_BED[0] and ext[1] <= PRINT_BED[1] and ext[2] <= PRINT_BED[2])
    zmin = m.bounds[0][2]
    n = m.face_normals
    centers = m.triangles_center
    over = (n[:, 2] < -0.7072) & (centers[:, 2] > zmin + 0.3)
    res["overhang_mm2"] = float(m.area_faces[over].sum())
    return res


def build_capsule_set(tilt):
    """Capsule parts in capsule frame, then rotated nose-down by `tilt` about the hinge (Y)."""
    rot = loc((0, 0, 0), (0, 1, 0), tilt)
    return {k: f().val().moved(rot) for k, f in
            (("body", P.capsule_body), ("lid", P.capsule_lid), ("window", P.window_disc),
             ("bezel", P.bezel), ("camera", P.camera_dummy))}


def main():
    report = ["# Reporte de verificación (generado por `build.py`)", "",
              "No editar a mano: se regenera. Valores en mm, cm³, g y MPa.", ""]

    # ------------------------------------------------------------ parts
    shapes, rows, checks = {}, [], {}
    for pid, stem, f, mat, qty, orient in PARTS:
        wp = f()
        shapes[pid], checks[pid] = export_part(stem, wp)
        mc = mesh_checks(stem, orient)
        valid = shapes[pid].isValid()
        mass = mc["vol_cm3"] * (PETG_DENSITY if mat == "PETG" else ACRYLIC_DENSITY)
        rows.append((pid, stem, mat, qty, valid, mc, mass))

    report += ["## 1. Piezas: sólido cerrado e imprimible", "",
               f"Cama supuesta {PRINT_BED[0]:.0f} × {PRINT_BED[1]:.0f} × {PRINT_BED[2]:.0f} mm. Voladizo = caras con "
               "normal hacia abajo a más de 45° de la vertical, fuera de la cama, en la orientación de impresión indicada.",
               "",
               "| Pieza | Archivo | Material | Cant. | Sólido válido | Estanco (STL) | Cuerpos | Volumen cm³ | Masa g (100 % relleno) | Caja en orientación de impresión | Cabe en la cama | Voladizo mm² |",
               "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for pid, stem, mat, qty, valid, mc, mass in rows:
        bb = " × ".join(f"{v:.0f}" for v in mc["bbox"])
        report.append(f"| {pid} | `{stem}` | {mat} | {qty} | {'sí' if valid else 'NO'} | "
                      f"{'sí' if mc['watertight'] else 'NO'} | {mc['bodies']} | {mc['vol_cm3']:.1f} | {mass:.0f} | "
                      f"{bb} | {'sí' if mc['fits_bed'] else 'NO'} | {mc['overhang_mm2']:.0f} |")
    report += ["", "Antes de exportar, cada pieza pasa por `clean()`, `ShapeFix_Shape` y `UnifySameDomain` (OCP), y luego "
               f"por `BRepCheck_Analyzer`, `BOPAlgo_ArgumentAnalyzer` y un barrido de astillas (arista ≥ {MIN_EDGE} mm, "
               f"cara ≥ {MIN_FACE} mm²). Si algo falla, el build se detiene. El STEP escrito se vuelve a leer y se compara.", "",
               "| Pieza | BRepCheck | BOPAlgo | Sólidos | Arista mínima mm | Cara mínima mm² |", "|---|---|---|---|---|---|"]
    for pid, c in checks.items():
        report.append(f"| {pid} | {'ok' if c['brep'] else 'FALLA'} | {'ok' if c['bop'] else 'FALLA'} | {c['solids']} | "
                      f"{c['min_edge']:.2f} | {c['min_face']:.2f} |")
    report.append("")
    petg_mass = sum(m * q for pid, _, mat, q, _, _, m in rows if mat == "PETG" and pid != "M8")
    win_mass = sum(m * q for pid, _, mat, q, _, _, m in rows if pid == "M7")

    # ------------------------------------------------------------ derived thicknesses
    cap_fl_w = CAP_CAV_W + 2 * CAP_WALL + 2 * CAP_FLANGE
    cl = (CAP_CAV_W + (cap_fl_w - CAP_FLANGE)) / 2
    cap_screw = cap_fl_w / 2 - CAP_FLANGE / 2
    box_out_w = BOX_CAV_W + 2 * BOX_WALL
    box_cl = (BOX_CAV_W + box_out_w + BOX_FLANGE) / 2
    box_screw = box_out_w / 2 + BOX_FLANGE / 2
    walls = [
        ("Hombro de la ventana (pared frontal − asiento)", CAP_FRONT - WIN_SEAT_DEPTH),
        ("Tapa cápsula bajo la ranura del O-ring", CAP_LID_T - GROOVE_DEPTH),
        ("Tapa caja bajo la ranura del O-ring", BOX_LID_T - GROOVE_DEPTH),
        ("Ranura ↔ agujero de tornillo (cápsula)", cap_screw - M3_CLEAR / 2 - (cl / 2 + GROOVE_WIDTH / 2)),
        ("Ranura ↔ cavidad (cápsula)", (cl / 2 - GROOVE_WIDTH / 2) - CAP_CAV_W / 2),
        ("Ranura ↔ agujero de tornillo (caja, lado corto)", box_screw - M3_CLEAR / 2 - (box_cl / 2 + GROOVE_WIDTH / 2)),
        ("Ranura ↔ cavidad (caja, lado corto)", (box_cl / 2 - GROOVE_WIDTH / 2) - BOX_CAV_W / 2),
        ("Fondo del inserto M3 ↔ cavidad (almohadilla del brazo)", ARM_PAD_T + BOX_WALL - M3_INSERT_DEPTH),
        ("Agujero piloto M2 del bisel ↔ cavidad", CAP_FRONT - 4.0),
        ("Pared de brazo", ARM_WALL),
        ("Barra de malla de prueba", MESH_BAR),
    ]
    report += ["", "## 2. Espesores mínimos que quedan bajo cada corte", "",
               f"Mínimo aceptado: {MIN_WALL} mm (3 perímetros de boquilla 0.4).", "",
               "| Zona | Espesor mm | ¿≥ mínimo? |", "|---|---|---|"]
    for name, t in walls:
        report.append(f"| {name} | {t:.2f} | {'sí' if t >= MIN_WALL - 1e-6 else 'NO'} |")

    # ------------------------------------------------------------ assembly placement
    out_l, out_w, out_h = P.box_dims()
    zc = -out_h / 2                            # origin = centre of the box body
    z_arm = P.arm_z() + zc
    x_root = out_l / 2 + ARM_PAD_T
    hinge = (x_root + P.arm_axis_x(), 0.0, z_arm)
    assert CAM_TILT_DEG % (360 / HINGE_TEETH) == 0, "tilt must be a multiple of the tooth pitch"

    box_loc = loc((0, 0, zc))
    arm_loc_r = loc((x_root, 0, z_arm))
    flip = loc((0, 0, 0), (0, 0, 1), 180)

    assy = cq.Assembly(name="LanternGuard_modulo_mecanico")
    colors = {"petg": cq.Color(0.85, 0.2, 0.18), "lid": cq.Color(0.95, 0.95, 0.95), "arm": cq.Color(0.25, 0.25, 0.28),
              "win": cq.Color(0.6, 0.8, 1.0, 0.5), "frame": cq.Color(0.2, 0.55, 0.35)}
    assy.add(shapes["M1"], name="M1_caja_cuerpo", loc=box_loc, color=colors["petg"])
    assy.add(shapes["M2"], name="M2_caja_tapa", loc=box_loc, color=colors["lid"])
    world = [shapes["M1"].moved(box_loc), shapes["M2"].moved(box_loc)]
    for side, pre in (("der", loc()), ("izq", flip)):
        al = pre * arm_loc_r
        assy.add(shapes["M3"], name=f"M3_brazo_{side}", loc=al, color=colors["arm"])
        world.append(shapes["M3"].moved(al))
        cl_ = pre * loc(hinge) * loc((0, 0, 0), (0, 1, 0), CAM_TILT_DEG)
        for pid, nm, col in (("M4", "capsula_cuerpo", "petg"), ("M5", "capsula_tapa", "lid"),
                             ("M6", "bisel", "lid"), ("M7", "ventana", "win")):
            assy.add(shapes[pid], name=f"{pid}_{nm}_{side}", loc=cl_, color=colors[col])
            world.append(shapes[pid].moved(cl_))
    assy.export(str(STEP_DIR / "ENSAMBLE_modulo.step"))
    back = cq.importers.importStep(str(STEP_DIR / "ENSAMBLE_modulo.step"))
    bad = [i for i, so in enumerate(back.solids().vals()) if not BRepCheck_Analyzer(so.wrapped, True).IsValid()]
    if bad or len(back.solids().vals()) != len(world):
        raise SystemExit(f"ENSAMBLE_modulo.step round trip: {len(back.solids().vals())} solids, invalid {bad}")
    report_assy = f"`ENSAMBLE_modulo.step` releído: {len(world)} sólidos, todos válidos según BRepCheck."
    module = cq.Compound.makeCompound(world)
    cq.exporters.export(cq.Workplane().add(module), str(STL_DIR / "ENSAMBLE_modulo.stl"), tolerance=0.1, angularTolerance=0.3)

    # test bench: + mesh frame in front of the right camera, perpendicular to its optical axis
    t = math.radians(CAM_TILT_DEG)
    d = np.array([math.cos(t), 0.0, -math.sin(t)])
    x_front = P.cap_dims()[6]
    win_c = np.array(hinge) + x_front * d
    fc = win_c + TEST_DISTANCE * d
    frame_loc = loc(tuple(fc), (0, 1, 0), 90 + CAM_TILT_DEG)
    assy.add(shapes["M8"], name="M8_marco_malla_prueba", loc=frame_loc, color=colors["frame"])
    assy.export(str(STEP_DIR / "ENSAMBLE_banco_prueba.step"))
    bench = cq.Compound.makeCompound(world + [shapes["M8"].moved(frame_loc)])
    cq.exporters.export(cq.Workplane().add(bench), str(STL_DIR / "ENSAMBLE_banco_prueba.stl"), tolerance=0.1, angularTolerance=0.3)

    # ------------------------------------------------------------ fit and interference
    report += ["", "## 3. Encaje de componentes e interferencias", "", report_assy, ""]
    report += ["| Par | Volumen de interferencia mm³ | Holgura mínima mm | Resultado |", "|---|---|---|---|"]

    def pair(name, a, b, need_gap=None, tol=0.5):
        v = a.intersect(b).Volume()
        gap = a.distance(b) if v < tol else 0.0
        ok = v < tol and (need_gap is None or gap >= need_gap - 1e-6)
        report.append(f"| {name} | {v:.2f} | {gap:.2f} | {'OK' if ok else 'REVISAR'} |")
        return ok

    box_b, box_l = shapes["M1"], shapes["M2"]
    for nm, comp in P.box_components():
        pair(f"{nm} ↔ caja (cuerpo)", comp.val(), box_b, None if "probe" in nm else CLEARANCE)
        pair(f"{nm} ↔ caja (tapa)", comp.val(), box_l, CLEARANCE)
    # PG7 locknuts inside the end walls (hex 15 AF ~ 17.3 across corners, 6 thick)
    for s in (1, -1):
        xw = s * (BOX_CAV_L / 2)
        nut = (cq.Workplane("YZ").workplane(offset=xw - (6 if s > 0 else 0)).center(0, P.arm_z())
               .polygon(6, PG7_NUT_AF / math.cos(math.pi / 6)).extrude(6)).val()
        for nm, comp in P.box_components():
            pair(f"contratuerca PG7 ({'+' if s > 0 else '−'}X) ↔ {nm}", nut, comp.val(), CLEARANCE)
    # PG9 locknut under the lid
    out_l, out_w, out_h = P.box_dims()
    nut9 = (cq.Workplane("XY").workplane(offset=out_h - NUT_T).center(0, LID_GLAND_Y)
            .polygon(6, PG9_NUT_AF / math.cos(math.pi / 6)).extrude(NUT_T)).val()
    pair("contratuerca PG9 (tapa) ↔ caja (cuerpo)", nut9, box_b)
    for nm, comp in P.box_components():
        pair(f"contratuerca PG9 (tapa) ↔ {nm}", nut9, comp.val(), CLEARANCE)
    cam = P.camera_dummy().val()
    x0c = P.cap_dims()[5]
    nut7 = (cq.Workplane("XY").workplane(offset=-CAP_CAV_H / 2).center(x0c + CAP_GLAND_X, 0)
            .polygon(6, PG7_NUT_AF / math.cos(math.pi / 6)).extrude(NUT_T)).val()
    pair("contratuerca PG7 (cápsula) ↔ cámara", nut7, cam, CLEARANCE)
    pair("contratuerca PG7 (cápsula) ↔ cápsula (cuerpo)", nut7, P.capsule_body().val())
    pair("contratuerca PG7 (cápsula) ↔ cápsula (tapa)", nut7, P.capsule_lid().val())
    pair("cámara ↔ cápsula (cuerpo)", cam, P.capsule_body().val(), CLEARANCE)
    pair("cámara ↔ cápsula (tapa)", cam, P.capsule_lid().val(), CLEARANCE)
    pair("ventana ↔ cápsula (cuerpo)", P.window_disc().val(), P.capsule_body().val())

    report += ["", "Bisagra: la lengüeta de la tapa engrana con las orejas del brazo. Se comprueba el cuerpo de la "
               "cápsula contra el brazo en todo el rango; los dientes de la tapa contra los del brazo se reportan aparte "
               "porque se tocan por diseño (flanco con flanco).", "",
               "| Ángulo | Cuerpo cápsula ↔ brazo mm³ | Holgura mm | Tapa (sin dientes) ↔ brazo mm³ |", "|---|---|---|---|"]
    arm_local = shapes["M3"].moved(loc((-P.arm_axis_x(), 0, 0)))      # arm in hinge frame
    for ang in (0, 10, 20, 30, 40, 50, 60, 70, 80, 90):
        cs = build_capsule_set(ang)
        v1 = cs["body"].intersect(arm_local).Volume()
        g1 = cs["body"].distance(arm_local) if v1 < 0.5 else 0.0
        lid_core = cs["lid"].cut(cq.Workplane("XZ").circle(HINGE_DISC_D / 2 + 0.5).extrude(20, both=True).val())
        v2 = lid_core.intersect(arm_local).Volume()
        report.append(f"| {ang}° | {v1:.2f} | {g1:.2f} | {v2:.2f} |")
    teeth_v = build_capsule_set(CAM_TILT_DEG)["lid"].intersect(arm_local).Volume()
    report.append("")
    report.append(f"Dientes engranados a {CAM_TILT_DEG:.0f}° (ángulo de trabajo): solape {teeth_v:.2f} mm³ "
                  "(≈ 0 = flancos en contacto, sin juego ni choque).")

    # ------------------------------------------------------------ buoyancy
    cav_box = BOX_CAV_L * BOX_CAV_W * BOX_CAV_H / 1000
    cav_cap = CAP_CAV_W * CAP_CAV_H * CAP_CAV_L / 1000
    sealed_air = cav_box + 2 * cav_cap
    comp_mass = sum(v[3] for k, v in COMPONENTS.items() if k != "arducam_mega_5mp") + 2 * COMPONENTS["arducam_mega_5mp"][3]
    petg_vol = petg_mass / PETG_DENSITY
    win_vol = win_mass / ACRYLIC_DENSITY
    total_mass = petg_mass + win_mass + comp_mass + CABLE_MASS_G + HARDWARE_G
    displaced = petg_vol + win_vol + sealed_air + HARDWARE_G / 7.9
    apparent_g = total_mass - SEAWATER_DENSITY * displaced
    lo, hi = 200, 500
    ballast_lo = (lo - apparent_g)
    ballast_hi = (hi - apparent_g)
    report += ["", "## 4. Peso y flotabilidad (exigencia: peso aparente de 0.2 a 0.5 kgf; ≤ 3 kg en aire)", "",
               "| Concepto | Valor |", "|---|---|",
               f"| PETG impreso (sin el marco de prueba), 100 % relleno | {petg_mass:.0f} g |",
               f"| Ventanas de acrílico | {win_mass:.0f} g |",
               f"| Electrónica (datasheets, ver params.py) | {comp_mass:.0f} g |",
               f"| Cables y prensaestopas (supuesto) | {CABLE_MASS_G:.0f} g |",
               f"| Tornillería (supuesto) | {HARDWARE_G:.0f} g |",
               f"| **Masa total en aire** | **{total_mass:.0f} g** ({'cumple' if total_mass <= 3000 else 'NO cumple'} ≤ 3 kg) |",
               f"| Aire sellado (caja {cav_box:.0f} + 2 cápsulas × {cav_cap:.0f}) | {sealed_air:.0f} cm³ |",
               f"| Volumen desplazado | {displaced:.0f} cm³ |",
               f"| Empuje en agua de mar ({SEAWATER_DENSITY} g/cm³) | {SEAWATER_DENSITY * displaced:.0f} g |",
               f"| **Peso aparente** | **{apparent_g:.0f} g** ({'flota' if apparent_g < 0 else 'se hunde'}) |",
               f"| Lastre para entrar en 0.2 a 0.5 kgf | {ballast_lo:.0f} a {ballast_hi:.0f} g de peso aparente "
               f"(acero inoxidable: ×1.15 en aire, ≈ {ballast_lo * 1.15:.0f} a {ballast_hi * 1.15:.0f} g) |",
               "", "El relleno real < 100 % baja la masa y deja aire atrapado en las paredes: el peso aparente real "
               "será más negativo. Medir en balde y ajustar el lastre."]

    # ------------------------------------------------------------ plate stresses (Roark)
    # Roark's Formulas for Stress and Strain, 7th ed., Table 11.4, case 1a (all edges simply supported,
    # uniform load): sigma_max = beta q b^2 / t^2 ; y_max = alpha q b^4 / (E t^3). Conservative vs clamped.
    beta_t = [(1.0, 0.2874, 0.0444), (1.2, 0.3762, 0.0616), (1.4, 0.4530, 0.0770), (1.6, 0.5172, 0.0906),
              (1.8, 0.5688, 0.1017), (2.0, 0.6102, 0.1110), (3.0, 0.7134, 0.1335), (4.0, 0.7410, 0.1400),
              (5.0, 0.7476, 0.1417), (1e9, 0.7500, 0.1421)]

    def coef(r):
        for (r0, b0, a0), (r1, b1, a1) in zip(beta_t, beta_t[1:]):
            if r0 <= r <= r1:
                f = (r - r0) / (r1 - r0)
                return b0 + f * (b1 - b0), a0 + f * (a1 - a0)
        return beta_t[0][1], beta_t[0][2]

    E_PETG = 1700.0
    panels = [("Tapa de la caja", BOX_CAV_L, BOX_CAV_W, BOX_LID_T), ("Fondo de la caja", BOX_CAV_L, BOX_CAV_W, BOX_FLOOR),
              ("Pared lateral de la caja", BOX_CAV_L, BOX_CAV_H, BOX_WALL),
              ("Pared extrema de la caja", BOX_CAV_W, BOX_CAV_H, BOX_WALL),
              ("Pared de la cápsula", CAP_CAV_L, CAP_CAV_W, CAP_WALL), ("Tapa de la cápsula", CAP_CAV_W, CAP_CAV_H, CAP_LID_T)]
    q = DESIGN_PRESSURE
    report += ["", f"## 5. Presión a {DESIGN_DEPTH_M:.0f} m ({q} MPa): placa plana, estimación de Roark", "",
               "Fórmula: σ = β·q·b²/t², y = α·q·b⁴/(E·t³). Roark, *Formulas for Stress and Strain*, 7.ª ed., "
               "tabla 11.4 caso 1a (bordes simplemente apoyados, más conservador que empotrado). "
               f"σy PETG = {PETG_YIELD} MPa, E = {E_PETG:.0f} MPa (valores tentativos del T01).", "",
               "| Panel | a × b mm | t mm | β | σ MPa | FS = σy/σ | Flecha mm |", "|---|---|---|---|---|---|---|"]
    for name, a, b, t_ in panels:
        a_, b_ = max(a, b), min(a, b)
        beta, alpha = coef(a_ / b_)
        sig = beta * q * b_ ** 2 / t_ ** 2
        y = alpha * q * b_ ** 4 / (E_PETG * t_ ** 3)
        report.append(f"| {name} | {a_:.0f} × {b_:.0f} | {t_:.0f} | {beta:.3f} | {sig:.1f} | {PETG_YIELD / sig:.1f} | {y:.2f} |")
    report += ["", "**Límites de esta estimación.** (1) Roark supone placa sin agujeros: el agujero del sensor JSN-SR04T "
               "está en el centro del fondo, donde el momento es máximo, con un factor de concentración Kt ≈ 2. "
               "(2) En las paredes laterales la flexión cruza las capas de impresión, la dirección débil del FDM "
               "(resistencia entre capas del orden de la mitad). Con ambos efectos, el factor de seguridad efectivo del "
               "fondo y de las paredes laterales baja a **≈ 2**, no a los valores de la tabla. **No está probado**: falta "
               "el ensayo en cámara de presión o a profundidad. Las simulaciones SimScale del equipo usaron 50 kPa (≈ 5 m), "
               "un tercio de esta carga."]

    # ------------------------------------------------------------ seal
    squeeze = (ORING_CORD - GROOVE_DEPTH) / ORING_CORD * 100
    fill = (math.pi * (ORING_CORD / 2) ** 2) / (GROOVE_WIDTH * GROOVE_DEPTH) * 100
    report += ["", "## 6. Junta tórica (sello de cara, estático)", "",
               f"Cordón Ø{ORING_CORD} mm en ranura de {GROOVE_WIDTH} × {GROOVE_DEPTH} mm: compresión {squeeze:.0f} % "
               f"(rango habitual 15 a 30 % para sello estático), llenado de ranura {fill:.0f} % (< 90 %). "
               "Calculado, **no probado**."]

    out = HERE / "reporte_verificacion.md"
    out.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    main()
