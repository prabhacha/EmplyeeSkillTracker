# Employee Skill & Certification Tracker with GenAI

Full-stack starter bundle containing a Django REST Framework backend (including the AI recommendation endpoint) and a React + Vite frontend.

## Features
- Django REST API for employees, skills, certifications, training and reports (backend apps included).
- JWT sign-in through `/api/auth/login/`.
- GenAI skill-gap and learning-plan recommendations through `POST /api/ai/recommend/<employee_id>/`.
- React dashboard UI to sign in, choose an employee ID and target role, and display skill gaps, recommendations and a learning roadmap.

## Prerequisites
- Python compatible with your installed Django version
- Node.js 18+
- OpenAI API key for live GenAI responses

## 1. Start the backend (Windows PowerShell)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-ai.txt
python manage.py migrate
python manage.py createsuperuser
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
$env:OPENAI_MODEL="gpt-5-mini"
python manage.py runserver
```

The included settings currently use SQLite for easy local setup. To use MySQL, update `DATABASES` in `backend/config/settings.py` with your local MySQL database and install the appropriate MySQL driver compatible with your Django/Python version. Do not commit API keys or production secrets.

## 2. Start the frontend
Open a second PowerShell terminal:
```powershell
cd frontend
npm install
npm run dev
```
Open the Vite URL shown in the terminal (usually `http://localhost:5173`). Sign in with an existing Django user that has Admin or Manager permissions, then enter an active employee's database ID and generate recommendations.

Optional frontend API override: create `frontend/.env` with `VITE_API_BASE_URL=http://127.0.0.1:8000/api`.

## Notes
- The frontend uses the login response's `access` or `access_token` field for JWT. Adjust `frontend/src/main.jsx` if your existing login serializer returns a different field name.
- AI recommendations require a valid OpenAI API key, available API quota, and permission to use the selected model. Without these, the endpoint may return an error.
- This is a development starter bundle, not production-hardened. Review secrets, authentication/authorization, database settings, CORS, and dependency versions before deployment.
