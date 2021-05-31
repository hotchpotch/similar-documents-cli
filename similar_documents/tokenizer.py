from __future__ import annotations
from typing import Any, cast


def _createJapaneseTokenizer(target_features=["名詞", "形容詞", "感動詞"], ignore_numeric=True):
    import fugashi

    Tagger = cast(Any, fugashi).Tagger
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