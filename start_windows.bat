@echo off

echo ============================
echo       EduGenie
echo ============================

echo.

if not exist ".venv" (

    echo Creating virtual environment...

    py -3 -m venv .venv

)

echo.

echo Activating environment...

call .venv\Scripts\activate

echo.

echo Installing dependencies...

python -m pip install --upgrade pip

pip install -r requirements.txt

echo.

if not exist ".env" (

    copy .env.example .env

    echo.
    echo .env file created.
    echo Please add your Gemini API key.
    echo.

)

echo Starting EduGenie...

uvicorn main:app --reload

pause