Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'

if (-not (Test-Path $pythonExe)) {
    throw "No se encontró el Python del venv en '$pythonExe'. Crea el entorno virtual primero."
}

& $pythonExe -m streamlit run (Join-Path $projectRoot 'dashboard.py')