#!/bin/bash
set -e
echo "============================================================"
echo "  Dynamic AI Chatbot (Python + FastAPI) — Mac/Linux Setup"
echo "============================================================"

echo ""
echo "[1/6] Checking Python..."
python3 --version || { echo "Install Python 3.10+ from https://python.org"; exit 1; }

echo ""
echo "[2/6] Creating virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
echo "✅ venv activated"

echo ""
echo "[3/6] Installing Python deps (this may take 2-5 mins)..."
pip install --upgrade pip -q
pip install fastapi "uvicorn[standard]" python-socketio python-dotenv pydantic pydantic-settings -q
pip install nltk scikit-learn numpy scipy vaderSentiment textblob -q
pip install motor pymongo "python-jose[cryptography]" "passlib[bcrypt]" bcrypt loguru httpx aiofiles psutil -q
echo "✅ Python dependencies installed"

echo ""
echo "[4/6] Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
echo "✅ NLTK data ready"

echo ""
echo "[5/6] Setting up .env files..."
[ ! -f .env ] && cp .env.example .env && echo "✅ Backend .env created"
cd ../frontend
[ ! -f .env ] && cp .env.example .env && echo "✅ Frontend .env created"

echo ""
echo "[6/6] Installing Frontend dependencies..."
npm install --silent
echo "✅ Frontend dependencies installed"

cd ..
echo ""
echo "============================================================"
echo "  ✅ Setup Complete!"
echo "============================================================"
echo ""
echo "  TERMINAL 1 — Start Backend:"
echo "    cd backend && source venv/bin/activate"
echo "    uvicorn main:socket_app --reload --port 8000"
echo ""
echo "  TERMINAL 2 — Start Frontend:"
echo "    cd frontend && npm start"
echo ""
echo "  Browser:   http://localhost:3000"
echo "  API Docs:  http://localhost:8000/docs"
echo "============================================================"
