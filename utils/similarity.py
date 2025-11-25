from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def similarity_score(text1, text2):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([text1, text2])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return float(score)
