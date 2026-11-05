"""Capacity of the buoy and the node against sea loads (05/11): reads docs/resultados/resultados.json (FS between layers of each case),
computes "aguanta hasta" (load at which the between-layer stress reaches 22 MPa, linear) and the safe load (that / 3), and converts them into
sea conditions with the drag law F = 0.5 * rho * Cd * A * v^2 and deep-water linear waves (water particle velocity at the surface v = pi * H / T).

    python capacidad_mar.py       (from cad_final/)  ->  salida/capacidad_mar.json, salida/capacidad_mar.md
"""
import json
import math
from pathlib import Path

import params as P
import boya_pet as BP

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
RHO = P.SEAWATER_DENSITY * 1000.0  # kg/m3 (params gives g/cm3: 1.025 -> 1025)
FS_OBJ = 3.0
CD_BLUFF = 1.2                    # flat plate / box normal to the flow (bluff body, Hoerner: 1.1 to 1.3)
CD_NODE = 1.0                     # capsule front used by the FEM cases (simscale_run.case_a)
T_WAVE = (4.0, 6.0)               # s, short sea / swell


def drag_v(F, cd, a_m2):
    return math.sqrt(2.0 * F / (RHO * cd * a_m2))


def waves(v):
    return {f"H_T{int(t)}s_m": round(v * t / math.pi, 2) for t in T_WAVE}


