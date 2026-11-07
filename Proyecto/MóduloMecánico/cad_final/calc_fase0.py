import math
# geometry from params.py (current)
BOX_L=132+10; ARM_PAD_T=10; ARM_LEN=190; FORK=52; ARM_H=25; ARM_W=30; t=3
x_root=BOX_L/2+ARM_PAD_T; pivot=x_root+ARM_LEN+FORK-ARM_H/2
print("raiz brazo x=",x_root,"pivote x=",pivot)
ring_x=250; print("apoyo en aro x=",ring_x," voladizo apoyo->pivote",pivot-ring_x)
# section arm
I=(ARM_W*ARM_H**3-(ARM_W-2*t)*(ARM_H-2*t)**3)/12; W=I/(ARM_H/2)
print(f"I={I:.0f} mm4 W={W:.0f} mm3")
sy=45; 
for name,F,L in [("150N en punta (agarran por la cápsula), desde raíz",150,pivot-x_root+20),
                 ("150N en punta, desde el apoyo del aro",150,pivot-ring_x+20)]:
    M=F*L; s=M/W; print(f"{name}: M={M/1000:.1f} N·m  sigma={s:.1f} MPa  FS(macizo45)={sy/s:.1f}  FS(entre capas 0.5)={0.5*sy/s:.1f}")
# drag 0.5 m/s on capsule face 0.05x0.06
F=0.5*1025*1.2*0.05*0.06*0.5**2; print("arrastre 0.5 m/s por cápsula N=",round(F,2))
# pressure 1 m
p=1025*9.81*1/1e6; print("p 1 m MPa=",round(p,4),"  vs 15 m 0.151 -> factor",round(0.151/p,1))
# roark lid box 132x66 t6 at 1 m
b=66;tt=6;s=0.61*p*b*b/tt**2; print("tapa caja sigma 1 m MPa=",round(s,2))
# hinge friction: M4 clamp; capsule moment in air: mass ~ 130 g at 40 mm
print("momento cápsula en aire N·mm=",round(0.13*9.81*40,1))
# cable path far camera: ESP32 at -X end of box (current layout) -> right camera
cam_x=pivot+16+5+20
for esp_x in (-BOX_L/2+30, 0):
    path=(cam_x-esp_x)+25+30   # +bajadas/curvas + holgura
    print(f"ESP32 en x={esp_x:.0f}: recorrido cámara lejana ≈ {path:.0f} mm vs 300 incluido")
