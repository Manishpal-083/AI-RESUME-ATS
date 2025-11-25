import os

# Path to tesseract executable (only needed on Windows if not on PATH)
TESSERACT_CMD = os.getenv("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")

# OpenAI API Key (if you use OpenAI for suggestions)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Models save paths
ATS_MODEL_PATH = "models/ats_classifier.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

