import spacy
import re
from collections import Counter
from typing import List, Dict
import pkg_resources
import os

# load spaCy model (make sure to download 'en_core_web_sm' or bigger)
try:
    nlp = spacy.load("en_core_web_sm")
except:
    # fallback: user must run: python -m spacy download en_core_web_sm
    nlp = None

# curated skill list (start) — extend with industry lists
BASE_SKILLS = [
    "python","java","c++","sql","nosql","tensorflow","pytorch","keras",
    "scikit-learn","pandas","numpy","matplotlib","seaborn","aws","azure",
    "docker","kubernetes","git","nlp","computer vision","cv","react","node.js",
    "javascript","html","css","linux","bash","mlops","data engineering",
    "spark","hadoop","spark","tableau","powerbi"
]

def simple_skill_match(text: str, skill_list: List[str]=None):
    text_low = text.lower()
    skill_list = skill_list or BASE_SKILLS
    found = []
    for skill in skill_list:
        if skill.lower() in text_low:
            found.append(skill)
    return list(set(found))

def nlp_entity_skills(text: str):
    if nlp is None:
        return []
    doc = nlp(text)
    # heuristic: look for noun chunks and PROPN/TECH tokens
    tokens = [t.text for t in doc if t.pos_ in ("PROPN","NOUN","PROPN","X")]
    # filter short tokens
    tokens = [t.lower() for t in tokens if len(t) > 1]
    return list(set(tokens))[:100]

def extract_skills(text: str):
    skills = set(simple_skill_match(text))
    # add obvious technology phrases using regex
    tech_patterns = re.findall(r"(?:\b[A-Za-z\+\#\.]{2,}\b(?:\s(?:/|-)\s)?(?:[A-Za-z\+\#\.]{2,})?)", text)
    for p in tech_patterns:
        if len(p) > 2 and len(p) < 50:
            # filter noise
            lower = p.lower()
            if any(ch.isdigit() or ch.isalpha() for ch in lower):
                skills.add(p.strip())
    # spaCy suggestions
    skills.update(nlp_entity_skills(text))
    return sorted(list(skills))
