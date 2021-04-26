from __future__ import annotations

from typing import Optional
from pathlib import Path

from scipy.sparse.csr import csr_matrix
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


def file_to_text(
    file: str,
    converter: Optional[text_converter.TextConverter] = None,
    encoding="utf-8",
) -> str:
    path = Path(file)
    source = path.read_text(encoding=encoding)
    if converter:
        converted = converter(source)
    else:
        converted = _detect_converter(path.suffix)(source)
    return converted


def _file_to_text_tuple(t: tuple(str, Optional[text_converter.TextConverter], str)):
    return file_to_text(t[0], converter=t[1], encoding=t[2])


def files_to_texts(
    files: list[str],
    converter: Optional[text_converter.TextConverter] = None,
    encoding="utf-8",
) -> list[str]:
    pool = mp.Pool(mp.cpu_count())
    texts: list[str] = pool.map(
        _file_to_text_tuple,
        zip(files, itertools.cycle([converter]), itertools.cycle([encoding])),
    )
    return texts


def _top_k_tuple(t: tuple(csr_matrix, csr_matrix, int)):
    return similar.top_k(*t)


def similar_vectors_top_k(vectors: list[csr_matrix], k=5):
    pool = mp.Pool(mp.cpu_count())
    return pool.map(
        _top_k_tuple, zip(vectors, itertools.cycle([vectors]), itertools.cycle([k]))
    )


def assign_top_k(files: list[str], top_ks: list[list[tuple[int, float]]]):
    file_dict: dict[str, tuple[str, float]] = {}
    for (file, top_k) in zip(files, top_ks):
        file_dict[file] = [(files[index], score) for (index, score) in top_k]
    return file_dict
