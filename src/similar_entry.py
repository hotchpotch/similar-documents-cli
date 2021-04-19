import numpy as np
from scipy.sparse.csr import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from typing import Callable, Optional, List, Tuple

def tfidf_vectors(texts: List[str], tokenizer: Optional[Callable[[str], str]]) -> csr_matrix:
    vectorizer = TfidfVectorizer(preprocessor=tokenizer)
    return vectorizer.fit_transform(texts)

def similar_top_k(target: csr_matrix, vectors: csr_matrix, k=3) -> List[Tuple[int, float]]:
    scores = cosine_similarity(target, vectors)[0]
    sort_indexes = scores.argsort()[::-1]
    top_indexes = sort_indexes[:1+k]
    top_scores = scores[top_indexes]
    if abs(top_scores[0] - 1.0) < 0.001:
        # top-1 == texts, delete top
        top_scores = np.delete(top_scores, 0)
        top_indexes = np.delete(top_indexes, 0)
    else:
        top_scores = np.delete(top_scores, k)
        top_indexes = np.delete(top_indexes, k)
    return zip(top_indexes, top_scores)