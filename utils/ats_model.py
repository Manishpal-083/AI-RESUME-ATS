import os
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "ats_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")


def train_ats_model(df: pd.DataFrame):
    """
    Train a simple ATS regression model on columns:
    - resume_text
    - jd_text
    - score (0–100)
    """
    os.makedirs(MODEL_DIR, exist_ok=True)

    # keep only needed cols
    df = df.dropna(subset=["resume_text", "jd_text", "score"])
    resumes = df["resume_text"].astype(str).tolist()
    jds = df["jd_text"].astype(str).tolist()
    scores = df["score"].astype(float).tolist()

    combined_texts = [r + " " + j for r, j in zip(resumes, jds)]

    vectorizer = TfidfVectorizer(max_features=8000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(combined_texts)
    y = np.array(scores)

    model = LinearRegression()
    model.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    print("[SUCCESS] ATS model + vectorizer saved in /models")
    return model


def predict_ats_score(resume_text: str, jd_text: str) -> float:
    """
    Load trained ATS model + vectorizer and predict score between 0 and 100.
    """
    if not (os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH)):
        raise FileNotFoundError("ATS model not trained. Train it first.")

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    combined = (resume_text or "") + " " + (jd_text or "")
    X = vectorizer.transform([combined])
    pred = float(model.predict(X)[0])
    # clamp 0–100
    return max(0.0, min(100.0, pred))
