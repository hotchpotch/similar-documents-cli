from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional, cast, Any

import plac as _plac

from . import assign_top_k, files_to_texts, similar_vectors_top_k, tfidf_vectorize
from . import tokenizer as _tokenizer

plac = cast(Any, _plac)


@plac.opt("output_file", help="Optional: write output file (default STDOUT)", type=Path)
@plac.opt("top_k", help="Number of similar documents", abbrev="k", type=int)
@plac.opt(
    "tokenizer",
    help="tokenizer [japanese] (default None(space splitting))",
    choices=["japanese"],
)
@plac.opt("encoding", help="file encoding(default utf-8)")
@plac.flg("debug", "Show debug messages")
def cli(
    output_file: Optional[Path] = None,
    top_k=5,
    debug=False,
    tokenizer=None,
    encoding="utf-8",
    *_documents: str,
):
    """
    usage: $ similar-documents -o result.json -k 5 -t japanese *.md
           $ similar-documents -h
    """
    if len(_documents) == 0:
        print(cli.__doc__, file=sys.stderr)
        exit(1)

    documents = list(_documents)

    if tokenizer:
        if tokenizer and tokenizer == "japanese":
            tokenizer = _tokenizer.japanese
        else:
            raise Exception(f"tokenizer:{tokenizer} is unknown.")
    if debug:
        print(f"files to texts {len(documents)} documents", file=sys.stderr)
    texts = files_to_texts(documents, encoding=encoding)
    if debug:
        print(f"calc tfidf...", file=sys.stderr)
    vectors = tfidf_vectorize(texts, tokenizer=tokenizer)
    if debug:
        print(f"calc similarity...", file=sys.stderr)
    top_ks = similar_vectors_top_k(vectors, k=top_k)
    if debug:
        print(f"assign similarity score", file=sys.stderr)
    assigned = assign_top_k(documents, top_ks)
    json_body = json.dumps(assigned)
    if output_file:
        if debug:
            print(f"write result to file {str(output_file)}", file=sys.stderr)
        output_file.open("w", encoding=encoding).write(json_body)
    else:
        print(json_body)