def main():
    R = json.loads((MOD / "docs" / "resultados" / "resultados.json").read_text(encoding="utf-8"))
    d = BP.dims(P.FLOT_BOTTLE, P.FLOT_COUNT)
    out = []

    def fs_of(keys):
        e = [R[k] for k in keys if k in R]
        w = min(e, key=lambda x: x["fs_capas"])
        return w["fs_capas"], w["pieza"]

    # ---- 1. lateral hit on the panel (the structure above the deck is the sail)
    fs, pz = fs_of(["B2_cubierta_lisa_lateral", "B2_cubierta_mastil_lateral"])
    L = 200.0
    up = L * fs
    sf = up / FS_OBJ
    pl, pw, pt = P.BUOY_PANEL
    z_col = d["z_panel0"] - d["z_bar"]
    a_cm2 = (pl * pt                                                        # panel edge on
             + d["Lx"] * (d["HB"] + P.PET_LID_T)                             # box + lid side
             + 2 * P.PET_COLUMN_D * z_col                                    # 2 columns in line seen from the side
             + P.PET_MAST[0] * (d["z_mast"] - d["z_bar"])) / 100.0
    A = a_cm2 * 1e-4
    out.append(dict(caso="golpe lateral sobre el panel (B2, cada mitad con los 200 N enteros)", pieza=pz, carga_N=L, fs_capas=fs, aguanta_hasta_N=round(up),
                    segura_N=round(sf), area_proyectada_m2=round(A, 4), Cd=CD_BLUFF,
                    equivalente=dict(velocidad_agua_aguanta_m_s=round(drag_v(up, CD_BLUFF, A), 1), velocidad_agua_segura_m_s=round(drag_v(sf, CD_BLUFF, A), 1),
                                     **{k + "_segura": v for k, v in waves(drag_v(sf, CD_BLUFF, A)).items()}),
                    justificacion_mar=(f"Area de lo que queda sobre el agua visto de lado (caja y tapa {d['Lx']:.0f} x {d['HB'] + P.PET_LID_T:.0f} mm, 2 columnas, mastil, canto del panel) = "
                                       f"{a_cm2:.0f} cm2, Cd {CD_BLUFF}; velocidad del agua que la empuja con la carga segura; ola de aguas profundas, v = pi*H/T. "
                                       "Cada mitad se calcula con los 200 N enteros (en la boya completa se reparten entre las dos), asi que es conservador.")))

    # ---- 2. vertical wave on the deck
    fs, pz = fs_of(["B2_cubierta_lisa", "B2_cubierta_mastil"])
    L = 200.0
    up = L * fs
    sf = up / FS_OBJ
    xw, xt, _xy, _xe = P.PET_XBAR
    a_deck = (xw * d["WH"] * 2 + P.PET_BAR_W * d["WH"] + 2 * P.PET_BAR_W * d["LH"] / 2) * 1e-6      # one half: screw-line bars (2), seam bar, 2 long bars
    out.append(dict(caso="golpe de ola vertical sobre las barras de la cubierta (B2, cada mitad con los 200 N enteros)", pieza=pz, carga_N=L, fs_capas=fs,
                    aguanta_hasta_N=round(up), segura_N=round(sf), area_proyectada_m2=round(a_deck, 4), Cd=1.0,
                    equivalente=dict(velocidad_agua_aguanta_m_s=round(drag_v(up, 1.0, a_deck), 1), velocidad_agua_segura_m_s=round(drag_v(sf, 1.0, a_deck), 1),
                                     **{k + "_segura": v for k, v in waves(drag_v(sf, 1.0, a_deck)).items()}),
                    justificacion_mar=(f"Area en planta de las barras de una media cubierta = {a_deck * 1e4:.0f} cm2 (el resto es hueco), Cd 1.0, agua que cae a v sobre las barras; "
                                       "v = pi*H/T de una ola de aguas profundas.")))

    # ---- 3. mooring line
    fs, pz = fs_of(["B1_casco_cabo"])
    L = 300.0                                                   # total pull; the FEM case loads each hull half with L / (2 cos 30) = 173 N (the 2 legs share it)
    up = L * fs
    sf = up / FS_OBJ
    import capsula as CP
    cd_ = CP.cap_dims()
    a_cap = math.pi * (cd_[1] / 2) ** 2 * 1e-6
    out.append(dict(caso="tiron del cabo de amarre repartido en la pata de gallo (B1, 2 ramales a 60 grados, 173 N cada uno con 300 N de tiron)", pieza=pz, carga_N=L, fs_capas=fs, aguanta_hasta_N=round(up), segura_N=round(sf),
                    area_proyectada_m2=round(a_cap, 4), Cd=CD_NODE,
                    equivalente=dict(velocidad_agua_aguanta_m_s=round(drag_v(up, CD_NODE, a_cap), 1), velocidad_agua_segura_m_s=round(drag_v(sf, CD_NODE, a_cap), 1)),
                    justificacion_mar=(f"El cabo tira de la boya con el arrastre de la linterna (frente de la capsula {a_cap * 1e4:.0f} cm2, Cd {CD_NODE}) mas su propio peso en el agua; "
                                       "se compara solo con el arrastre de la capsula (el cabo, la manguera y el cuerpo de la linterna suman mas, por eso el valor es optimista en velocidad). "
                                       "El tiron de olas no se incluye: depende de la longitud del cabo. La carga es el tiron TOTAL de la pata de gallo (cada ramal lleva 300 / (2 cos 30) = 173 N); si un ramal se rompe, el otro lleva todo y el resultado baja a la mitad o menos.")))

    # ---- 4. node: hook + current
    fs, pz = fs_of(["M3s_riel_gancho", "M5s_capsula_tapa_pie", "M1s_caja_cuerpo"])
    q = 0.5 * RHO * 1.5 ** 2
    drag15 = q * a_cap * CD_NODE
    L = math.hypot(150.0, drag15)
    up = L * fs
    sf = up / FS_OBJ
    out.append(dict(caso="nodo colgado del gancho: 150 N hacia abajo y corriente de 1.5 m/s (M3s, M5s, M1s)", pieza=pz, carga_N=round(L, 1), fs_capas=fs, aguanta_hasta_N=round(up),
                    segura_N=round(sf), area_proyectada_m2=round(a_cap, 4), Cd=CD_NODE,
                    equivalente=dict(arrastre_a_1_5_m_s_N=round(drag15, 1), velocidad_agua_si_toda_la_carga_segura_fuera_corriente_m_s=round(drag_v(sf, CD_NODE, a_cap), 1)),
                    justificacion_mar=(f"La carga del caso es casi toda peso del nodo (150 N); el arrastre de una corriente de 1.5 m/s sobre la capsula ({a_cap * 1e4:.0f} cm2, Cd {CD_NODE}) es solo {drag15:.1f} N. "
                                       "La corriente no es el limite: el limite es cuanto peso cuelga del gancho.")))
    (MOD / "salida").mkdir(exist_ok=True)
    (MOD / "salida" / "capacidad_mar.json").write_text(json.dumps(dict(
        supuestos=dict(rho_agua_kg_m3=RHO, Cd_cuerpo_romo=CD_BLUFF, Cd_capsula=CD_NODE, olas="aguas profundas, teoria lineal, velocidad de la particula en la superficie v = pi*H/T",
                       periodos_s=list(T_WAVE), fs_objetivo=FS_OBJ, material="PETG, entre capas 22 MPa", lineal="el esfuerzo es proporcional a la carga"), casos=out),
        indent=1, ensure_ascii=False), encoding="utf-8")
    md = ["# Que aguanta la boya y el nodo en el mar", "",
          "Cada parrafo dice hasta que fuerza llega la pieza antes de que sus capas se despeguen y cual es la fuerza segura (un tercio de esa). "
          "Despues lo traduce a agua que empuja. Es una estimacion con formulas simples, no una promesa: el mar real tiene golpes mas bruscos. "
          "Ojo con las alturas de ola: una ola de 4 s no puede pasar de unos 3 m sin romperse, asi que cuando sale una altura mayor solo quiere decir que el limite no lo pone el mar normal sino un golpe directo (olas rompiendo, un choque). "
          "El cabo de amarre solo lo aguanta con la pata de gallo de dos ramales: si un ramal se rompe, el otro lleva todo y la pieza queda en la mitad de margen o menos.", ""]
    for c in out:
        e = c["equivalente"]
        md += ["## " + c["caso"][0].upper() + c["caso"][1:], ""]
        txt = (f"La carga del caso es {c['carga_N']:.0f} N y las capas aguantan {c['fs_capas']:.1f} veces eso: la pieza llega hasta unos {c['aguanta_hasta_N']} N "
               f"y lo seguro es no pasar de {c['segura_N']} N. ")
        if "velocidad_agua_segura_m_s" in e:
            txt += f"Eso equivale a agua empujando a {e['velocidad_agua_segura_m_s']} m/s (la pieza llegaria al limite con {e['velocidad_agua_aguanta_m_s']} m/s)"
            if "H_T4s_m_segura" in e:
                txt += (f"; en olas seria una ola de unos {e['H_T4s_m_segura']} m con 4 s entre crestas o de unos {e['H_T6s_m_segura']} m con 6 s")
            txt += ". "
        else:
            txt += f"Una corriente de 1.5 m/s solo empuja {e['arrastre_a_1_5_m_s_N']} N: no es el limite, lo es el peso que cuelga. "
        txt += c["justificacion_mar"]
        md += [txt, ""]
    (MOD / "salida" / "capacidad_mar.md").write_text(chr(10).join(md), encoding="utf-8")
    print(json.dumps(out, indent=1, ensure_ascii=False)[:3000])


if __name__ == "__main__":
    main()
