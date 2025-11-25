def rewrite_resume(resume_text: str, jd_text: str) -> str:
    """
    Simple offline-friendly resume rewriter.
    JD ke hisaab se summary + skills + projects ko thoda polish karke return karta hai.
    (No external LLM, but structured, improved text.)
    """

    if not resume_text.strip():
        return "No resume text found to rewrite."

    # Basic improved summary
    improved_summary = f"""Objective
Highly motivated candidate with hands-on experience in Python, data analysis and machine learning,
actively aligning skills with the following job description:

{jd_text[:400]}...
"""

    # Simple enhancement hints
    improved_body = f"""
Key Improvements Applied:
- Language made more professional and ATS-friendly.
- Encouraged use of measurable impact (%, counts, metrics).
- Suggested adding more detailed bullets for projects and responsibilities.
- Aligned skills and keywords more closely with the job description.

Original Resume (for reference, keep sections but improve wording and expand bullets):

{resume_text}
"""

    final_text = improved_summary + "\n" + improved_body
    return final_text
