import os
from config import OPENAI_API_KEY
try:
    import openai
    openai.api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
except Exception:
    openai = None

PROMPT_TEMPLATE = """
You are an expert resume writer and recruiter. Improve the following resume text to better match the job description. Make suggestions, rewrite bullet points to be achievement-oriented (include metrics where possible), and add missing skills. 
Resume: {resume}
JobDescription: {jd}
Return a JSON with keys: "score_explanation", "improvements", "rewritten_resume", "missing_skills" (as a list).
"""

def ask_openai_for_suggestions(resume_text, jd_text, max_tokens=400):
    if openai is None:
        return {"error": "OpenAI not configured. Set OPENAI_API_KEY."}
    prompt = PROMPT_TEMPLATE.format(resume=resume_text, jd=jd_text)
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini", # change if needed or use "gpt-4o" depending on access
        messages=[{"role":"user","content":prompt}],
        max_tokens=max_tokens,
        temperature=0.2
    )
    text = resp["choices"][0]["message"]["content"]
    return {"raw": text}
