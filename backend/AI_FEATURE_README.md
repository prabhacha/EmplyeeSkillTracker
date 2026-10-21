# Employee Skill Tracker - AI Skill Recommendations

## What was added

- New `ai_recommendations` Django app.
- `POST /api/ai/recommend/<employee_id>/`
- Uses existing `EmployeeSkill`, `EmployeeCertification`, and `Training` data.
- Python calculates deterministic skill gaps first.
- OpenAI Responses API generates structured recommendations and a 4-6 week roadmap.
- Target role can be passed in the request; otherwise the employee's `designation` is used.
- Initial role catalogue includes Python Full Stack Developer, Senior React Developer, and Frontend Developer.
- No new database migration is required for this first version.

## Install

From the backend folder:

```powershell
pip install openai
```

Or:

```powershell
pip install -r requirements-ai.txt
```

## Configure API key

Set these environment variables in the terminal before starting Django:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
$env:OPENAI_MODEL="gpt-5-mini"
```

Do not put the API key in React code or commit it to Git.

## Run

```powershell
python manage.py runserver
```

## API

Endpoint:

```text
POST http://127.0.0.1:8000/api/ai/recommend/<employee_id>/
```

Example body:

```json
{
  "target_role": "Python Full Stack Developer"
}
```

The endpoint requires the existing JWT authentication and Admin/Manager permission.

## Example response shape

```json
{
  "employee": {
    "id": 1,
    "employee_id": "EMP001",
    "name": "Rahul",
    "department": "IT",
    "designation": "Frontend Developer"
  },
  "target_role": "Python Full Stack Developer",
  "current_skills": [],
  "skill_gaps": [],
  "certifications": [],
  "training_catalogue": [],
  "recommendations": [
    {
      "skill": "Django REST Framework",
      "priority": "High",
      "reason": "Useful for building production REST APIs with Django.",
      "learning_steps": [
        "Serializers",
        "ViewSets",
        "Authentication and permissions"
      ]
    }
  ],
  "learning_roadmap": [
    {
      "week": "Week 1",
      "focus": "Django REST Framework",
      "skills": ["Django REST Framework"],
      "outcome": "Build a small authenticated REST API"
    }
  ]
}
```

## Important

The OpenAI key must stay on the Django server. React calls Django; Django calls OpenAI.

The OpenAI integration uses the Responses API and structured JSON output. OpenAI's current documentation recommends the Responses API for new integrations and supports JSON Schema through `text.format`. See the official OpenAI developer quickstart for the current SDK/API syntax.
