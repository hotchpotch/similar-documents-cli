from similar_entry.similar import tfidf_vectorize, top_k

def test_similar():
    texts = ['hello world!', 'hello similar!', 'hi, hello', 'similar', 'hi']
    vectors = tfidf_vectorize(texts)
    results = list(top_k(vectors[4], vectors)) # 4 is hi
    assert results[0][0] == 2 # 2 is 'hi hello'
    results = list(top_k(vectors[3], vectors))
    assert results[0][0] == 1


