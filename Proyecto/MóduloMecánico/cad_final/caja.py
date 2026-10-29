# Dimensionado de la caja central por layout (mm). Todo 'est' = estimado, medir.
DUP=15   # alto de conectores dupont sobre los pines + curva del cable
LAT=10   # holgura lateral para que salgan cables de un modulo
GL=20    # zona de contratuerca PG7 por dentro (AF15 + llave/dedos)
W=4      # pared PETG a 1 m (0.01 MPa) -> 4 mm sobra
mods = {  # L, A, alto con pines
 "ESP32-S3 DevKitC-1 N16R8": (69,26,15),
 "KIT A (adaptador)":        (80,70,12),
 "XY-017 RS-485":            (45,15,12),
 "HW-517 x2":                (34,2*17+5,12),
 "microSD SPI":              (42,24,12),
 "MPU-6050 GY-521":          (21,16,4),
}
def caja(cav_L,cav_A,cav_H,name):
    out=(cav_L+2*W, cav_A+2*W, cav_H+W+W)
    aire=cav_L*cav_A*cav_H/1000
    print(f"{name}: cavidad {cav_L}x{cav_A}x{cav_H}  exterior {out[0]}x{out[1]}x{out[2]}  aire {aire:.0f} cm3 -> empuje {aire*1.025:.0f} g")
# A: KIT A en el piso (con la DevKit encima), modulos en una 2a bandeja sobre separadores
L=80+2*LAT+GL; A=70+2*LAT; H=5+12+15+DUP+ 5+12+DUP   # piso: standoff+kitA+devkit+dupont ; bandeja 5 + modulo + dupont
caja(L,A,H,"A  KIT A + bandeja arriba")
# A': KIT A + modulos al costado (un solo piso)
caja(80+2*LAT+GL, 70+45+3*LAT, 5+12+15+DUP, "A' KIT A + modulos al lado")
# B: sin KIT A: DevKit en placa perforada 70x50 con borneras; modulos alrededor
caja(70+45+3*LAT+GL//2, 50+26+3*LAT, 5+15+DUP+3, "B  DevKit en perfboard (sin KIT A)")
