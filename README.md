# similar-documents

Generates similarity document scores from cli. Useful when combined with static site generators.

```
$ similar-documents -t japanese -k 2 ~/Dropbox/secon-sites/data/markdowns/recently/*.md | jq . | head -20
{
  "/home/yu1/Dropbox/secon-sites/data/markdowns/recently/2021-04-01.md": [
    [
      "/home/yu1/Dropbox/secon-sites/data/markdowns/recently/2021-04-26.md",
      0.3123780045484529
    ],
    [
      "/home/yu1/Dropbox/secon-sites/data/markdowns/recently/2021-04-03.md",
      0.17384380113610887
    ]
  ],
  "/home/yu1/Dropbox/secon-sites/data/markdowns/recently/2021-04-02.md": [
    [
      "/home/yu1/Dropbox/secon-sites/data/markdowns/recently/2021-04-26.md",
      0.10715535963136594
    ],
    [
      "/home/yu1/Dropbox/secon-sites/data/markdowns/recently/2021-04-23.md",
      0.09411751563901728
    ]
```

## Installation

```
pip install similar-documents
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
