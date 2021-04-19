
def _createMecabTokenizer():
    from fugashi import Tagger
    tagger = Tagger('-Owakati')
    def tokenizer(text: str) -> str:
        res = []
        for word in tagger(text):
            if word.feature[0] == "名詞":
                res.append(word.surface)
        return ' '.join(res)
    return tokenizer

mecab = _createMecabTokenizer()