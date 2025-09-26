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



### Image References
<img width="1799" height="852" alt="Screenshot from 2025-09-26 16-23-22" src="https://github.com/user-attachments/assets/2d8d603e-74ba-4cbe-b1cf-d3d3a32b378a" />


<img width="1848" height="1012" alt="Screenshot from 2025-09-26 16-17-29" src="https://github.com/user-attachments/assets/c0e7366c-ee9f-4610-881e-471be70bd7c8" />


<img width="1848" height="1012" alt="Screenshot from 2025-09-26 16-15-36" src="https://github.com/user-attachments/assets/fa53e218-31b2-4efa-b51a-2489e598af9d" />


## Authored By:
Immaculate Nayiga




