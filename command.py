from pathlib import Path
from similar_entry.cli import similar_entry
import os

files = list(
    (
        Path(os.getenv("HOME"))
        .joinpath("Dropbox/secon-sites/data/markdowns/recently/")
        .glob("**/*.md")
    )
)
if __name__ == "__main__":
    top_ks = similar_entry(files)
    print(repr(len(top_ks)))
