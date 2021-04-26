from ..cmd_utils import files_to_texts, similar_vectors_top_k, assign_top_k
from ..similar import tfidf_vectorize
from ..tokenizer import japanese

from pathlib import Path
import os

fixtures_path = Path(os.path.dirname(__file__)).joinpath("fixtures")


def test_integration():
    files = [str(path) for path in fixtures_path.glob("*")]
    texts = files_to_texts(files)
    vectors = tfidf_vectorize(texts, tokenizer=japanese)
    top_ks = similar_vectors_top_k(vectors, k=2)
    assigned = assign_top_k(files, top_ks)
    assert len(list(assigned.keys())) == 5
    assert len(list(assigned.values())[0]) == 2  # size of k
