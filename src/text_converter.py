
from markdown import Markdown
from bs4 import BeautifulSoup

def _createMarkdownToText():
    md = Markdown()
    def md2text(source: str) -> str:
        body = md.convert(source)
        text = html(body)
        # meta = md.Meta
        return text
    return md2text

markdown = _createMarkdownToText()

def html(source: str) -> str:
    return ''.join(BeautifulSoup(source).findAll(text=True)).strip()

def text(source: str) -> str:
    return source.strip()