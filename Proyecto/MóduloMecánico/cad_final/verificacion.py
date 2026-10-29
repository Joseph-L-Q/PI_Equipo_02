"""Fase E: hand verification (formulas and units in the report). Only the rail cross-sections come from CAD (thin slab
of the real pieces, so the T-slot, ribs and thickened lap walls count); everything else is arithmetic on params.py.
Where a capacity is not known (inserts, bolt grade, acrylic), the report gives the demand, not an invented safety factor.

    python verificacion.py      (from cad_final/)   -> cad_final/reporte_verificacion.md
"""
import math
from pathlib import Path

import cadquery as cq
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.gp import gp_Ax1, gp_Dir, gp_Pnt

import camara as CH
import capsula as CP
import caja_central as C
import fase_a as FA
import gancho as G
import largo_riel as LR
import layout as LY
import riel as R
from params import (BASE_M4_PTS, BOX_FLOOR, BOX_LID_T, BOX_WALL, CAP_WALL, CAPSULE_CONTENT_G, CAPSULE_SET_G,
                    CARRIAGE_TRAVEL, FIT_CLEAR, HANDLE_GRIP, HANDLE_H, HANDLING_LOAD_N, HINGE_DISC_D, HINGE_EAR_T,
                    HINGE_GAP, HINGE_TEETH, HINGE_TEETH_RIN, HINGE_TOOTH_H, HOOK_CONTACT_W, HOOK_FLANGE, HOOK_LOAD_N, KNOB_D,
                    KNOB_FREE_EXTRA, LENS_APERTURE, M4_CLEAR, M4_NUT, PETG_E, PETG_NU, PETG_YIELD, PETG_YIELD_Z,
                    RAIL_DOVETAIL, RAIL_DOVETAIL_KEY, RAIL_CENTRAL_L, RAIL_EXT_L, RAIL_EXT_PER_RING, RAIL_LAP_Z,
                    RAIL_SECTION, RAIL_TSLOT, RING_DIAMETERS, DESIGN_PRESSURE, WIN_T)

HERE = Path(__file__).resolve().parent
F = HANDLING_LOAD_N
G0 = 9.81e-3                              # N per g
ROARK = [(1.0, 0.2874, 0.0444), (1.2, 0.3762, 0.0616), (1.4, 0.4530, 0.0770), (1.6, 0.5172, 0.0906),
         (1.8, 0.5688, 0.1017), (2.0, 0.6102, 0.1110), (3.0, 0.7134, 0.1335), (4.0, 0.7410, 0.1400),
         (5.0, 0.7476, 0.1417), (1e9, 0.7500, 0.1421)]   # copied from ../cad/build.py (Roark 7th ed., table 11.4, 1a)


def fs(sig):
    return (PETG_YIELD / sig, PETG_YIELD_Z / sig) if sig > 0 else (math.inf, math.inf)


# ------------------------------------------------------------------ rail sections from CAD
def section_props(shape, x, t=0.05):
    """Area and second moment about the horizontal centroidal axis (bending under vertical loads) of the cut at x."""
    bb = shape.BoundingBox()
    slab = cq.Solid.makeBox(t, bb.ylen + 2, bb.zlen + 2, cq.Vector(x - t / 2, bb.ymin - 1, bb.zmin - 1))
    cut = shape.intersect(slab)
    pr = GProp_GProps()
    BRepGProp.VolumeProperties_s(cut.wrapped, pr)
    com = pr.CentreOfMass()
    A = pr.Mass() / t
    Iy = pr.MomentOfInertia(gp_Ax1(gp_Pnt(com.X(), com.Y(), com.Z()), gp_Dir(0, 1, 0))) / t
    zb = cut.BoundingBox()
    c = max(zb.zmax - com.Z(), com.Z() - zb.zmin)
    return dict(A=A, I=Iy, c=c, Z=Iy / c, zc=com.Z())


