import json
import os
from datetime import date, timedelta

from certifications.models import EmployeeCertification
from skills.models import EmployeeSkill
from training.models import Training
from .role_requirements import get_required_skills


PROFICIENCY_LEVELS = {
    "Beginner": 1,
    "Intermediate": 2,
    "Advanced": 3,
    "Expert": 4,
}

REQUIRED_PROFICIENCY_LEVEL = 2


def _normalise(value):
    return " ".join(str(value).strip().lower().split())


def calculate_skill_gaps(employee, target_role):
    """
    Deterministic part of the feature.
    We calculate gaps in Python first; the LLM is used for prioritization
    and personalized recommendations, not as the source of truth for the
    employee's database data.
    """
    employee_skills = list(
        EmployeeSkill.objects
        .filter(employee=employee)
        .select_related("skill")
    )

    skill_map = {
        _normalise(item.skill.name): item
        for item in employee_skills
    }

    required_skills = get_required_skills(target_role)

    # For a role not yet present in the local catalogue, the AI can infer
    # requirements. We return an empty deterministic list in that case.
    gaps = []

    for required in required_skills:
        existing = skill_map.get(_normalise(required))

        if existing is None:
            gaps.append({
                "skill": required,
                "gap_type": "Missing",
                "current_proficiency": None,
                "years_of_experience": 0,
            })
            continue

        level = PROFICIENCY_LEVELS.get(existing.proficiency, 0)

        if level < REQUIRED_PROFICIENCY_LEVEL:
            gaps.append({
                "skill": required,
                "gap_type": "Needs improvement",
                "current_proficiency": existing.proficiency,
                "years_of_experience": float(existing.years_of_experience),
            })

    return gaps


def get_employee_context(employee, target_role):
    employee_skills = list(
        EmployeeSkill.objects
        .filter(employee=employee)
        .select_related("skill")
        .order_by("skill__name")
    )

    employee_certifications = list(
        EmployeeCertification.objects
        .filter(employee=employee)
        .select_related("certification")
        .order_by("expiry_date")
    )

    today = date.today()
    expiry_warning_date = today + timedelta(days=90)

    skills = [
        {
            "skill": item.skill.name,
            "category": item.skill.category,
            "proficiency": item.proficiency,
            "years_of_experience": float(item.years_of_experience),
            "last_used": item.last_used.isoformat() if item.last_used else None,
        }
        for item in employee_skills
    ]

    certifications = []
    for item in employee_certifications:
        if item.expiry_date < today:
            status = "Expired"
        elif item.expiry_date <= expiry_warning_date:
            status = "Expires within 90 days"
        else:
            status = "Active"

        certifications.append({
            "name": item.certification.name,
            "issuing_organization": item.certification.issuing_organization,
            "issue_date": item.issue_date.isoformat(),
            "expiry_date": item.expiry_date.isoformat(),
            "status": status,
        })

    gaps = calculate_skill_gaps(employee, target_role)

    # Only send relevant training catalogue entries for deterministic gaps.
    gap_names = {_normalise(item["skill"]) for item in gaps}
    trainings = list(
        Training.objects
        .filter(skill__name__in=[item["skill"] for item in gaps])
        .select_related("skill")
        .order_by("name")
    )

    training_catalogue = [
        {
            "id": training.id,
            "name": training.name,
            "skill": training.skill.name,
            "provider": training.provider,
            "duration": training.duration,
            "training_url": training.training_url,
        }
        for training in trainings
        if _normalise(training.skill.name) in gap_names
    ]

    return {
        "employee": {
            "id": employee.id,
            "employee_id": employee.employee_id,
            "name": employee.name,
            "department": employee.department,
            "designation": employee.designation,
        },
        "target_role": target_role,
        "current_skills": skills,
        "skill_gaps": gaps,
        "certifications": certifications,
        "training_catalogue": training_catalogue,
    }


def generate_ai_recommendations(context):
    """
    Calls the OpenAI Responses API and requests strict JSON output.
    The API key is read from OPENAI_API_KEY and is never sent by React.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured on the Django server."
        )

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "OpenAI Python SDK is not installed. Run: pip install openai"
        ) from exc

    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    schema = {
        "type": "object",
        "properties": {
            "recommendations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "skill": {"type": "string"},
                        "priority": {
                            "type": "string",
                            "enum": ["High", "Medium", "Low"],
                        },
                        "reason": {"type": "string"},
                        "learning_steps": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": [
                        "skill",
                        "priority",
                        "reason",
                        "learning_steps",
                    ],
                    "additionalProperties": False,
                },
            },
            "learning_roadmap": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "week": {"type": "string"},
                        "focus": {"type": "string"},
                        "skills": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "outcome": {"type": "string"},
                    },
                    "required": [
                        "week",
                        "focus",
                        "skills",
                        "outcome",
                    ],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["recommendations", "learning_roadmap"],
        "additionalProperties": False,
    }

    prompt = f"""
You are an employee skill development assistant.

Use ONLY the employee information supplied below. Do not invent
certifications, skills, experience, or training records.

Goal:
Recommend the most useful skills for the employee to move toward
the target role.

Rules:
- Prioritize actual skill gaps.
- If the employee has a skill at Beginner level, it may be recommended
  as "Needs improvement".
- Do not recommend a skill as missing if it is already Advanced or Expert.
- Consider certification expiry when it is relevant.
- Prefer training entries from the supplied training catalogue when useful.
- Return exactly 5 recommendations when possible. If fewer than 5
  meaningful recommendations exist, return only meaningful ones.
- Keep learning steps practical and suitable for a working developer.
- Create a simple 4-6 week roadmap.

Employee context:
{json.dumps(context, indent=2)}
"""

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=model,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "skill_recommendations",
                "strict": True,
                "schema": schema,
            }
        },
        max_output_tokens=2500,
    )

    try:
        return json.loads(response.output_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "The AI returned an invalid structured response."
        ) from exc
