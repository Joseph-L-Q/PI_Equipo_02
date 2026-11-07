#!/usr/bin/env bash
# Prepara el CAD del nodo LanternGuard en macOS (o Linux) y prueba que regenera.
#   bash setup_mac.sh
# Crea .venv/ junto a este archivo, instala requirements.txt y corre: python cad_final/build.py --rapido
set -euo pipefail
cd "$(dirname "$0")"
t0=$(date +%s)

PY=""
for c in python3.12 python3 python; do
  if command -v "$c" >/dev/null 2>&1 && [ "$("$c" -c 'import sys; print("%d.%d" % sys.version_info[:2])')" = "3.12" ]; then
    PY="$c"; break
  fi
done
if [ -z "$PY" ]; then
  echo "No encontre Python 3.12."
  echo "Instalalo con:  brew install python@3.12"
  echo "o desde https://www.python.org/downloads/release/python-31210/"
  exit 1
fi
echo "Python 3.12 encontrado: $PY"

[ -x .venv/bin/python ] || { echo "Creando .venv ..."; "$PY" -m venv .venv; }
echo "Instalando dependencias (la primera vez tarda varios minutos) ..."
.venv/bin/python -m pip install --upgrade pip --quiet
.venv/bin/python -m pip install -r requirements.txt --quiet

echo "Regenerando (build --rapido) ..."
if .venv/bin/python cad_final/build.py --rapido; then
  echo "LISTO en $(( ($(date +%s) - t0) / 60 )) min. Para regenerar despues:  .venv/bin/python cad_final/build.py --rapido"
else
  echo "El build fallo. Mira los logs en salida/_logs_build/"
  exit 1
fi
