from __future__ import annotations


def _createMecabTokenizer(target_fetures=["名詞", "形容詞", "感動詞"]):
    from fugashi import Tagger

    tagger = Tagger("-Owakati")

    def tokenizer(text: str) -> list[str]:
        tokens = []
        for word in tagger(text):
            if word.feature[0] in target_fetures:
                tokens.append(word.surface)
        return tokens

    return tokenizer


mecab = _createMecabTokenizer()