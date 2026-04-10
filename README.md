<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=30&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&width=600&lines=🤖+Dynamic+AI+Chatbot;Python+%2B+FastAPI+%2B+NLP+%2B+React;Advanced+Conversational+AI+System" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Socket.IO](https://img.shields.io/badge/Socket.IO-4.7-010101?style=for-the-badge&logo=socket.io&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

<br/>

> **A production-grade, full-stack AI Chatbot** powered by Natural Language Processing, Machine Learning, and Real-time WebSocket communication.

<br/>

**🏢 Amdox Technologies Internship Project**
**👥 Group 3 | Batch 4.2 | 2026**

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Live Demo & Screenshots](#-live-demo--screenshots)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [AI Models Explained](#-ai-models-explained)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [API Reference & Testing](#-api-reference--testing)
- [Socket.IO Events](#-socketio-events)
- [Features](#-features)
- [Git Setup & GitHub Push](#-git-setup--github-push)
- [Team Members](#-team-members)
- [Acknowledgements](#-acknowledgements)

---

## 🎯 Project Overview

The **Dynamic AI Chatbot** is a conversational AI system that understands natural language, responds contextually, and provides intelligent interactions. It was built as an internship capstone project at **Amdox Technologies** to demonstrate practical implementation of:

- 🧠 **Natural Language Processing (NLP)** — Intent recognition, sentiment analysis, NER
- 🤖 **Machine Learning (ML)** — Naive Bayes classifier, MLP neural network
- ⚡ **Real-time Systems** — WebSocket via Socket.IO
- 🗄️ **Database Integration** — MongoDB for persistent conversation storage
- ⚛️ **Modern Frontend** — React 18 with responsive glassmorphism UI

### What Makes This Chatbot Special

| Feature | Description |
|---|---|
| **Knowledge Base AI** | 25+ technical topics with code examples — Java, Python, OOP, ML, APIs |
| **Emotion Priority** | Detects 5 emotions — sad, angry, anxious, happy, very sad — empathetic responses |
| **Multi-Intent** | Handles multiple questions in one message |
| **Context Memory** | 20-turn sliding window — remembers your name and previous topics |
| **Self-Learning** | ML model retrains automatically every 10 user feedbacks |
| **Zero Downtime** | In-memory fallback when MongoDB is unavailable |

---

## 🖥️ Live Demo & Screenshots

```
Frontend:  http://localhost:3000
Backend:   http://localhost:8000
API Docs:  http://localhost:8000/docs
```

### Chat Interface
```
User:  "What is Java?"
Bot:   ## 📚 Java Programming Language
       Java is a high-level, OOP language by Sun Microsystems (1995)
       ✅ Platform independent — Write Once Run Anywhere
       ✅ Frameworks: Spring, Hibernate
       ✅ Used for: Android, enterprise apps...

User:  "Explain OOP concepts"
Bot:   ## 📚 Object-Oriented Programming (OOP)
       4 Pillars: Encapsulation, Inheritance, Polymorphism, Abstraction
       [Code examples in Python included]

User:  "I feel sad today"
Bot:   I can feel you're going through a tough time 💙
       Would you like to talk about what's bothering you?
```

---

## 🛠️ Technology Stack

### Backend Stack

| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.10+ | Core programming language |
| **FastAPI** | 0.109 | High-performance async web framework |
| **Uvicorn** | 0.27 | ASGI server for FastAPI |
| **Socket.IO** | 5.11 | Real-time WebSocket communication |
| **NLTK** | 3.8 | NLP tokenization, text processing |
| **scikit-learn** | 1.4 | Naive Bayes, TF-IDF, MLP Neural Network |
| **NumPy** | 1.26 | Numerical arrays for ML |
| **SciPy** | 1.12 | Scientific computing |
| **VADER Sentiment** | 3.3 | Rule-based sentiment analysis |
| **TextBlob** | 0.17 | NLP fallback processing |
| **Motor** | 3.3 | Async MongoDB driver |
| **PyMongo** | 4.6 | MongoDB sync driver |
| **Pydantic** | 2.5 | Data validation + request/response models |
| **python-jose** | 3.3 | JWT authentication tokens |
| **passlib + bcrypt** | 1.7 | Secure password hashing |
| **Loguru** | 0.7 | Structured logging |
| **psutil** | 5.9 | CPU/memory monitoring |

### Frontend Stack

| Technology | Version | Purpose |
|---|---|---|
| **React** | 18.2 | UI component framework |
| **React Router DOM** | 6.21 | Client-side navigation |
| **Socket.IO Client** | 4.7 | Real-time backend connection |
| **Axios** | 1.6 | HTTP REST API calls |
| **Recharts** | 2.10 | Analytics charts (Bar, Pie, Area, Radial) |
| **React Markdown** | 9.0 | Render bot markdown responses |
| **React Hot Toast** | 2.4 | Toast notifications |
| **Lucide React** | 0.303 | Modern icon library |
| **Tailwind CSS** | 3.4 | Utility-first CSS framework |
| **Framer Motion** | 10.18 | Smooth animations |

### Infrastructure

| Technology | Purpose |
|---|---|
| **MongoDB Atlas / Local** | Persistent conversation storage |
| **In-Memory Fallback** | Works without MongoDB too |
| **WebSocket (Socket.IO)** | Real-time bidirectional communication |
| **REST API** | Alternative HTTP communication |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT (React 18)                     │
│  ┌──────────────┐  ┌─────────────────┐  ┌────────────┐  │
│  │   Chat Page  │  │ Analytics Page  │  │  Sidebar   │  │
│  │  (ChatPage)  │  │(AnalyticsPage)  │  │ (Sidebar)  │  │
│  └──────┬───────┘  └────────┬────────┘  └────────────┘  │
│         │                  │                             │
│         │ Socket.IO    Axios HTTP                        │
└─────────┼──────────────────┼─────────────────────────────┘
          │                  │
          ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│                  FASTAPI BACKEND                         │
│                                                         │
│  ┌─────────────┐    ┌──────────────┐                    │
│  │  Socket.IO  │    │   REST API   │                    │
│  │   Events    │    │   Routers    │                    │
│  └──────┬──────┘    └──────┬───────┘                   │
│         │                  │                            │
│         └────────┬─────────┘                           │
│                  ▼                                      │
│  ┌───────────────────────────────────────────────┐     │
│  │              NLP ENGINE v5.0                  │     │
│  │                                               │     │
│  │  ┌─────────────┐   ┌─────────────────────┐   │     │
│  │  │   Intent    │   │  Emotion Detector   │   │     │
│  │  │ Classifier  │   │ (5 emotion types)   │   │     │
│  │  │(Naive Bayes)│   └─────────────────────┘   │     │
│  │  └─────────────┘                             │     │
│  │  ┌─────────────┐   ┌─────────────────────┐   │     │
│  │  │  Sentiment  │   │  Context Manager    │   │     │
│  │  │  Analyzer   │   │  (20-turn memory)   │   │     │
│  │  │   (VADER)   │   └─────────────────────┘   │     │
│  │  └─────────────┘                             │     │
│  │  ┌─────────────┐   ┌─────────────────────┐   │     │
│  │  │     NER     │   │  Knowledge Base     │   │     │
│  │  │  Processor  │   │  (25+ tech topics)  │   │     │
│  │  │  (Regex)    │   └─────────────────────┘   │     │
│  │  └─────────────┘                             │     │
│  │  ┌─────────────────────────────────────────┐ │     │
│  │  │     Response Generator                  │ │     │
│  │  │  (Dynamic — no hardcoded answers)       │ │     │
│  │  └─────────────────────────────────────────┘ │     │
│  └───────────────────────────────────────────────┘     │
│                                                         │
│  ┌──────────────────┐   ┌───────────────────────────┐  │
│  │   ML Model       │   │   Analytics Service       │  │
│  │  (MLP Neural Net)│   │  (In-memory tracking)     │  │
│  │  Self-learning   │   └───────────────────────────┘  │
│  └──────────────────┘                                   │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│                    MongoDB Database                      │
│  conversations | feedback | users | analytics            │
└─────────────────────────────────────────────────────────┘
```

---

## 🧠 AI Models Explained

### 1. Intent Classifier — Naive Bayes + TF-IDF

```python
Algorithm:    Multinomial Naive Bayes
Features:     TF-IDF vectors (unigrams + bigrams + trigrams)
Max Features: 12,000
Training Data: 570+ labeled phrases
Intents:      16 categories
Min per class: 27 examples
```

**16 Intent Categories:**

| Intent | Example Input |
|---|---|
| `greeting` | "Hello!", "Hi there!", "Good morning" |
| `farewell` | "Bye", "Goodbye", "Take care" |
| `thanks` | "Thank you", "Appreciate it" |
| `help` | "What can you do?", "Show features" |
| `about` | "Who are you?", "Introduce yourself" |
| `technical` | "What is Java?", "Explain OOP" |
| `time_date` | "What time is it?", "Today's date?" |
| `weather` | "How's the weather?", "Will it rain?" |
| `joke` | "Tell me a joke", "Make me laugh" |
| `math` | "What is calculus?", "Explain algebra" |
| `emotion_happy` | "I am so happy today!" |
| `emotion_sad` | "I'm feeling low" |
| `emotion_angry` | "I'm so frustrated!" |
| `emotion_anxious` | "I'm very stressed" |
| `compliment` | "You're amazing!" |
| `negative_feedback` | "Wrong answer", "Not helpful" |

### 2. MLP Neural Network — Self-Learning

```
Architecture: [9 → 64 → 32 → 16 → 7]
Activation:   ReLU
Optimizer:    Adam
Max Iter:     1000
Input:        9 encoded features
Output:       7 probability scores
Auto-retrain: Every 10 user feedbacks
```

**9 Input Features:**

| Feature | Encoding |
|---|---|
| `has_greeting` | 1.0 if greeting keywords found |
| `has_question` | 1.0 if question words found |
| `has_negative` | 1.0 if negative words found |
| `has_positive` | 1.0 if positive words found |
| `has_thanks` | 1.0 if thanks words found |
| `has_tech` | 1.0 if tech keywords found |
| `msg_length` | Normalized (0.0 to 1.0) |
| `word_count` | Normalized (0.0 to 1.0) |
| `has_emotion` | 1.0 if emotion keywords found |

### 3. VADER Sentiment Analyzer

```
Type:      Rule-based + Valence-aware
Score:     Compound (-1.0 to +1.0)
Labels:    5 categories
```

| Score Range | Label | Emoji |
|---|---|---|
| >= 0.5 | Very Positive | 😄 |
| 0.05 to 0.5 | Positive | 🙂 |
| -0.05 to 0.05 | Neutral | 😐 |
| -0.5 to -0.05 | Negative | 😟 |
| <= -0.5 | Very Negative | 😢 |

### 4. Knowledge Base Response System

```
Topics:    25+ technical topics
Content:   Explanations + Code examples
Priority:  Checked BEFORE ML classifier
Coverage:  Java, Python, JS, OOP, ML, DL, NLP,
           APIs, MongoDB, Git, Docker, Algorithms,
           Data Structures, Cloud Computing, etc.
```

### 5. Named Entity Recognition (NER)

```
Emails:     Regex pattern
Phones:     Regex pattern
URLs:       Regex pattern
Dates:      Regex pattern
Currencies: Regex pattern
Locations:  Keyword matching (20+ cities/countries)
Persons:    Pattern-based ("my name is X")
```

### 6. Context Manager

```
Memory:         20-turn sliding window
Personalization: Extracts user name
Emotion History: Last 5 emotions tracked
Cleanup:        Auto-removes inactive sessions
```

---

## 📁 Project Structure

```
ai-chatbot-python/
│
├── 📄 README.md
├── 📄 PROJECT_REPORT.md
├── 📄 .gitignore
├── 📄 setup.bat                    ← Windows one-click setup
├── 📄 setup.sh                     ← Mac/Linux setup
├── 📄 chatbot-python.code-workspace← VS Code workspace
│
├── 🐍 backend/
│   ├── 📄 main.py                  ← FastAPI app + Socket.IO + all events
│   ├── 📄 requirements.txt         ← All Python dependencies
│   ├── 📄 .env.example             ← Environment variables template
│   │
│   └── app/
│       ├── api/
│       │   ├── chat.py             ← Chat REST endpoints
│       │   ├── analytics.py        ← Analytics endpoints
│       │   ├── auth.py             ← JWT auth endpoints
│       │   └── websocket.py        ← WebSocket info
│       │
│       ├── controllers/
│       │   └── chat_controller.py  ← Shared chat processing logic
│       │
│       ├── core/
│       │   ├── config.py           ← Settings from .env
│       │   └── database.py         ← MongoDB + fallback
│       │
│       ├── models/
│       │   └── schemas.py          ← Pydantic models
│       │
│       ├── services/
│       │   ├── nlp_engine.py       ← 🧠 Core AI (NLP + KB + Context)
│       │   ├── ml_model.py         ← 🤖 MLP Neural Network
│       │   └── analytics_service.py← 📊 Metrics tracker
│       │
│       ├── training/
│       │   └── train.py            ← Model training script
│       │
│       └── data/
│           └── feedback_data.json  ← Auto-created: feedback storage
│
└── ⚛️ frontend/
    ├── 📄 package.json
    ├── 📄 tailwind.config.js
    ├── 📄 postcss.config.js
    ├── 📄 .env.example
    │
    ├── public/
    │   └── index.html
    │
    └── src/
        ├── App.js                  ← Router + Socket.IO context
        ├── index.js
        ├── styles/
        │   └── index.css           ← Glassmorphism + responsive CSS
        ├── components/
        │   ├── Sidebar.js          ← Desktop navigation
        │   └── Canvas.js           ← Particle background
        └── pages/
            ├── ChatPage.js         ← Full chat interface
            └── AnalyticsPage.js    ← Dashboard with charts
```

---

## ⚙️ Prerequisites

| Tool | Version | Download |
|---|---|---|
| Python | 3.10+ | https://python.org/downloads |
| Node.js | 18+ | https://nodejs.org |
| VS Code | Latest | https://code.visualstudio.com |
| Git | Any | https://git-scm.com |
| MongoDB | 6+ (optional) | https://mongodb.com/try/download/community |

---

## 🚀 Installation & Setup

### Step 1 — Clone / Extract Project

```bash
# If from GitHub:
git clone https://github.com/YOUR_USERNAME/dynamic-ai-chatbot.git
cd dynamic-ai-chatbot

# If from ZIP:
# Extract → open folder in VS Code
```

### Step 2 — Backend Setup (Python)

Open **Terminal 1** in VS Code (`Ctrl + `` ` ``):

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install all libraries
pip install fastapi "uvicorn[standard]" python-socketio python-dotenv pydantic pydantic-settings
pip install nltk scikit-learn numpy scipy vaderSentiment textblob
pip install motor pymongo "python-jose[cryptography]" "passlib[bcrypt]" bcrypt
pip install loguru httpx aiofiles psutil python-multipart

# Setup .env file
copy .env.example .env

# Generate SECRET_KEY (copy the output and paste in .env)
python -c "import secrets; print(secrets.token_hex(32))"

# Start server
uvicorn main:socket_app --reload --host 0.0.0.0 --port 8000
```

**✅ Expected output:**
```
🚀 Starting Dynamic AI Chatbot Server...
✅ Intent Classifier trained: 570 samples | 16 intents | min_per_class=27
✅ ML Model trained: 24 samples, early_stopping=True, #1
✅ VADER Sentiment Analyzer ready
🚀 NLP Engine v5.0 ready — Model analyzes everything itself!
✅ Server ready at http://0.0.0.0:8000
📡 WebSocket: Active | REST API: Active | Analytics: Active
```

### Step 3 — Frontend Setup (React)

Open **Terminal 2**:

```bash
cd frontend
npm install
copy .env.example .env
npm start
```

**✅ Browser opens at:** `http://localhost:3000`

### Step 4 — .env Configuration

Edit `backend/.env`:

```dotenv
# Required
SECRET_KEY=paste_your_generated_key_here

# MongoDB (optional — app works without it)
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_chatbot_db

# Leave these as-is for local development
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

---

## 🌐 API Reference & Testing

### Base URL
```
http://localhost:8000/api
```

### Interactive Docs
```
http://localhost:8000/docs      ← Swagger UI
http://localhost:8000/redoc     ← ReDoc
```

---

### 💬 Chat Endpoints

#### POST `/api/chat/message` — Send a Message

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Java?",
    "session_id": "test-session-001"
  }'
```

**Response:**
```json
{
  "session_id": "test-session-001",
  "message": "## 📚 Java Programming Language\n\nJava is a high-level, object-oriented programming language...",
  "metadata": {
    "intent": {
      "intent": "technical",
      "confidence": 0.98,
      "kb_topic": "java",
      "all_scores": {"technical": 0.98}
    },
    "emotion": null,
    "sentiment": {
      "label": "neutral",
      "score": 0.0,
      "emoji": "😐",
      "compound": 0.0,
      "positive_words": [],
      "negative_words": []
    },
    "entities": {
      "emails": [], "phones": [], "urls": [],
      "locations": [], "persons": []
    },
    "multi_intents": [{"intent": "technical", "confidence": 0.98}],
    "processing_time_ms": 14.2,
    "turn_count": 1,
    "contextual": false,
    "context_summary": {
      "user_name": null,
      "last_intent": null
    }
  },
  "timestamp": "2026-03-29T18:30:00Z"
}
```

---

#### POST `/api/chat/message` — Emotion Detection

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am feeling very sad today",
    "session_id": "test-session-001"
  }'
```

**Response:**
```json
{
  "session_id": "test-session-001",
  "message": "I can feel you're going through a tough time 💙 That's completely okay...",
  "metadata": {
    "intent": {"intent": "emotion_sad", "confidence": 0.89},
    "emotion": "sad",
    "sentiment": {"label": "very_negative", "score": -0.72, "emoji": "😢"},
    "processing_time_ms": 9.8,
    "turn_count": 2,
    "contextual": true
  }
}
```

---

#### POST `/api/chat/message` — Multi-Intent

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Python and tell me a joke",
    "session_id": "test-session-001"
  }'
```

**Response:**
```json
{
  "message": "I see **2 questions** — let me address them:\n\n## 📚 Python...\n\n---\nWhy do programmers prefer dark mode?...",
  "metadata": {
    "multi_intents": [
      {"intent": "technical", "confidence": 0.97, "segment": "What is Python"},
      {"intent": "joke", "confidence": 0.88, "segment": "tell me a joke"}
    ]
  }
}
```

---

#### GET `/api/chat/history/{session_id}` — Get History

```bash
curl http://localhost:8000/api/chat/history/test-session-001
```

**Response:**
```json
{
  "session_id": "test-session-001",
  "messages": [
    {
      "user_message": "What is Java?",
      "bot_response": "## 📚 Java...",
      "intent": "technical",
      "created_at": "2026-03-29T18:30:00Z"
    }
  ],
  "count": 1,
  "source": "mongodb"
}
```

---

#### DELETE `/api/chat/history/{session_id}` — Clear History

```bash
curl -X DELETE http://localhost:8000/api/chat/history/test-session-001
```

**Response:**
```json
{
  "message": "History cleared",
  "session_id": "test-session-001",
  "deleted_from_db": 3
}
```

---

#### POST `/api/chat/feedback` — Submit Feedback (triggers ML retrain)

```bash
curl -X POST http://localhost:8000/api/chat/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-001",
    "message_content": "What is Java?",
    "rating": 5,
    "was_helpful": true,
    "correct_intent": "technical"
  }'
```

**Response:**
```json
{"message": "Feedback received! Thank you! 🙏"}
```

---

#### POST `/api/chat/analyze` — NLP Analysis Only

```bash
curl -X POST http://localhost:8000/api/chat/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I am really happy about machine learning!"}'
```

**Response:**
```json
{
  "text": "I am really happy about machine learning!",
  "analysis": {
    "intent": {"intent": "emotion_happy", "confidence": 0.91},
    "emotion": "happy",
    "sentiment": {
      "label": "very_positive",
      "score": 0.64,
      "emoji": "😄",
      "positive_words": ["happy"],
      "negative_words": []
    },
    "entities": {"emails": [], "locations": [], "persons": []},
    "multi_intents": [{"intent": "emotion_happy", "confidence": 0.91}],
    "ml_prediction": {"dominant": "positive", "confidence": 0.78},
    "word_count": 8,
    "char_count": 41
  }
}
```

---

### 📊 Analytics Endpoints

#### GET `/api/analytics/dashboard`

```bash
curl http://localhost:8000/api/analytics/dashboard
```

**Response:**
```json
{
  "realtime": {
    "server_uptime_seconds": 3600,
    "memory_usage_mb": 245.3,
    "cpu_percent": 12.4,
    "nlp_engine_ready": true,
    "ml_model_ready": true,
    "active_sessions": 3
  },
  "session_stats": {
    "total_messages": 47,
    "total_sessions": 5,
    "avg_response_time_ms": 18.4,
    "avg_confidence": 0.9123,
    "intent_distribution": {
      "technical": 18,
      "greeting": 9,
      "joke": 5,
      "emotion_sad": 3
    },
    "sentiment_distribution": {
      "neutral": 22,
      "positive": 14,
      "very_positive": 7,
      "negative": 4
    },
    "hourly_activity": {"14": 12, "15": 23, "16": 12}
  },
  "model_stats": {
    "is_ready": true,
    "feedback_count": 8,
    "retrain_count": 1,
    "architecture": "MLP [9 → 64 → 32 → 16 → 7] (MultiOutput)"
  }
}
```

---

#### GET `/api/analytics/intents`

```bash
curl http://localhost:8000/api/analytics/intents
```

**Response:**
```json
{
  "distribution": {"technical": 18, "greeting": 9, "joke": 5},
  "total": 32,
  "top_intent": "technical",
  "intent_count": 3
}
```

---

### 🔐 Auth Endpoints

#### POST `/api/auth/register`

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {"id": "uuid-here", "username": "john_doe", "role": "user"}
}
```

---

#### POST `/api/auth/login`

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "securepassword123"}'
```

---

#### GET `/api/health`

```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "5.0.0",
  "nlp_engine": true,
  "ml_model": true,
  "environment": "development",
  "total_messages": 47,
  "total_sessions": 5
}
```

---

## 🔌 Socket.IO Events

### Connect & Chat (JavaScript example)

```javascript
import { io } from "socket.io-client";

const socket = io("http://localhost:8000");

// Connected
socket.on("connected", ({ socket_id, message }) => {
  console.log("Connected:", socket_id);
});

// Send message
socket.emit("chat_message", {
  message: "What is Python?",
  session_id: "my-session-123"
});

// Bot is typing
socket.on("bot_typing", ({ typing }) => {
  console.log("Bot typing:", typing);
});

// Receive response
socket.on("bot_response", ({ message, metadata, session_id }) => {
  console.log("Bot:", message);
  console.log("Intent:", metadata.intent.intent);
  console.log("Sentiment:", metadata.sentiment.label);
});

// Active users
socket.on("user_count", ({ count }) => {
  console.log("Active users:", count);
});
```

### All Events Reference

**Client → Server:**

| Event | Payload | Description |
|---|---|---|
| `chat_message` | `{message, session_id}` | Send message |
| `user_typing` | `{typing}` | Typing indicator |
| `clear_session` | `{session_id}` | Clear context |
| `feedback` | `{message_content, correct_intent, was_helpful}` | Feedback |

**Server → Client:**

| Event | Payload | Description |
|---|---|---|
| `connected` | `{socket_id, message}` | Connection confirmed |
| `bot_typing` | `{typing: bool}` | Typing indicator |
| `bot_response` | `{message, metadata, session_id}` | AI response |
| `user_count` | `{count}` | Active connections |
| `session_cleared` | `{session_id}` | Clear confirmed |
| `feedback_received` | `{message}` | Feedback ack |

---

## ✨ Features

### Core AI Features
- ✅ Intent Recognition — 16 categories, Naive Bayes + TF-IDF
- ✅ Emotion Detection — 5 types with empathetic responses
- ✅ Sentiment Analysis — VADER compound scoring
- ✅ Named Entity Recognition — email, phone, URL, location, person
- ✅ Multi-Intent Handling — multiple questions in one message
- ✅ Context Memory — 20-turn sliding window with name memory
- ✅ Knowledge Base — 25+ technical topics with code examples
- ✅ Self-Learning — ML retrains on user feedback

### UI/UX Features
- ✅ Dark glassmorphism design
- ✅ Animated particle network background
- ✅ NLP metadata overlay per message (click ⚡)
- ✅ Sentiment badges with color coding
- ✅ Thumbs up/down feedback → ML retrain
- ✅ Copy button for responses
- ✅ Quick prompt chips
- ✅ Analytics dashboard — Bar, Pie, Area, Radial charts
- ✅ Socket/REST toggle
- ✅ Chat export to .txt
- ✅ Fully responsive — mobile + tablet + desktop

### Backend Features
- ✅ FastAPI with auto Swagger docs at `/docs`
- ✅ Socket.IO real-time WebSocket
- ✅ MongoDB integration with in-memory fallback
- ✅ JWT authentication
- ✅ Rate limiting
- ✅ GZIP compression
- ✅ CORS configured
- ✅ Background tasks for async DB saves

---

## 📤 Git Setup & GitHub Push

### Step 1 — Create GitHub Repository

1. Go to **https://github.com/new**
2. Repository name: `dynamic-ai-chatbot`
3. Description: `🤖 Advanced AI Chatbot — Python FastAPI + NLP + React | Amdox Technologies Internship 2026`
4. Visibility: **Public**
5. **DO NOT** initialize with README (we have one)
6. Click **Create repository**

---

### Step 2 — Initialize Git Locally

Open VS Code terminal in your project root:

```bash
# Make sure you're in the project root folder
cd D:\Semseter4\ai-chatbot-python

# Initialize git
git init

# Set your identity
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

---

### Step 3 — Create .gitignore

```bash
# Create .gitignore (already in project, verify it has these):
```

The `.gitignore` should contain:
```
venv/
__pycache__/
*.pyc
*.pyo
.env
*.log
backend/app/data/feedback_data.json
backend/app/training/saved_models/
node_modules/
frontend/build/
.DS_Store
Thumbs.db
```

---

### Step 4 — Stage & Commit

```bash
# Add all files
git add .

# First commit
git commit -m "🚀 Initial commit — Dynamic AI Chatbot

- FastAPI backend with NLP Engine v5.0
- Naive Bayes + TF-IDF intent classifier (16 intents)
- VADER sentiment analysis (5 emotion types)
- MLP Neural Network with self-learning
- Knowledge base with 25+ tech topics
- MongoDB integration with fallback
- React 18 frontend with glassmorphism UI
- Socket.IO real-time communication
- Analytics dashboard with Recharts
- Responsive design (mobile + desktop)

Team: Group 3, Batch 4.2 | Amdox Technologies 2026"
```

---

### Step 5 — Connect to GitHub & Push

```bash
# Connect to your GitHub repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/dynamic-ai-chatbot.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

---

### Step 6 — Future Updates

```bash
# After making changes:
git add .
git commit -m "✨ Fix: improved OOP explanation with code examples"
git push
```

---

### Suggested Commit Message Format

```
🚀 Initial commit
✨ Add: new feature
🐛 Fix: bug description
📝 Docs: update README
🎨 Style: UI improvements
🔧 Config: settings update
🧪 Test: add tests
♻️ Refactor: code cleanup
```

---

## 👥 Team Members

<div align="center">

| Name | Role |
|---|---|
| 👨‍💻 **Abhinash Kumar** | Backend Development, NLP Engine |
| 👨‍💻 **Nirnay Kumar** | Machine Learning, Model Training |
| 👨‍💻 **Avinash Kumar** | Frontend Development, UI/UX |
| 👩‍💻 **Divyani Singh** | Database Integration, Analytics |
| 👨‍💻 **Sunny Kumar** | API Development, Testing |

**Group 3 | Batch 4.2 | 2026**

</div>

---

## 🙏 Acknowledgements

<div align="center">

A **huge shoutout** to our amazing team members who contributed to every aspect of this project!

👨‍💻 **Abhinash Kumar** | 👨‍💻 **Nirnay Kumar** | 👨‍💻 **Avinash Kumar** | 👩‍💻 **Divyani Singh** | 👨‍💻 **Sunny Kumar**

<br/>

### 🏢 Special Thanks

**Thank you Amdox Technologies for this incredible learning opportunity!** 🙏

This internship gave us hands-on experience with:
- Real-world AI/ML implementation
- Full-stack development practices
- Team collaboration on a production-grade project
- Modern technologies: FastAPI, React, MongoDB, NLP

<br/>

*Built with ❤️ | Group 3 | Batch 4.2 | Amdox Technologies 2026*

</div>

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Activate venv: `venv\Scripts\activate` then reinstall |
| CV error in training | Already fixed — using plain `MultinomialNB` |
| Port 8000 in use | `uvicorn main:socket_app --port 8001` |
| MongoDB error | App works without MongoDB (in-memory fallback) |
| Frontend CORS error | Check `.env`: `REACT_APP_BACKEND_URL=http://localhost:8000` |
| Socket not connecting | Start backend first, then frontend |
| `npm install` fails | Delete `node_modules/` folder, run again |

---

<div align="center">

⭐ **If this project helped you, please give it a star on GitHub!** ⭐

*Group 3 | Batch 4.2 | Amdox Technologies Internship 2026*

</div>
