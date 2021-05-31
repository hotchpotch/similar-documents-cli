from __future__ import annotations

import itertools
import multiprocessing as mp
from pathlib import Path
from typing import Optional

from scipy.sparse.csr import csr_matrix

from . import similar, text_converter

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


def _file_to_text_tuple(t: tuple(str, Optional[text_converter.TextConverter], str)):  # type: ignore
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


def _top_k_tuple(t: tuple(csr_matrix, csr_matrix, int)):  # type: ignore
    return similar.top_k(*t)


def similar_vectors_top_k(vectors: csr_matrix, k=5):
    pool = mp.Pool(mp.cpu_count())
    return pool.map(
        _top_k_tuple, zip(vectors, itertools.cycle([vectors]), itertools.cycle([k]))
    )


def assign_top_k(files: list[str], top_ks: list[list[tuple[int, float]]]):
    file_dict: dict[str, list[tuple[str, float]]] = {}
    for (file, top_k) in zip(files, top_ks):
        scores = [(files[index], score) for (index, score) in top_k]
        file_dict[file] = scores
    return file_dict
