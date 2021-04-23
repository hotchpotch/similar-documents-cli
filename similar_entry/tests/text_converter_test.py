from ..text_converter import markdown, text, html

from pathlib import Path
import os

fixtures_path = Path(os.path.dirname(__file__)).joinpath("fixtures")


def _read_fixture(filename: str):
    target = fixtures_path.joinpath(filename)
    return target.read_text(encoding="utf-8")


def test_markdown():
    fixture = _read_fixture("markdown.md")
    assert markdown(fixture) == "Hello markdown"


def test_markdown_with_yaml():
    fixture = _read_fixture("markdown_yaml.md")
    assert markdown(fixture) == "Title\nHello markdown with yaml"


def test_html():
    fixture = _read_fixture("1.html")
    assert html(fixture) == "Hello html"


def test_text():
    fixture = _read_fixture("plain.txt")
    assert text(fixture) == "plain text<br />"
