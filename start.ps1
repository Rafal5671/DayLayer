# Daylayer - Start Script

Write-Host "Starting Daylayer..." -ForegroundColor Cyan

# Redis
Write-Host "Starting Redis..." -ForegroundColor Yellow
docker run -d -p 6379:6379 --name daylayer-redis redis:alpine 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Redis already running, skipping..." -ForegroundColor Gray
    docker start daylayer-redis 2>$null
}

Start-Sleep -Seconds 2

# Django
Write-Host "Starting Django..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; .\venv\Scripts\activate; python manage.py runserver"

# Celery
Write-Host "Starting Celery..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; .\venv\Scripts\activate; celery -A config worker --loglevel=info --pool=solo"

# Scraping Service
Write-Host "Starting Scraping Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\scraping-service'; .\venv\Scripts\activate; uvicorn main:app --port 8001 --reload"

# Frontend
Write-Host "Starting Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

Write-Host ""
Write-Host "Daylayer is running!" -ForegroundColor Green
Write-Host "Django:           http://localhost:8000" -ForegroundColor White
Write-Host "Scraping Service: http://localhost:8001" -ForegroundColor White
Write-Host "Frontend:         http://localhost:5173" -ForegroundColor White
