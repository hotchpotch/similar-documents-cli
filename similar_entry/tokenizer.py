
from typing import List


def _createMecabTokenizer(target_fetures = ['名詞', '形容詞', '感動詞']):
    from fugashi import Tagger
    tagger = Tagger('-Owakati')
    def tokenizer(text: str) -> List[str]:
        tokens = []
        for word in tagger(text):
            if word.feature[0] in target_fetures:
                tokens.append(word.surface)
        return tokens
    return tokenizer

mecab = _createMecabTokenizer()