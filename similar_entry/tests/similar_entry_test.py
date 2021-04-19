from similar_entry.similar import tfidf_vectorize, top_k
from similar_entry.tokenizer import mecab

def test_similar():
    texts = ['hello world!', 'hello similar!', 'hi, hello', 'similar', 'hi']
    vectors = tfidf_vectorize(texts)
    results = list(top_k(vectors[4], vectors)) # 4 is hi
    assert results[0][0] == 2 # 2 is 'hi hello'
    results = list(top_k(vectors[3], vectors))
    assert results[0][0] == 1

def test_similar_with_mecab():
    texts = ['こんにちは、かわいい犬ですね。', '犬とライオン', "猫とライオン"]
    vectors = tfidf_vectorize(texts, mecab)
    results = list(top_k(vectors[0], vectors))
    assert results[0][0] == 1
 

