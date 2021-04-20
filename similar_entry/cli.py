from typing import Dict, List, Optional, Callable, Tuple
from pathlib import Path
from similar_entry import similar, text_converter
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
    files: List[str], converter: Optional[text_converter.Converter] = None
) -> List[str]:
    pool = mp.Pool(mp.cpu_count())
    texts: List[str] = pool.map(
        _file_to_text_tuple, zip(files, itertools.cycle([converter]))
    )
    return texts


def _top_k_tuple(t):
    return similar.top_k(t[0], t[1])


if __name__ == "__main__":
    import os

    files = list(
        (
            Path(os.getenv("HOME"))
            .joinpath("Dropbox/secon-sites/data/markdowns/")
            .glob("**/*.md")
        )
    )
    print("read")
    texts = files_to_texts(files)
    print("vector")
    vectors = similar.tfidf_vectorize(texts)
    print("cos")
    results = {}
    pool = mp.Pool(mp.cpu_count())
    top_ks = pool.map(_top_k_tuple, zip(vectors, itertools.cycle(vectors)))
    # for (i, vect) in enumerate(vectors):
    #     # これも並列化できる
    #     k = similar.top_k(vect, vectors)
    #     k_files = [(str(files[index]), score) for (index, score) in k]
    #     results[str(files[i])] = k_files
    print(repr(len(top_ks)))
