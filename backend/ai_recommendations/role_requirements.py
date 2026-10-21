# Initial deterministic skill catalogue for the project.
# Add more roles as your application grows. The AI is still used to
# prioritize gaps and create the personalized learning roadmap.

ROLE_REQUIRED_SKILLS = {
    "python full stack developer": [
        "Python",
        "Django",
        "Django REST Framework",
        "REST API",
        "SQL",
        "React",
        "Git",
        "Docker",
    ],
    "senior react developer": [
        "React",
        "JavaScript",
        "TypeScript",
        "HTML",
        "CSS",
        "Redux",
        "REST API",
        "Jest",
        "Git",
    ],
    "frontend developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Git",
        "REST API",
    ],
}


def get_required_skills(target_role):
    key = target_role.strip().lower()
    return ROLE_REQUIRED_SKILLS.get(key, [])
