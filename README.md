File Download/Transfer System based on Index
============================================

[![GitHub license](https://img.shields.io/github/license/peitaosu/indexDown.svg)](https://github.com/peitaosu/indexDown/blob/master/LICENSE)

A File download/transfer system prototype, based on index and use hash to reduce duplicate files.

## Usage
```
> python index.py -h

Usage: index.py [options]

Options:
  -h, --help            show this help message and exit
  -p PATH, --path=PATH  directory path
  -i INDEX, --index=INDEX
                        index file
  -s SOURCE, --source=SOURCE
                        source path
  -t TARGET, --target=TARGET
                        target path
  -c, --create          create index
  -d, --download        download from index
  -r, --reduce          reduce size

# create index
> python index.py -p test -i test.index -c

# download from index
> python index.py -s . -t target -i test.index -d

# reduce size
> python index.py -p test -r
```