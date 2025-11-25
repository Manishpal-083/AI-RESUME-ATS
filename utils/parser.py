import re
from typing import Dict, List

SECTION_KEYWORDS = {
    "experience": ["experience","work experience","professional experience","employment","projects"],
    "education": ["education","academic","qualifications","degree"],
    "skills": ["skills","technical skills","expertise"],
    "projects": ["projects","personal projects","relevant projects"],
    "summary": ["summary","profile","about","professional summary","objective"]
}

def split_into_sections(text: str):
    # naive section splitter by headings
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    joined = "\n".join(lines)
    sections = {}
    # find headings by uppercase lines or keywords
    headings = []
    for i, line in enumerate(lines):
        low = line.lower()
        for sec, keys in SECTION_KEYWORDS.items():
            for k in keys:
                if low.startswith(k):
                    headings.append((i, sec, line))
    # fallback: if none found, return full text as summary
    if not headings:
        return {"summary": joined}
    # build sections
    headings_sorted = sorted(headings, key=lambda x: x[0])
    for idx, (i, sec, heading_text) in enumerate(headings_sorted):
        start = i+1
        end = len(lines)
        if idx+1 < len(headings_sorted):
            end = headings_sorted[idx+1][0]
        content = "\n".join(lines[start:end]).strip()
        if sec in sections:
            sections[sec] += "\n" + content
        else:
            sections[sec] = content
    return sections

def parse_resume_text(text: str) -> Dict:
    sections = split_into_sections(text)
    # basic outputs
    skills_text = sections.get("skills","")
    return {
        "sections": sections,
        "skills_text": skills_text,
        "full_text": text
    }

