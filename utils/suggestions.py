def generate_suggestions(resume_text, jd_text, resume_skills, jd_skills):
    suggestions = []

    missing = list(set(jd_skills) - set(resume_skills))

    # 1. Missing skills
    for skill in missing:
        suggestions.append(f"Add '{skill}' to your resume to match the job description better.")

    # 2. Resume too short?
    if len(resume_text.split()) < 150:
        suggestions.append("Your resume seems short. Add more achievements, project details, and responsibilities.")

    # 3. No projects?
    if "project" not in resume_text.lower():
        suggestions.append("Mention at least 1-2 strong projects with clear outcomes.")

    # 4. No numbers?
    if "%" not in resume_text and "increased" not in resume_text.lower():
        suggestions.append("Add numbers to quantify your impact (e.g., 20% improvement, 5k+ users).")

    # 5. No GitHub?
    if "github" not in resume_text.lower():
        suggestions.append("Include your GitHub link to increase ATS & recruiter trust.")

    # 6. No action verbs?
    action_verbs = ["developed", "built", "designed", "analyzed", "created", "implemented"]
    if not any(v in resume_text.lower() for v in action_verbs):
        suggestions.append("Use strong action verbs like Developed, Implemented, Designed to improve impact.")

    if not suggestions:
        suggestions.append("Your resume looks strong! Only minor improvements needed.")

    return suggestions
