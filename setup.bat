@echo off
echo ============================================================
echo   Dynamic AI Chatbot (Python + FastAPI) — Windows Setup
echo ============================================================
echo.

echo [1/6] Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Install from https://python.org
    pause & exit /b 1
)

echo.
echo [2/6] Creating virtual environment...
cd backend
python -m venv venv
call venv\Scripts\activate
echo Virtual environment ready!

echo.
echo [3/6] Installing Python dependencies...
pip install fastapi "uvicorn[standard]" python-socketio python-dotenv pydantic pydantic-settings
pip install nltk scikit-learn numpy scipy vaderSentiment textblob
pip install motor pymongo "python-jose[cryptography]" "passlib[bcrypt]" bcrypt loguru httpx aiofiles psutil
echo Python dependencies installed!

echo.
echo [4/6] Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

echo.
echo [5/6] Setting up .env files...
if not exist .env ( copy .env.example .env && echo Backend .env created )
cd ..\frontend
if not exist .env ( copy .env.example .env && echo Frontend .env created )

echo.
echo [6/6] Installing Frontend dependencies...
npm install
if %errorlevel% neq 0 ( echo ERROR: npm install failed! & pause & exit /b 1 )

cd ..
echo.
echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
echo   TERMINAL 1 — Start Backend:
echo     cd backend
echo     venv\Scripts\activate
echo     uvicorn main:socket_app --reload --port 8000
echo.
echo   TERMINAL 2 — Start Frontend:
echo     cd frontend
echo     npm start
echo.
echo   Browser: http://localhost:3000
echo   API Docs: http://localhost:8000/docs
echo ============================================================
pause
