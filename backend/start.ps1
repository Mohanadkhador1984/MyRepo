# start.ps1
$ErrorActionPreference = 'Continue'   # لا يقف عند أول خطأ
$ScriptRoot = Split-Path $MyInvocation.MyCommand.Path

Write-Host "Activating virtual environment..."
. "$ScriptRoot\.venv\Scripts\Activate.ps1"

Write-Host "Running migrations..."
try {
    python "$ScriptRoot\manage.py" migrate --noinput
} catch {
    Write-Error "Migration failed: $_"
}

Write-Host "Starting Waitress on port $($env:PORT -or 8000)..."
python -m waitress --port=$($env:PORT -or 8000) quiz_project.wsgi:application
