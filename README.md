Tech Stack
Frontend

React (UI)

TypeScript (type-safe frontend)

Vite (dev server + build tool)

Backend

FastAPI (Python web framework)

Uvicorn (ASGI server)

AI

OpenAI API (LLM analysis for tickets/leads, summaries, etc.)

Database

SQLite (default local database)

DevOps / Tooling

Docker + Docker Compose (containerized local run)

GitHub (version control)

Run the Project

This project has:

Backend: FastAPI (port 8000)

Frontend: React + Vite (port 5173)

Prerequisites

Install these first:

Git

Docker Desktop (recommended)

If running locally (no Docker): Python 3.10+ and Node.js 18+

Option A: Run with Docker (Recommended)
1) Clone the repo
git clone https://github.com/Loyd22/AI-CRM-Assistant.git
cd AI-CRM-Assistant
2) Create .env in the project root

Create a file named .env beside docker-compose.yml:

OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=your_model_here
3) Build and run
docker compose up --build
4) Open in browser

Frontend: http://localhost:5173

Backend API docs (Swagger): http://localhost:8000/docs

5) Stop containers

Press Ctrl + C, then:

docker compose down
Option B: Run Locally (No Docker)
Backend (FastAPI)
cd backend
python -m venv .venv

Activate venv:

Windows PowerShell

.venv\Scripts\Activate.ps1

Mac/Linux

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Set environment variables:

Windows PowerShell

$env:OPENAI_API_KEY="your_openai_key_here"
$env:OPENAI_MODEL="your_model_here"

Mac/Linux

export OPENAI_API_KEY="your_openai_key_here"
export OPENAI_MODEL="your_model_here"

Run the backend:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Backend will be available at:

http://localhost:8000

http://localhost:8000/docs

Frontend (Vite)

Open a new terminal:

cd frontend
npm install

Set API base URL:

Windows PowerShell

$env:VITE_API_BASE_URL="http://127.0.0.1:8000"

Mac/Linux

export VITE_API_BASE_URL="http://127.0.0.1:8000"

Run frontend:

npm run dev

Frontend will be available at:

http://localhost:5173

Troubleshooting
Docker ports already in use

Stop other services using the ports:

8000 (backend)

5173 (frontend)

Then rerun:

docker compose up --build
Backend cannot call OpenAI

Make sure .env exists in the project root and has:

OPENAI_API_KEY

OPENAI_MODEL

Frontend cannot reach backend

Ensure backend is running at:

http://127.0.0.1:8000

If using local dev, confirm VITE_API_BASE_URL is set before running npm run dev.
