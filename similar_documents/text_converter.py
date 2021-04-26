from __future__ import annotations
from typing import Callable

from markdown import Markdown
from bs4 import BeautifulSoup

TextConverter = Callable[[str], str]


def _createMarkdownToText():
    md = Markdown(extensions=["full_yaml_metadata"])

    def md2text(source: str) -> str:
        body = md.convert(source)
        meta = md.Meta
        text = html(str(body))
        if type(meta) is dict:
            for key in meta.keys():
                if key.upper() == "TITLE" and type(meta[key]) is str:
                    text = f"{meta[key]}\n{text}"
                    break

        return text

    return md2text


markdown = _createMarkdownToText()


def html(source: str) -> str:
    return "".join(
        BeautifulSoup(source, features="html.parser").findAll(text=True)
    ).strip()


def text(source: str) -> str:
    return source.strip()