#!/usr/bin/env python

from pathlib import Path
import sys
import plac

lib = Path(__file__).parent.parent.joinpath("similar_documents")
if lib.exists():

    sys.path.append(str(lib.parent))

from similar_documents import cli

if __name__ == "__main__":
    plac.call(cli)
