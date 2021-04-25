from pathlib import Path
from similar_documents import (
    files_to_texts,
    similar_vectors_top_k,
    text_converter,
    tfidf_vectorize,
    assign_top_k,
    tokenizer,
)

import os
import sys
import json

files = list(
    (
        Path(os.getenv("HOME"))
        .joinpath("Dropbox/secon-sites/data/markdowns/")
        .glob("201*/*/*.md")
    )
)
files.extend(
    list(
        (
            Path(os.getenv("HOME"))
            .joinpath("Dropbox/secon-sites/data/markdowns/")
            .glob("202*/*/*.md")
        )
    )
)
files.extend(
    list(
        (
            Path(os.getenv("HOME"))
            .joinpath("Dropbox/secon-sites/data/markdowns/")
            .glob("recently/*.md")
        )
    )
)
files = [str(f) for f in files]

if __name__ == "__main__":
    # from glob import glob

    # print("text")
    texts = files_to_texts(files)
    # print("vectors")
    vectors = tfidf_vectorize(texts, tokenizer=tokenizer.japanese)
    # print("top_k")
    top_ks = similar_vectors_top_k(vectors, k=3)
    assigned = assign_top_k(files, top_ks)
    print(json.dumps(assigned))
