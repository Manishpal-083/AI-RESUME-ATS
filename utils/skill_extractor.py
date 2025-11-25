import spacy

# Load lightweight spaCy model
nlp = spacy.load("en_core_web_sm")

# Simple curated skills list (optional)
COMMON_SKILLS = {
    "python", "java", "sql", "html", "css", "javascript", "git",
    "machine learning", "deep learning", "pandas", "numpy",
    "data analysis", "data science", "matplotlib", "excel",
    "communication", "teamwork", "leadership"
}

def extract_skills_advanced(text: str):
    doc = nlp(text.lower())
    skills = set()

    # Extract noun tokens as potential skills
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and len(token.text) >= 3:
            skills.add(token.text)

    # Match curated skills
    for skill in COMMON_SKILLS:
        if skill in text.lower():
            skills.add(skill)

    return sorted(list(skills))