def rail_sections(lay, c):
    ext = R.ext(c, 0.0).val()
    cen = R.central(lay, c).val()
    lap = RAIL_DOVETAIL
    out = {"ext_medio": section_props(ext, RAIL_EXT_L / 2),
           "ext_ranura_salida": section_props(ext, RAIL_EXT_L - R.RAIL_EXIT_SLOT[2] - R.RAIL_EXIT_SLOT[1] / 2)}
    # half sections in the lap: female (central end, top half) and male (ext inner end, bottom half), worst over the lap
    xs = [c.x_joint + lap * k / 6 for k in range(1, 6)]
    cen0 = cen.moved(cq.Location(cq.Vector(0, 0, -c.z_rail)))
    out["union_hembra"] = min((section_props(cen0, x) for x in xs), key=lambda d: d["Z"])
    out["union_macho"] = min((section_props(ext, x) for x in (lap * k / 6 for k in range(1, 6))), key=lambda d: d["Z"])
    return out


# ------------------------------------------------------------------ geometry of the node along the rail
def rail_tip(n):
    """Outer end of the rail with n extensions per side (riel.py places each one overlapping the previous by LAP)."""
    return RAIL_CENTRAL_L / 2 + n * (RAIL_EXT_L - RAIL_DOVETAIL)


def load_x(n):
    """Worst lever: carriage with its sleeve end flush on the tip (s = 0), load at the hinge axis."""
    return rail_tip(n) + CP.carriage_axis()[0]


