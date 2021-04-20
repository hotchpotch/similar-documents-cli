from ..tokenizer import mecab


def test_mecab():
    assert mecab("こんにちは、かわいい犬ですね。") == ["こんにちは", "かわいい", "犬"]
    assert mecab("猫と犬") == ["猫", "犬"]
