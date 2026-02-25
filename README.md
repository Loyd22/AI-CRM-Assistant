AI CRM Assistant

AI-powered CRM system with ticket and lead management, including AI-generated summaries, classification, urgency scoring, and draft replies.

🚀 Tech Stack
Frontend

React

TypeScript

Vite

Backend

FastAPI

Uvicorn

AI Integration

OpenAI API (LLM-powered ticket/lead analysis)

Database

SQLite (default local database)

DevOps & Tooling

Docker

Docker Compose

GitHub

🛠️ Installation & Running the Project

This project contains:

Backend → FastAPI (Port 8000)

Frontend → React + Vite (Port 5173)

✅ Option A: Run with Docker (Recommended)
1️⃣ Clone the repository
git clone https://github.com/Loyd22/AI-CRM-Assistant.git
cd AI-CRM-Assistant
2️⃣ Create .env file (Project Root)

Create a .env file beside docker-compose.yml:

OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=your_model_here
3️⃣ Build and start containers
docker compose up --build
4️⃣ Access the application

Frontend:
http://localhost:5173

Backend API Docs (Swagger):
http://localhost:8000/docs

5️⃣ Stop containers

Press:

Ctrl + C

Then run:

docker compose down
💻 Option B: Run Locally (Without Docker)
🔹 Backend Setup
1️⃣ Navigate to backend
cd backend
2️⃣ Create virtual environment
python -m venv .venv
3️⃣ Activate virtual environment

Windows (PowerShell)

.venv\Scripts\Activate.ps1

Mac/Linux

source .venv/bin/activate
4️⃣ Install dependencies
pip install -r requirements.txt
5️⃣ Set environment variables

Windows (PowerShell)

$env:OPENAI_API_KEY="your_openai_key_here"
$env:OPENAI_MODEL="your_model_here"

Mac/Linux

export OPENAI_API_KEY="your_openai_key_here"
export OPENAI_MODEL="your_model_here"
6️⃣ Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Backend will be available at:

http://localhost:8000

http://localhost:8000/docs

🔹 Frontend Setup

Open a new terminal.

1️⃣ Navigate to frontend
cd frontend
2️⃣ Install dependencies
npm install
3️⃣ Set API base URL

Windows (PowerShell)

$env:VITE_API_BASE_URL="http://127.0.0.1:8000"

Mac/Linux

export VITE_API_BASE_URL="http://127.0.0.1:8000"
4️⃣ Run frontend
npm run dev

Frontend will be available at:

http://localhost:5173

🧱 Project Structure
AI-CRM-Assistant/
│
├── backend/          # FastAPI backend
├── frontend/         # React + Vite frontend
├── docker-compose.yml
├── .env              # Environment variables (not committed)
└── README.md
⚠️ Troubleshooting
Port already in use

Make sure ports 8000 and 5173 are not used by other applications.

OpenAI API not working

Ensure .env file exists in the project root and contains:

OPENAI_API_KEY
OPENAI_MODEL
Frontend cannot connect to backend

Confirm backend is running at:

http://127.0.0.1:8000

And VITE_API_BASE_URL is set correctly before starting the frontend.
