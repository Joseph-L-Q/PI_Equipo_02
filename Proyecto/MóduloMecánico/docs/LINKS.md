# Links de LanternGuard CAD

## Repo
- Rama: https://github.com/Joseph-L-Q/PI_Equipo_02/tree/cad/version-final
- PR #10 (cad/version-final → main): https://github.com/Joseph-L-Q/PI_Equipo_02/pull/10
- Carpeta del módulo: https://github.com/Joseph-L-Q/PI_Equipo_02/tree/cad/version-final/Proyecto/M%C3%B3duloMec%C3%A1nico

## Drive
- LanternGuard_CAD: https://drive.google.com/drive/folders/1T8cv6NW7W2cESde3SLp9HgS4VRJMWwCO
  (`07_Documentos` tiene ESTADO.md y el documento para el equipo)

## Onshape
La API pública de Onshape no tiene un endpoint para crear carpetas, así que los documentos nuevos quedan en la raíz de
la cuenta. Para ordenarlos: en Onshape, *Create > Folder* "LanternGuard" y arrastrar los documentos `LG_*` adentro.
Los ids quedan en `cad_final/onshape_docs.json`; se suben con
`python cad_final/onshape_push.py --carpeta <carpeta> --documento <nombre>`.

| Documento | Qué tiene | Link |
|---|---|---|
| LanternGuard CAD final (el de antes) | Pestañas simple_D200_V1/V2/V3, LR1, nodo_simple_V2, boya_simple_V1, boya_referencia_V1, sistema_simple_V1 y la modular vieja | https://cad.onshape.com/documents/cf6f0f08630e1b23677101ac/w/53ecc7142a15110b1fe8e8d1 |
| LG_probetas | Las 15 probetas (STL, una pestaña por probeta) | https://cad.onshape.com/documents/dfcea0e1fd7d960062f6631e/w/7030967448e32d98d4462131 |
| LG_P0_original | P0 simple V1: una pestaña por pieza + ENSAMBLE; la modular como ENSAMBLE_modular | https://cad.onshape.com/documents/95702b685c4703a1812f1cd5/w/22e05e9a953df1fd6ec5ee2a |
