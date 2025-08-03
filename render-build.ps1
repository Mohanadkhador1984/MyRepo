# render-build.ps1
Write-Output "1. Building Vue frontend"

cd frontend/quiz-frontend
npm ci
npm run build
cd ../../backend
python -m pip install --upgrade pip setuptools
pip install -r requirements.txt
python manage.py collectstatic --no-input

Write-Output "2. Installing backend dependencies"
$env:PORT = $env:PORT -or 8000  # Default port if not set
gunicorn quiz_project.wsgi:application --bind 0.0.0.0:$env:PORT --workers 3 --log-level info