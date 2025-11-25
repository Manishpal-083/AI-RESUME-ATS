from sentence_transformers import SentenceTransformer, util
import numpy as np
from config import EMBEDDING_MODEL

# initialize model once
_model = None
def get_model(name=EMBEDDING_MODEL):
    global _model
    if _model is None:
        _model = SentenceTransformer(name)
    return _model

def embed_texts(texts):
    model = get_model()
    return model.encode(texts, convert_to_tensor=True)

def similarity_score(text1, text2):
    model = get_model()
    emb1 = model.encode([text1], convert_to_tensor=True)
    emb2 = model.encode([text2], convert_to_tensor=True)
    sim = util.pytorch_cos_sim(emb1, emb2).item()
    return sim