# ------------------------------------------------------------------ main
def main():
    lay = LY.build(floors=1)
    c = CH.dims(lay)
    sec = rail_sections(lay, c)
    r = ["# Verificación a mano (generado por `verificacion.py`)", "",
         f"Carga de manipulación: {F:g} N en una cápsula; gancho: {HOOK_LOAD_N:g} N. PETG: E {PETG_E:g} MPa, ν {PETG_NU:g}, "
         f"σy {PETG_YIELD:g} MPa macizo (a lo largo de las capas) y {PETG_YIELD_Z:g} MPa entre capas. Todos estimados. "
         "FS = σ admisible / σ calculada; se dan las dos columnas y se dice cuál aplica según la orientación de impresión.", ""]

    # 1. rail sections
    r += ["## 1. Secciones del riel (cortes del CAD)", "",
          "Corte de 0.05 mm del sólido real; I respecto del eje horizontal que pasa por el centroide; Z = I / c.", "",
          "| Sección | A mm² | I mm⁴ | c mm | Z mm³ |", "|---|---|---|---|---|"]
    for k, d in sec.items():
        r.append(f"| {k} | {d['A']:.0f} | {d['I']:.0f} | {d['c']:.1f} | {d['Z']:.0f} |")
    z_full = min(sec["ext_medio"]["Z"], sec["ext_ranura_salida"]["Z"])
    I_full = sec["ext_medio"]["I"]
    z_half = min(sec["union_hembra"]["Z"], sec["union_macho"]["Z"])

    # 2. rail bending, two support cases
    r += ["", "## 2. Riel con 150 N en la cápsula", "",
          "Carga en el eje de la bisagra con el carro a ras de la punta (palanca máxima). La caída del eje bajo el riel no "
          "suma momento con carga vertical. El tramo se imprime acostado: la flexión va a lo largo de las capas (aplica 45).",
          "",
          "**Caso A, nodo colgado del asa:** voladizo desde la caja. Momento en la unión central/extensión (|x| = "
          f"{RAIL_CENTRAL_L / 2:g}) M = F·(x_carga − {RAIL_CENTRAL_L / 2:g}); en la sección llena σ = M/Z; en la media madera "
          "σ = M/Z_mitad. Flecha de la punta δ = F·L³/(3·E·I) con la sección llena (las uniones la aumentan).",
          "",
          "**Caso B, nodo apoyado en los ganchos:** voladizo más allá del gancho, M = F·(x_carga − D/2).", "",
          "| Aro | Ext. | Punta mm | x carga mm | A: M N·mm | A: σ llena MPa | A: σ media madera MPa | A: FS 45 / 22 (media madera) | A: flecha mm | B: M N·mm | B: σ MPa | B: FS 45 / 22 |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    rail_rows = {}
    for D in RING_DIAMETERS:
        n = RAIL_EXT_PER_RING[D]
        xl = load_x(n)
        La = xl - RAIL_CENTRAL_L / 2
        Ma = F * La
        sa, sh = Ma / z_full, Ma / z_half
        da = F * La ** 3 / (3 * PETG_E * I_full)
        Lb = xl - D / 2
        Mb = F * max(Lb, 0.0)
        sb = Mb / z_full
        rail_rows[D] = dict(n=n, tip=rail_tip(n), xl=xl, Ma=Ma, sa=sa, sh=sh, da=da, Mb=Mb, sb=sb, Lb=Lb)
        fa, fb = fs(sh), fs(sb)
        note = " (la carga queda dentro del aro)" if Lb < 0 else ""
        r.append(f"| Ø{D:g} | {n} | {rail_tip(n):.0f} | {xl:.1f} | {Ma:.0f} | {sa:.1f} | {sh:.1f} | {fa[0]:.1f} / {fa[1]:.1f} | "
                 f"{da:.1f} | {Mb:.0f}{note} | {sb:.1f} | {fb[0]:.1f} / {fb[1]:.1f} |")
    r += ["", "En Ø100 no hay posición válida del carro sobre el tramo central (C15, ver la Fase D); la fila usa la punta del "
          "tramo central igual, como referencia."]

    # 3. joint
    Mj = max(v["Ma"] for v in rail_rows.values())
    T = Mj / RAIL_LAP_Z
    d_b = M4_CLEAR - 0.2                                    # M4 shank, bearing diameter
    a_s = math.pi * 4.0 ** 2 / 4
    kw, kl, kh = RAIL_DOVETAIL_KEY
    r += ["", "## 3. Unión de tramos (media madera + llave en cola de milano + 2 M4 verticales)", "",
          f"Momento más cargado: caso A, M = {Mj:.0f} N·mm. Par de fuerzas con brazo igual a la media altura de la media madera "
          f"(z = {RAIL_LAP_Z:g}): la mitad de arriba se apoya en el hombro y abajo aparece una tracción T = M / {RAIL_LAP_Z:g} = "
          f"**{T:.0f} N** que tiende a separar las mitades a lo largo del riel. La toman los 2 M4 en corte simple y la llave "
          "en aplastamiento; se dan los dos por separado (ambos son conservadores porque comparten).", "",
          f"- M4 solos, corte: τ = T / (2·{a_s:.1f} mm²) = **{T / (2 * a_s):.0f} MPa** en el acero (A2-70: fluencia del orden de "
          "450 MPa, corte del orden de 0.6 de eso, dato de catálogo por confirmar).",
          f"- M4 solos, aplastamiento del PETG: σ = T / (2·d·h) con d = {d_b:.1f} y h = {RAIL_LAP_Z:g} (media altura) = "
          f"**{T / (2 * d_b * RAIL_LAP_Z):.1f} MPa** → FS {fs(T / (2 * d_b * RAIL_LAP_Z))[0]:.1f} (45, carga en el plano de las capas, "
          f"tramo acostado) / {fs(T / (2 * d_b * RAIL_LAP_Z))[1]:.1f} (22).",
          f"- Llave sola ({kw:g} × {kl:g} × {kh:g}), aplastamiento en su cara de {kw:g} × {kh:g}: σ = {T / (kw * kh):.1f} MPa → FS "
          f"{fs(T / (kw * kh))[0]:.1f} / {fs(T / (kw * kh))[1]:.1f}; corte en su base {kl:g} × {kw:g}: τ = {T / (kl * kw):.1f} MPa.",
          f"- Flexión en la media madera: σ = M / Z_mitad = {Mj / z_half:.1f} MPa → FS {fs(Mj / z_half)[0]:.1f} / {fs(Mj / z_half)[1]:.1f}."]

    # 3b. the joint and the rail-length decision are one decision (largo_riel.py)
    nd, lrows = LR.table()
    from params import M8_ROD
    r += ["", "### 3b. La unión depende del largo del riel (decisión pendiente, ver `FASE_D.md`)", "",
          "Mismo caso A con la punta del riel en cada configuración posible: la actual, la mínima que deja armar gancho + carro "
          f"(R + {nd['need0']:.0f}, que coincide con la tabla del equipo) y la regla automática con extensiones solapadas.", "",
          "| Aro | Configuración | Punta mm | M en la unión N·mm | σ media madera MPa | FS 45 / 22 |", "|---|---|---|---|---|---|"]
    worst = 0.0
    for lr in lrows:
        for name, t in (("actual", lr["solape"]["tip"]), ("mínima para armar", lr["need0"]),
                        (f"auto solapada (n = {lr['solape']['n_auto']})", lr["solape"]["tip_auto"])):
            M_ = F * (t + CP.carriage_axis()[0] - RAIL_CENTRAL_L / 2)
            worst = max(worst, M_)
            r.append(f"| Ø{lr['D']:g} | {name} | {t:.0f} | {M_:.0f} | {M_ / z_half:.1f} | {fs(M_ / z_half)[0]:.1f} / {fs(M_ / z_half)[1]:.1f} |")
    n_e = M8_ROD["E"] / PETG_E
    dc = M8_ROD["d_nucleo"]
    A_r, I_r = math.pi * dc ** 2 / 4, math.pi * dc ** 4 / 64
    zr = RAIL_SECTION / 2
    hm = sec["union_macho"]
    I_tr = hm["I"] + n_e * (I_r + A_r * (zr - hm["zc"]) ** 2)
    yb = max(hm["c"], 0.0)
    r += ["", f"Refuerzo opcional `riel.varilla_M8` (equipo) en el peor caso, M = {worst:.0f} N·mm, sección compuesta con la "
          f"media madera macho (n = E_acero/E_PETG = {n_e:.0f}, núcleo Ø{dc:g} en el centro del conducto, z = {zr:g}): I transformada "
          f"{I_tr:.0f} mm⁴ contra {hm['I']:.0f} sin varilla. PETG σ ≈ M·c/I = {worst * (yb + abs(zr - hm['zc'])) / I_tr:.1f} MPa; "
          f"acero σ ≈ n·M·y/I = {n_e * worst * (abs(zr - hm['zc']) + dc / 2) / I_tr:.0f} MPa. Sólo vale si la varilla pasa ajustada por "
          "la unión (agujeros o bujes) para que se curve junto con el riel; suelta en el conducto no ayuda. Estimación gruesa."]

    # 4. box-floor M4 inserts (rail moment into the box)
    xs = sorted({abs(x) for x, _ in BASE_M4_PTS})
    arm = 2 * xs[0]
    r += ["", "## 4. Insertos M4 del fondo de la caja (caso A)", "",
          f"El momento del riel entra a la caja por los 4 M4 de la brida de la cámara en (±{xs[0]:g}, ±{abs(BASE_M4_PTS[0][1]):g}). "
          f"Pivote en la línea de tornillos del lado opuesto (conservador): T_par = F·(x_carga + {xs[0]:g}) / {arm:g}, la mitad por inserto.", "",
          "| Aro | x carga mm | Tracción por inserto N |", "|---|---|---|"]
    ins = {}
    for D, v in rail_rows.items():
        t_ins = F * (v["xl"] + xs[0]) / arm / 2
        ins[D] = t_ins
        r.append(f"| Ø{D:g} | {v['xl']:.1f} | **{t_ins:.0f}** |")
    r += ["", f"**Exigencia:** cada inserto térmico M4 del fondo debe aguantar al menos {max(ins.values()):.0f} N de arranque "
          "en PETG (más el factor de seguridad que el equipo quiera). No hay dato de capacidad del inserto: hay que probarlo "
          "o tomarlo del fabricante."]

    # 5. hook
    L = G.hook_layout()
    d = L["d"]
    web_w = HOOK_CONTACT_W                     # web (alma) and jaw are as wide as the 12 mm seat
    e = web_w / 2                              # rod centre at x = 0, web from x = -web_w to 0
    A_w = web_w * web_w
    fl_l, fl_t = HOOK_FLANGE
    x_bolt, x_end = L["xk"], L["fx0"]
    lever_load = abs(x_bolt - (-e))
    lever_tip = abs(x_end - x_bolt)
    Rc = HOOK_LOAD_N * lever_load / lever_tip
    Mfl = HOOK_LOAD_N * lever_load
    Zfl = (RAIL_SECTION - M4_CLEAR) * fl_t ** 2 / 6
    s_web = HOOK_LOAD_N / A_w + HOOK_LOAD_N * e * 6 / (12.0 * web_w ** 2)
    nut_lip = (M4_NUT[0] - RAIL_TSLOT["abertura"]) / 2
    s_lip = (HOOK_LOAD_N + Rc) / (2 * nut_lip * M4_NUT[0])
    r += ["", "## 5. Gancho con 75 N", "",
          f"Varilla en x = 0; alma de {web_w:g} × 12 de x = −{web_w:g} a 0 (excentricidad e = {e:g}); M4 de la perilla en x = "
          f"{x_bolt:.1f}; extremo de la brida en x = {x_end:.1f}. La brida sólo puede empujar contra el fondo del riel, así que "
          "el apoyo está en el extremo del lado de la perilla y el perno toma la suma.", "",
          f"- Alma: σ = F/A + F·e/Z = {HOOK_LOAD_N:g}/{A_w:g} + {HOOK_LOAD_N:g}·{e:g}/{12.0 * web_w ** 2 / 6:.0f} = **{s_web:.1f} MPa** → "
          f"FS {fs(s_web)[0]:.1f} (45: el gancho se imprime de costado y la carga va en el plano de las capas).",
          f"- Reacción en el extremo de la brida R = F·{lever_load:.1f}/{lever_tip:.1f} = {Rc:.0f} N; perno M4 = F + R = "
          f"**{HOOK_LOAD_N + Rc:.0f} N**.",
          f"- Brida en el perno: M = {Mfl:.0f} N·mm, Z = ({RAIL_SECTION:g} − {M4_CLEAR:g})·{fl_t:g}²/6 = {Zfl:.0f} mm³, σ = **{Mfl / Zfl:.1f} MPa** → "
          f"FS {fs(Mfl / Zfl)[0]:.1f} / {fs(Mfl / Zfl)[1]:.1f}.",
          f"- Tuerca M4 contra los labios de la ranura T (apoyo de {nut_lip:.1f} por lado × {M4_NUT[0]:g}): σ = {s_lip:.1f} MPa → "
          f"FS {fs(s_lip)[0]:.1f} / {fs(s_lip)[1]:.1f} (tramo acostado: el labio trabaja en el plano de las capas, aplica 45).",
          f"- Asiento recto: flecha de la curva del aro sobre {HOOK_CONTACT_W:g} de contacto, f = c²/(8R): " +
          ", ".join(f"Ø{D:g} {HOOK_CONTACT_W ** 2 / (8 * D / 2):.2f} mm" for D in RING_DIAMETERS) +
          ". El prompt pedía este cálculo: el asiento recto sirve."]

    # 6. handle, lid screws
    pts = C.screw_pts(lay)
    bar_t = 10.0
    M_h = F * HANDLE_GRIP / 4
    s_h = M_h / (12.0 * bar_t ** 2 / 6)
    r += ["", "## 6. Asa y tapa con 150 N de izado", "",
          f"- Barra del asa como viga simplemente apoyada de {HANDLE_GRIP:g} (conservador), sección 12 × {bar_t:g}: M = F·L/4 = "
          f"{M_h:.0f} N·mm, σ = **{s_h:.1f} MPa** → FS {fs(s_h)[0]:.1f} (la tapa se imprime con el asa arriba: la barra flexa en el "
          "plano de las capas).",
          f"- Patas del asa: tracción a través de las capas, F/2 sobre 12 × 12: {F / 2 / 144:.2f} MPa → FS {fs(F / 2 / 144)[1]:.0f} (22).",
          f"- {len(pts)} tornillos M3 con inserto en la brida: si sólo los tornillos llevan el izado, **{F / len(pts):.1f} N por inserto**, "
          "más la reacción de la junta tórica comprimida (sin dato: depende de la dureza del cordón)."]

    # 7. hinge
    m_cap = CAPSULE_SET_G + CAPSULE_CONTENT_G
    _, out_h, _, _, _, x0, x_front = CP.cap_dims()
    x_cg = (x0 + x_front) / 2
    T_w = m_cap * G0 * x_cg
    r_m = (HINGE_TEETH_RIN + HINGE_DISC_D / 2) / 2
    half_pitch = math.pi * r_m / HINGE_TEETH
    alpha = math.degrees(math.atan(HINGE_TOOTH_H / half_pitch))
    mu = 0.3
    phi = math.degrees(math.atan(mu))
    k = 2 * r_m * math.tan(math.radians(alpha + phi))
    T_150 = F * (x_front - 0.0)
    tongue = HINGE_GAP - 2 * HINGE_TOOTH_H
    r += ["", "## 7. Bisagra dentada", "",
          f"- Peso de la cápsula con contenido en aire: {m_cap:.0f} g, centro a {x_cg:.0f} del eje → par T = {T_w:.0f} N·mm (en el agua "
          "casi neutra: desplaza 128 cm³).",
          f"- Dientes: {HINGE_TEETH}, alto {HINGE_TOOTH_H:g}, radio medio {r_m:.1f}, semipaso {half_pitch:.2f} → flanco α = {alpha:.1f}°. "
          f"Par para saltar un diente con precarga axial N, dos caras: T = 2·N·r_m·tan(α + φ), con μ = {mu:g} (estimado, φ = {phi:.1f}°): "
          f"T = {k:.1f}·N.",
          f"- Contra el peso propio: N ≥ {T_w / k:.1f} N. Contra 150 N en el frente (palanca {x_front:.0f}): N ≥ **{T_150 / k:.0f} N**, "
          f"que un M4 da con un par de apriete de unos {0.2 * 4 * T_150 / k / 1000:.2f} N·m (T = 0.2·d·N, coeficiente típico).",
          f"- Aplastamiento del M4 con 150 N: en las orejas 2 × 4 × {HINGE_EAR_T:g} → {F / (2 * 4 * HINGE_EAR_T):.1f} MPa; en la lengua "
          f"4 × {tongue:.1f} → {F / (4 * tongue):.1f} MPa. FS > {fs(F / (4 * tongue))[1]:.0f} aun entre capas."]

    # 8. pressure, Roark
    q = DESIGN_PRESSURE
    Lc, Wc, Hc = lay.cav

    def coef(rt):
        for (r0, b0, a0), (r1, b1, a1) in zip(ROARK, ROARK[1:]):
            if r0 <= rt <= r1:
                f_ = (rt - r0) / (r1 - r0)
                return b0 + f_ * (b1 - b0), a0 + f_ * (a1 - a0)
        return ROARK[0][1], ROARK[0][2]

    panels = [("Tapa de la caja (campo de 5; bajo la ranura quedan 3.5)", Lc, Wc, BOX_LID_T),
              ("Fondo de la caja", Lc, Wc, BOX_FLOOR), ("Pared larga", Lc, Hc, BOX_WALL), ("Pared corta", Wc, Hc, BOX_WALL),
              ("Pared de la cápsula", 38.0, 38.0, CAP_WALL)]
    r += ["", f"## 8. Presión a 1 m ({q:.4f} MPa), placas de Roark", "",
          "σ = β·q·b²/t², y = α·q·b⁴/(E·t³) (Roark, 7.ª ed., tabla 11.4 caso 1a, bordes simplemente apoyados; coeficientes "
          "copiados de `cad/build.py`). La presión empuja hacia adentro: la tapa se apoya en la brida y la junta; los tornillos no "
          "la cargan.", "", "| Placa | a × b mm | t mm | β | σ MPa | FS 45 / 22 | flecha mm |", "|---|---|---|---|---|---|---|"]
    for name, a_, b_, t_ in panels:
        a_, b_ = max(a_, b_), min(a_, b_)
        beta, alpha_ = coef(a_ / b_)
        sig = beta * q * b_ ** 2 / t_ ** 2
        y = alpha_ * q * b_ ** 4 / (PETG_E * t_ ** 3)
        r.append(f"| {name} | {a_:.0f} × {b_:.0f} | {t_:g} | {beta:.3f} | {sig:.2f} | {fs(sig)[0]:.0f} / {fs(sig)[1]:.0f} | {y:.3f} |")
    a_w = LENS_APERTURE / 2
    nu_a = 0.37
    s_w = 3 * (3 + nu_a) * q * a_w ** 2 / (8 * WIN_T ** 2)
    r += ["", f"Ventana de acrílico, placa circular simplemente apoyada en el hombro (radio libre {a_w:g}, t {WIN_T:g}, ν {nu_a:g} "
          f"típico): σ = 3(3+ν)·q·a²/(8t²) = **{s_w:.2f} MPa**, frente a un acrílico típico de decenas de MPa (dato de material "
          "estimado, no medido)."]

    # 9. buoyancy and stability (fase_a numbers; capsules at their real height)
    r += ["", "## 9. Flotabilidad y estabilidad", "",
          "Los números de flotabilidad son los de `fase_a.py`. En esta fase se corrigió su cálculo de estabilidad: el acero de "
          "las pletinas no sumaba a la masa total y las cápsulas iban a la altura del riel (ahora van con el eje bajo el riel, a 0 y a 90°)."]
    an = FA.analyse_box(lay)
    f0 = FA.P.INFILL_CASES[0]
    res = FA.balance(an, f0)
    lo, hi = FA.P.BALLAST_TARGET_KGF
    r += ["", f"Exigencias: peso aparente de +{lo:g} a +{hi:g} kgf, total en aire ≤ 3 kg.", "",
          "| Relleno bandeja | Aro | Nodo sin acero g | Desplaza cm³ | Aparente sin acero g | Pletinas por lado | Aparente final g | En ventana | Total en aire g | ≤ 3 kg |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for fi in FA.P.INFILL_CASES:
        rr = res if fi == f0 else FA.balance(an, fi)
        for row in rr["rows"]:
            r.append(f"| {fi * 100:.0f} % | Ø{row['D']:g} | {row['node_g']:.0f} | {row['disp']:.0f} | {row['app0']:+.0f} | {row['layers']} | "
                     f"**{row['app']:+.0f}** | {'sí' if row['in_window'] else 'NO'} | {row['total']:.0f} | {'sí' if row['total'] <= 3000 else 'NO'} |")
    r += ["", "Totalmente sumergido no hay plano de flotación ni metacentro: el par adrizante al inclinarse un ángulo θ es "
          "B·BG·sen θ, con B el empuje y BG la distancia vertical del centro de masa (G) bajo el centro de empuje (B). BG > 0 "
          "quiere decir que no se voltea; el número que importa es BG. Las placas de acero ya están en G y en B.", "",
          "| Aro | Inclinación de las cápsulas | z G mm | z B mm | BG mm | B N | Par adrizante a 10° N·mm |",
          "|---|---|---|---|---|---|---|"]
    for row in res["rows"]:
        V = row["disp"] + row["steel_g"] / FA.P.STEEL_DENSITY
        Bn = V * FA.P.SEAWATER_DENSITY * G0
        for tilt in (0.0, 90.0):
            zg, zb = FA.stability(an, res, row["D"], tilt)
            bg = zb - zg
            r.append(f"| Ø{row['D']:g} | {tilt:.0f}° | {zg:.1f} | {zb:.1f} | **{bg:.1f}** | {Bn:.1f} | "
                     f"{Bn * bg * math.sin(math.radians(10)):.0f} |")
    r += ["", "Las cápsulas son casi neutras (128 g contra 128 cm³), así que bajarlas mueve G y B casi igual. El margen lo dan "
          "las pletinas bajo el riel contra el aire de la caja arriba."]

    (HERE / "reporte_verificacion.md").write_text("\n".join(r) + "\n", encoding="utf-8")
    print("written reporte_verificacion.md")
    for k_, v in sec.items():
        print(k_, {a: round(b, 1) for a, b in v.items()})
    for D, v in rail_rows.items():
        print(D, {a: round(b, 1) for a, b in v.items()})


if __name__ == "__main__":
    main()
