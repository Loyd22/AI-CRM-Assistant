
# backend/Dockerfile
# Purpose: Build and run the FastAPI backend in a container.
# Input: backend source code + requirements.txt
# Output: container that serves FastAPI on port 8000

FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . /app

# Run FastAPI
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]