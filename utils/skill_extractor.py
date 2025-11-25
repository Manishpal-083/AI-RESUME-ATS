# utils/skill_extractor.py
import re
from typing import List, Set, Dict
import spacy
from sentence_transformers import SentenceTransformer, util
from difflib import SequenceMatcher

# load spaCy
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

# lightweight curated skills list (extend this)
CURATED_SKILLS = [
    "python","pandas","numpy","matplotlib","seaborn","scikit-learn","sklearn",
    "sql","excel","aws","azure","gcp","docker","kubernetes","git","html","css",
    "javascript","nlp","spacy","nltk","transformers","pytorch","tensorflow",
    "sentence-transformers","faiss","pdfplumber","pytesseract","pymupdf",
    "data cleaning","data analysis","machine learning","deep learning",
    "streamlit","rest api","api","docker","ci/cd"
]

# normalize curated to lowercase
CURATED_SKILLS = sorted(list(set([s.lower() for s in CURATED_SKILLS])))

# embedding model (shared)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
_model = None
def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model

def fuzzy_match(a: str, b: str):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def clean_text(text: str) -> str:
    text = re.sub(r"[\r\n]+", " ", text)
    text = re.sub(r"[^\w\+\#\-/ ]+", " ", text)
    return text.strip()

def candidate_phrases(text: str) -> List[str]:
    """
    Return noun chunks and capitalized phrases as candidates.
    """
    text = clean_text(text)
    cand = set()
    if nlp:
        doc = nlp(text)
        # noun chunks and compound nouns
        for nc in doc.noun_chunks:
            chunk = nc.text.strip()
            if len(chunk) > 1 and len(chunk.split()) <= 4:
                cand.add(chunk)
        # also take some contiguous proper nouns / tokens that look techy
        tech_tokens = [t.text for t in doc if t.pos_ in ("PROPN","NOUN") and len(t.text) > 1]
        for t in tech_tokens:
            if len(t) <= 30:
                cand.add(t)
    else:
        # fallback: split by comma & slash
        parts = re.split(r"[,\;/\-]", text)
        for p in parts:
            p = p.strip()
            if len(p) > 1 and len(p.split()) <= 4:
                cand.add(p)
    return sorted(list(cand))

def map_to_curated(candidates: List[str]) -> Set[str]:
    """
    Map candidate phrases to curated skills using fuzzy + embedding similarity.
    """
    found = set()
    model = get_embedding_model()
    curated_embeddings = model.encode(CURATED_SKILLS, convert_to_tensor=True)

    for c in candidates:
        c_clean = c.lower().strip()
        # quick substring match
        for sk in CURATED_SKILLS:
            if sk in c_clean or c_clean in sk:
                found.add(sk)
        # fuzzy match
        for sk in CURATED_SKILLS:
            if fuzzy_match(c_clean, sk) > 0.85:
                found.add(sk)
        # embedding similarity check
        try:
            emb = model.encode([c_clean], convert_to_tensor=True)
            sims = util.pytorch_cos_sim(emb, curated_embeddings)[0].cpu().numpy()
            best_idx = int(sims.argmax())
            if sims[best_idx] > 0.65:
                found.add(CURATED_SKILLS[best_idx])
        except Exception:
            pass

    return set(found)

def extract_skills_advanced(text: str) -> List[str]:
    """
    Main entry: returns sorted unique skills (canonical lowercase).
    """
    if not text or len(text.strip()) < 5:
        return []
    text = clean_text(text)
    candidates = candidate_phrases(text)
    mapped = map_to_curated(candidates)
    # also try direct matches from curated list in text
    low = text.lower()
    for sk in CURATED_SKILLS:
        if re.search(r"\b" + re.escape(sk) + r"\b", low):
            mapped.add(sk)
    return sorted(mapped)
