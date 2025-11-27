@echo off
REM Smart Blood Bank - Windows Setup Script

echo Smart Blood Bank - Setup
echo ========================

:menu
echo.
echo Available Commands:
echo 1. Install dependencies
echo 2. Setup environment
echo 3. Check setup
echo 4. Start database (Docker)
echo 5. Stop database
echo 6. Run migrations
echo 7. Run tests
echo 8. Start server
echo 9. Exit
echo.

set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto setup
if "%choice%"=="3" goto check
if "%choice%"=="4" goto db_up
if "%choice%"=="5" goto db_down
if "%choice%"=="6" goto migrate
if "%choice%"=="7" goto test
if "%choice%"=="8" goto run
if "%choice%"=="9" goto end

echo Invalid choice!
goto menu

:install
echo Installing dependencies...
cd backend
pip install -r requirements.txt
cd ..
echo Done!
goto menu

:setup
echo Setting up environment...
copy .env.example .env
echo Done! Edit .env with your configuration.
goto menu

:check
echo Checking setup...
python scripts\check_setup.py
goto menu

:db_up
echo Starting PostgreSQL...
docker-compose up -d db
echo Done!
goto menu

:db_down
echo Stopping PostgreSQL...
docker-compose down
echo Done!
goto menu

:migrate
echo Running migrations...
cd backend
alembic upgrade head
cd ..
echo Done!
goto menu

:test
echo Running tests...
cd backend
pytest ..\tests\ -v
cd ..
goto menu

:run
echo Starting development server...
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
cd ..
goto menu

:end
echo Goodbye!
