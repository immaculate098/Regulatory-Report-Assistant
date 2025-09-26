## Regulatory Report Assistant (Feyti Medical Group)

Full‑stack app that processes adverse event reports using a Django REST API + spaCy and a React frontend. Includes history, translation, and a severity chart.

### Stack
- Backend: Django REST Framework, SQLite, spaCy (`en_core_web_sm`)
- Frontend: React (CRA), Axios, Chart.js (`react-chartjs-2`)
- Deploy: Render (backend) + Render (frontend)

### Project Structure
```
/backend
  manage.py
  /regulatory_backend
  /reports
  requirements.txt
/frontend (Create React App)
README.md
```

### Backend: Setup & Run (Local)
1. Create venv and install:
```
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```
2. Migrate and run:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 or python manage.py runserver
```

#### API Endpoints
- POST `/process-report`
  - Body: `{ "report": "..." }`
  - Response: `{ id, raw_report, drug, adverse_events, severity, outcome, created_at }`

- GET `/reports`
  - Response: `[{ ...report }, ...]`

- POST `/translate`
  - Body: `{ "outcome": "recovered|ongoing|fatal", "language": "fr|sw" }`
  - Response: `{ outcome, language, translated }`

### Frontend: Setup & Run (Local)
```
cd frontend
npm install
npm start
```
The app expects the backend at `http://localhost:8000`.

### Deployment (Render)
Backend on Render (free web service):
1. Push repository to GitHub.
2. On Render, “New +” → Web Service.
3. Select repo, root: `/backend`.
4. Environment: Python 3.x.
5. Build Command: `pip install -r requirements.txt && python manage.py migrate`
6. Start Command: `gunicorn regulatory_backend.wsgi:application --bind 0.0.0.0:$PORT`
7. Set `ALLOWED_HOSTS` properly or `*` (already set for demo). Save.

Frontend on Render:
- Build: `npm run build`
- Publish directory: `frontend/build`
  - Render Static Site: root `/frontend`, Build Command `npm install && npm run build`, Publish Directory `/build`.
  - Netlify: drag‑and‑drop `frontend/build` or connect repo.

### Deployment links

#### Frontend

https://regulatory-report-assistant-1.onrender.com

#### Backend

https://regulatory-report-assistant.onrender.com

### Authored By:
Immaculate Nayiga







