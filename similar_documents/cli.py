from __future__ import annotations
import json
from optparse import Option
import sys
import plac
from pathlib import Path

from . import (
    tokenizer as _tokenizer,
    files_to_texts,
    tfidf_vectorize,
    similar_vectors_top_k,
    assign_top_k,
)


@plac.opt("output_file", help="Optional: write output file (default STDOUT)", type=Path)
@plac.opt("top_k", help="Similar documents number", abbrev="k", type=int)
@plac.opt(
    "tokenizer",
    help="tokenizer [japanese] (default None(space splitting))",
    choices=["japanese"],
)
@plac.opt("encoding", help="file encoding(default utf-8)")
@plac.flg("debug", "Show debug messages")
def cli(
    output_file: Option[Path] = None,
    top_k=5,
    debug=False,
    tokenizer=None,
    encoding="utf-8",
    *documents: list[str],
):
    """similar documents score
    usage: $ similar_documents -o result.json -k 5 -t japanese *.md
           $ similar_documents -h
    """
    if len(documents) == 0:
        print(cli.__doc__, file=sys.stderr)
        exit(1)

    if tokenizer:
        if tokenizer and tokenizer == "japanese":
            tokenizer = _tokenizer.japanese
        else:
            raise f"tokenizer:{tokenizer} is unknown."
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
