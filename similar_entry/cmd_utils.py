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


def _top_k_tuple(t: tuple(csr_matrix, csr_matrix, int)):
    return similar.top_k(*t)


def similar_vectors_top_k(vectors: list[csr_matrix], k=3):
    pool = mp.Pool(mp.cpu_count())
    return pool.map(
        _top_k_tuple, zip(vectors, itertools.cycle([vectors]), itertools.cycle([k]))
    )


def assign_top_k(files: list[str], top_ks: list[list[tuple[int, float]]]):
    file_dict: dict[str, tuple[str, float]] = {}
    for (file, top_k) in zip(files, top_ks):
        file_dict[file] = [(files[index], score) for (index, score) in top_k]
    return file_dict
