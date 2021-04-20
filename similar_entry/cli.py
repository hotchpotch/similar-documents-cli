from typing import List, Optional, Callable
from pathlib import Path
from similar_entry import text_converter

_ext_converter_mappings = (
    (("md", "mdx", "markdown"), text_converter.markdown),
    (("html", "htm"), text_converter.html),
)


def _detect_converter(ext: str):
    ext = ext.lower()
    for (exts, converter) in _ext_converter_mappings:
        if ext in exts:
            return converter
    return text_converter.text


def files_to_texts(files: List[str], converter: Optional[Callable[[str], str]] = None):
    texts_dict = {}
    for file in files:
        path = Path(file)
        source = path.read_text(encoding="utf-8")
        if converter:
            converted = converter(source)
        else:
            converted = _detect_converter(path.suffix)(source)
        texts_dict[file] = converted
    return texts_dict
