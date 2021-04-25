from __future__ import annotations


def _createJapaneseTokenizer(target_features=["名詞", "形容詞", "感動詞"], ignore_numeric=True):
    from fugashi import Tagger

    tagger = Tagger("-Owakati")

    def tokenizer(text: str) -> list[str]:
        tokens = []
        for word in tagger(text):
            if word.feature[0] in target_features:
                if not (ignore_numeric and word.feature[1] == "数詞"):
                    tokens.append(word.surface)
        return tokens

    return tokenizer


japanese = _createJapaneseTokenizer()