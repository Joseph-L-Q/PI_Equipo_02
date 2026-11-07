# Prepara el CAD del nodo LanternGuard en Windows y prueba que regenera.
#   powershell -ExecutionPolicy Bypass -File .\setup_laptop.ps1
# Crea .venv\ junto a este archivo, instala requirements.txt y corre: python cad_final/build.py --rapido
$ErrorActionPreference = "Continue"  # native tools write warnings to stderr; exit codes are checked
Set-Location -LiteralPath $PSScriptRoot
$t0 = Get-Date

function Find-Python312 {
    foreach ($c in @(@("py", "-3.12"), @("python"), @("python3"))) {
        $exe = $c[0]; $rest = @($c | Select-Object -Skip 1)
        if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { continue }
        try { $v = & $exe @rest -c "import sys; print('%d.%d' % sys.version_info[:2])" 2>$null } catch { continue }
        if ($v -eq "3.12") { return , $c }
    }
    return $null
}

$py = Find-Python312
if (-not $py) {
    Write-Host "No encontre Python 3.12." -ForegroundColor Red
    Write-Host "Instalalo con:  winget install -e --id Python.Python.3.12"
    Write-Host "o desde https://www.python.org/downloads/release/python-31210/ (marca 'Add python.exe to PATH')."
    Write-Host "Despues cierra y abre la terminal y vuelve a correr este script."
    exit 1
}
Write-Host "Python 3.12 encontrado: $($py -join ' ')"

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creando .venv ..."
    $exe = $py[0]; $rest = @($py | Select-Object -Skip 1)
    & $exe @rest -m venv .venv
    if ($LASTEXITCODE -ne 0) { Write-Host "No se pudo crear .venv" -ForegroundColor Red; exit 1 }
}
$vpy = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

Write-Host "Instalando dependencias (la primera vez tarda varios minutos) ..."
& $vpy -m pip install --upgrade pip --quiet
& $vpy -m pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) { Write-Host "Fallo pip install -r requirements.txt" -ForegroundColor Red; exit 1 }

Write-Host "Regenerando (build --rapido) ..."
& $vpy cad_final/build.py --rapido
$ok = ($LASTEXITCODE -eq 0)
$min = [math]::Round(((Get-Date) - $t0).TotalMinutes, 1)
if ($ok) {
    Write-Host "LISTO en $min min. Para regenerar despues:  .venv\Scripts\python.exe cad_final/build.py --rapido" -ForegroundColor Green
} else {
    Write-Host "El build fallo ($min min). Mira los logs en salida\_logs_build\" -ForegroundColor Red
    exit 1
}
