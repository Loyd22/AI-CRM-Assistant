AI CRM Assistant

Description:
AI-powered CRM system with ticket and lead management,
including AI-generated summaries, classification,
urgency scoring, and draft replies.


==============================
TECH STACK
==============================

Frontend:
- React
- TypeScript
- Vite

Backend:
- FastAPI
- Uvicorn

AI Integration:
- OpenAI API (LLM-powered ticket/lead analysis)

Database:
- SQLite (default local database)

DevOps / Tooling:
- Docker
- Docker Compose
- GitHub


==============================
RUNNING THE PROJECT
==============================

This project contains:
- Backend  -> FastAPI (Port 8000)
- Frontend -> React + Vite (Port 5173)


--------------------------------
OPTION A: RUN WITH DOCKER
--------------------------------

1) Clone the repository

git clone https://github.com/Loyd22/AI-CRM-Assistant.git
cd AI-CRM-Assistant

2) Create .env file in project root

Create a file named:

.env

Add:

OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=your_model_here

3) Build and start containers

docker compose up --build

4) Access application

Frontend:
http://localhost:5173

Backend Swagger Docs:
http://localhost:8000/docs

5) Stop containers

Press Ctrl + C
Then run:

docker compose down


--------------------------------
OPTION B: RUN LOCALLY (NO DOCKER)
--------------------------------

BACKEND SETUP

cd backend
python -m venv .venv

Activate virtual environment:

Windows:
.venv\Scripts\Activate.ps1

Mac/Linux:
source .venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Set environment variables:

Windows:
$env:OPENAI_API_KEY="your_openai_key_here"
$env:OPENAI_MODEL="your_model_here"

Mac/Linux:
export OPENAI_API_KEY="your_openai_key_here"
export OPENAI_MODEL="your_model_here"

Run backend:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Backend available at:
http://localhost:8000
http://localhost:8000/docs


FRONTEND SETUP

Open new terminal:

cd frontend
npm install

Set API base URL:

Windows:
$env:VITE_API_BASE_URL="http://127.0.0.1:8000"

Mac/Linux:
export VITE_API_BASE_URL="http://127.0.0.1:8000"

Run frontend:
npm run dev

Frontend available at:
http://localhost:5173


==============================
PROJECT STRUCTURE
==============================

AI-CRM-Assistant/
│
├── backend/
├── frontend/
├── docker-compose.yml
├── .env
└── README.md


==============================
TROUBLESHOOTING
==============================

Port already in use:
Make sure ports 8000 and 5173 are not used by other applications.

OpenAI not working:
Ensure .env file exists in project root and contains:
OPENAI_API_KEY
OPENAI_MODEL

Frontend cannot connect:
Confirm backend running at:
http://127.0.0.1:8000
