# 🌱 GreenMate AI - Intelligent Plant Care Platform

GreenMate AI is a modern, responsive, full-stack AI-powered plant care and smart garden management platform built with FastAPI, PyMongo, MongoDB Atlas, and Gemini Vision AI.

Inspired by premium botanical design aesthetics, GreenMate AI empowers plant parents to identify unknown species, diagnose foliage diseases, schedule personalized watering routines, track plant growth, and converse with an AI botanical assistant.

---

## 🚀 Key Features

1. **AI Plant Identification**:
   - Computer vision analysis of uploaded plant photos or real-time smartphone camera snapshots.
   - Accurately classifies botanical common name, scientific taxonomy, confidence match percentage, sunlight requirements, watering frequency, and soil substrate.

2. **Smart Plant Doctor & Disease Diagnosis**:
   - Analyzes leaves displaying chlorosis, necrosis, lesions, or mold.
   - Detects diseases (e.g. Cercospora Leaf Spot, Powdery Mildew, Root Rot), highlights visible symptoms, diagnoses potential causes, estimates severity, and prescribes multi-step organic treatment protocols.

3. **Personalized Plant Care Plan Generator**:
   - Generates custom watering, misting, and nutrient schedules tailored to the user's specific room conditions (indoor vs. outdoor) and growth stage.

4. **Conversational Botanical Chatbot**:
   - Floating assistant (*GreenMate AI Assistant*) answering plant care queries in real-time, providing troubleshooting steps and customized follow-up prompts.

5. **Smart Garden Management**:
   - Add catalog or custom plants to your personal collection.
   - Set automated watering reminders with overdue visual indicators.
   - One-click hydration logging ("Mark Watered").
   - Plant growth tracker (height in cm, leaf unfurlings, observation notes).
   - Saved wishlist management.

6. **Botanical Care Guides**:
   - In-depth interactive guides covering Watering Techniques, Sunlight Optimization, Soil Substrate Mixing, Fertilizer Ratios, Disease Prevention, and Seasonal Plant Care.

7. **Responsive Design**:
   - Pixel-perfect layout across desktop, laptop, tablet, and mobile (tested for 320px, 375px, 425px, 768px, 1024px, 1440px+).

---

## 🛠️ Technology Stack

- **Frontend**: HTML5, Modern CSS3 (Grid & Flexbox), Vanilla JavaScript (ES6+ Modules), zero heavy runtime frameworks.
- **Backend**: Python 3.10+, FastAPI, Pydantic v2 validation, Uvicorn ASGI server.
- **Database**: MongoDB Atlas via PyMongo (with automatic fallback to persistent JSON document store when running locally without remote Atlas credentials).
- **Authentication**: Secure JWT (JSON Web Tokens) with salted bcrypt password hashing.
- **AI Integration**: Google Gemini Vision API (`gemini-2.5-flash` / `gemini-1.5-flash`) with native structured output parsing and botanical pathology heuristics.

---

## 📦 Project Structure

```
greenmate-ai/
│
├── frontend/
│   ├── index.html            # Main homepage (10 full sections matching reference screenshot)
│   ├── explore.html          # Plant catalog with live search & category filters
│   ├── plant-details.html    # Full plant specifications & custom care plan generator
│   ├── ai-doctor.html        # AI Plant Doctor & Vision Studio (Camera + Upload)
│   ├── my-garden.html        # Smart Garden dashboard (Watering reminders, growth logs)
│   ├── login.html            # Secure user login with demo account shortcut
│   ├── register.html         # User registration with password hashing
│   ├── guides.html           # Botanical guide library & full articles
│   ├── profile.html          # User profile & saved wishlist
│   │
│   ├── css/
│   │   ├── style.css         # Typography, colors, hero banner, categories, footer
│   │   ├── components.css    # Floating chatbot, modals, dropzones, toasts, buttons
│   │   └── responsive.css    # Media queries for 320px to 1440px+
│   │
│   └── js/
│       ├── api.js            # REST API client
│       ├── auth.js           # JWT authentication & session management
│       ├── plants.js         # Plant card rendering & wishlist operations
│       ├── garden.js         # Garden management, watering logs, growth milestones
│       ├── ai-doctor.js      # Computer vision diagnosis & species identification
│       ├── chatbot.js        # Floating conversational AI assistant
│       └── app.js            # Modals, toasts, search bar, global events
│
├── backend/
│   ├── main.py               # FastAPI application & static file mounts
│   ├── config.py             # App configuration & environment loader
│   ├── database.py           # PyMongo connection & local JSON document store fallback
│   ├── models/               # Pydantic data schemas
│   ├── routes/               # API route handlers (auth, plants, ai, garden, care, etc.)
│   ├── services/             # AI logic (plant_ai, disease_ai, care_ai, chatbot_ai)
│   ├── utils/                # Password hashing, JWT utils, seed data
│   ├── data/                 # Persistent local JSON storage
│   ├── uploads/              # Uploaded plant photographs
│   └── requirements.txt      # Python dependencies
│
├── .env.example              # Environment variables template
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone or Open Workspace
```bash
cd "c:\Users\raaga\OneDrive\Downloads\greenmate ai"
```

### 2. Install Python Dependencies
```bash
python -m pip install -r backend/requirements.txt
```

### 3. Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```
Update with your credentials:
```env
# MongoDB Atlas Connection String (PyMongo)
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/greenmate_db?retryWrites=true&w=majority
DB_NAME=greenmate_db

# Gemini AI API Key
GEMINI_API_KEY=your_gemini_api_key_here

# JWT Secret Key
JWT_SECRET=greenmate_botanical_secret_key_2026
```
> *Note: If `MONGO_URI` is not provided, the application runs on a persistent local document store (`backend/data/db.json`) with the exact same MongoDB collection API, so the site works immediately out of the box!*

---

## 🏃 Running the Application

Start the unified FastAPI server:

```bash
python backend/main.py
```
*(Or via uvicorn directly: `uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload`)*

Once started, open your browser:
- 🌿 **GreenMate AI Website**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 📚 **Interactive Swagger API Docs**: [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)
- 🩺 **AI Plant Doctor Studio**: [http://127.0.0.1:8000/ai-doctor.html](http://127.0.0.1:8000/ai-doctor.html)
- 🪴 **Smart Garden Dashboard**: [http://127.0.0.1:8000/my-garden.html](http://127.0.0.1:8000/my-garden.html)

---

## 🧪 Quick Test & Verification

To verify all endpoints and MongoDB persistence, run:
```bash
python -c "import sys; sys.path.insert(0, 'backend'); from fastapi.testclient import TestClient; from main import app, on_startup; on_startup(); client = TestClient(app); print('Status:', client.get('/api/health').json())"
```

---

## 📄 License
© 2026 GreenMate AI. Built for botanical lovers and indoor gardeners worldwide.
