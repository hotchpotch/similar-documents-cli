# similar-documents

Generates similarity document scores from cli. Useful when combined with static site generators.

```
$ similar-documents -h
usage: $ similar_documents -o result.json -k 5 -t japanese *.md
       $ similar_documents -h

positional arguments:
  documents             list[str]

optional arguments:
  -h, --help            show this help message and exit
  -o None, --output-file None
                        Optional: write output file (default STDOUT)
  -k 5, --top-k 5       Similar documents number
  -d, --debug           Show debug messages
  -t None, --tokenizer None
                        tokenizer [japanese] (default None(space splitting))
  -e utf-8, --encoding utf-8
                        file encoding(default utf-8)
```

```
$ similar-documents -t japanese -k 2 /data/markdowns/recently/*.md | jq . | head -20
{
  "/data/markdowns/recently/2021-04-01.md": [
    [
      "/data/markdowns/recently/2021-04-26.md",
      0.3123780045484529
    ],
    [
      "/data/markdowns/recently/2021-04-03.md",
      0.17384380113610887
    ]
  ],
  "/data/markdowns/recently/2021-04-02.md": [
    [
      "/data/markdowns/recently/2021-04-26.md",
      0.10715535963136594
    ],
    [
      "/data/markdowns/recently/2021-04-23.md",
      0.09411751563901728
    ]
```

## Installation

```
pip install -U similar-documents
```

### On Docker

```
$ docker build -t similar-doc .
# examples: run on windows
$ docker run -it -v C:\Users\yu1\Dropbox\secon-sites\data:/data/ --rm similar-doc bash -c 'similar-documents -t japanese -k 2 -o /data/result.json `ls /data/markdowns/*/*.md`'
```

## Lisence

MIT

## Author

- Yuichi Tateno
