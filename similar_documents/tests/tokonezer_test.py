from ..tokenizer import japanese


def test_japanese():
    assert japanese("こんにちは、かわいい犬ですね。") == ["こんにちは", "かわいい", "犬"]
    assert japanese("猫と犬") == ["猫", "犬"]


def test_japanese_numeric():
    assert japanese("こんにちは、100か千ですね。") == ["こんにちは"]
