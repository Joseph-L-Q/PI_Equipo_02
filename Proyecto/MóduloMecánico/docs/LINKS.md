# Links de LanternGuard CAD

## Repo
- Rama: https://github.com/Joseph-L-Q/PI_Equipo_02/tree/cad/version-final
- PR #10 (cad/version-final → main): https://github.com/Joseph-L-Q/PI_Equipo_02/pull/10
- Carpeta del módulo: https://github.com/Joseph-L-Q/PI_Equipo_02/tree/cad/version-final/Proyecto/M%C3%B3duloMec%C3%A1nico

## Drive
- LanternGuard_CAD: https://drive.google.com/drive/folders/1T8cv6NW7W2cESde3SLp9HgS4VRJMWwCO
  (`07_Documentos` tiene ESTADO.md, el documento para el equipo y los planos)

## Onshape: carpeta "LanternGuard"
Todos los documentos `LG_*` ya están dentro de la carpeta "LanternGuard" y tienen su descripción de una línea. Se movieron
por API con `updateDocumentAttributes` (`POST /documents/{did}` con `parentId`); el código está en
`cad_final/onshape_push.py`, función `organize`. Los ids quedan en `cad_final/onshape_docs.json`; se sube una carpeta
con `python cad_final/onshape_push.py --carpeta <carpeta> --documento <nombre> --ensamble <ensamble.step>`.

| Documento | Qué es | Link |
|---|---|---|
| LG_00_LEER_PRIMERO | Resumen: qué es cada documento, cuál se recomienda, qué se imprime primero | (se crea al cerrar la entrega) |
| LG_probetas | Probetas de calibración (PB6, PB7, PB8 y las del riel modular) | https://cad.onshape.com/documents/dfcea0e1fd7d960062f6631e/w/7030967448e32d98d4462131 |
| LG_P0_original | Referencia: simple V1 y la modular (ENSAMBLE_modular) | https://cad.onshape.com/documents/95702b685c4703a1812f1cd5/w/22e05e9a953df1fd6ec5ee2a |
| LG_P1_minimo | Riel en celosía, gancho snap, caja mínima (descartado) | https://cad.onshape.com/documents/78580e61be69350e3e1577c4/w/e8effc28aa305039dd6d79cb |
| **LG_P2_robusto** | **Recomendado para la piscina** | https://cad.onshape.com/documents/999b4e78fb31ffdeaf864392/w/5004d17b81ec1ab1c916dc78 |
| LG_P3_monocasco | Caja y riel en una pieza (base de P4) | https://cad.onshape.com/documents/a3f5a3445acf709539d118a1/w/6bec4bfed0a0cd181c80b6d6 |
| **LG_P4_estetico** | **Recomendado para presentar** | https://cad.onshape.com/documents/d8e4b0f024f7efcb8f94ed99/w/fabae97231abb068b21c50e6 |
| LG_boya_PET | Boya, primera vuelta: 2 botellas de 1 L (descartada para pruebas) | https://cad.onshape.com/documents/9bef1aea8cb725d8b9ef74ea/w/e0a2bb379713e51552ccdaf9 |
| **LG_boya_PET_v2** | **Boya, segunda vuelta: 4 botellas de 1 L en cruz (recomendada)**. ENSAMBLE con 19 partes, REF_ en electrónica y botellas | https://cad.onshape.com/documents/f4e8ac814316f253d53d94e0/w/a972a01f232336138e011bc2 |
| LG_sistema | Sistema completo con la boya plataforma vieja (referencia) | https://cad.onshape.com/documents/add9a482719cd49ae97ca226/w/bc4e69d2a95cf63d59e5dc97 |

Documentos viejos, que **no se tocaron** y que Yoichi mueve a `LanternGuard/_historico`:
- LanternGuard CAD final: https://cad.onshape.com/documents/cf6f0f08630e1b23677101ac/w/53ecc7142a15110b1fe8e8d1
- LanternGuard - Módulo mecánico

## Pestañas ENSAMBLE_v2 (correcciones 3 y 4)
Se sube con `python cad_final/onshape_push.py --ensamble-v2 <documento> --ensamble <STEP> [--pestana X]`: nombres REF_ en lo que no se
imprime, Part Studio aplanado y comparación de partes de Onshape contra sólidos del STEP (`--verificar <documento>` solo compara).

| Documento | Pestaña | Partes = sólidos | Link |
|---|---|---|---|
| LG_P0_original | ENSAMBLE_v2 (simple V1) | 53 = 53 | https://cad.onshape.com/documents/95702b685c4703a1812f1cd5/w/22e05e9a953df1fd6ec5ee2a/e/c04751805d4a14c6339f0ba7 |
| LG_P0_original | ENSAMBLE_modular_v2 | 47 = 47 | https://cad.onshape.com/documents/95702b685c4703a1812f1cd5/w/22e05e9a953df1fd6ec5ee2a/e/8eba078f08454031fe9c9db5 |
| LG_boya_PET_v2 | ENSAMBLE | 19 = 19 | https://cad.onshape.com/documents/f4e8ac814316f253d53d94e0/w/a972a01f232336138e011bc2/e/a7bc64699813d459a97704d7 |

## Pasos a mano en Onshape (la API pública no los permite)
- **Orden de pestañas:** no hay llamada para reordenarlas. En LG_P0_original, LG_P1 a LG_P4 y LG_boya_PET hay que
  arrastrar la pestaña ENSAMBLE al primer lugar. Los documentos que se crean desde ahora ya suben el ENSAMBLE primero,
  así que queda primero solo.
- Mover los 2 documentos viejos a `LanternGuard/_historico`.
