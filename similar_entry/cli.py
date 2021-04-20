from __future__ import annotations

from typing import Optional
from pathlib import Path
from . import similar, text_converter
import multiprocessing as mp
import itertools

_ext_converter_mappings = (
    (("md", "mdx", "markdown"), text_converter.markdown),
    (("html", "htm"), text_converter.html),
)


def _detect_converter(ext: str):
    ext = ext.lower().replace(".", "")
    for (exts, converter) in _ext_converter_mappings:
        if ext in exts:
            return converter
    return text_converter.text


def _file_to_text(
    file: str, converter: Optional[text_converter.Converter] = None
) -> str:
    path = Path(file)
    source = path.read_text(encoding="utf-8")
    if converter:
        converted = converter(source)
    else:
        converted = _detect_converter(path.suffix)(source)
    return converted


def _file_to_text_tuple(t):
    return _file_to_text(t[0], t[1])


def files_to_texts(
    files: list[str], converter: Optional[text_converter.Converter] = None
) -> list[str]:
    pool = mp.Pool(mp.cpu_count())
    texts: list[str] = pool.map(
        _file_to_text_tuple, zip(files, itertools.cycle([converter]))
    )
    return texts


def _top_k_tuple(t):
    return similar.top_k(t[0], t[1])


def similar_entry(files: list[str], top_k=3):
    texts = files_to_texts(files)
    vectors = similar.tfidf_vectorize(texts)
    pool = mp.Pool(mp.cpu_count())
    return pool.map(_top_k_tuple, zip(vectors, itertools.cycle(vectors)))
