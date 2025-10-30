# Perio Read (beta)

Local dev + Docker setup for frontend (React + Vite) and backend (FastAPI).
Ports:
- Backend: http://localhost:8000
- Frontend (static via nginx): http://localhost:3000

Quick local:
- Frontend dev: cd frontend && npm run dev
- Backend dev: (cd backend && uvicorn main:app --reload)

Docker:
- docker compose up --build

