# Chainsaw
A lightweight wrapper around git subtrees that lets you work with many subtrees at once

# Installation
```bash
pip install git-chainsaw
```

# Dependencies
- git v1.7.11 or above
- make sure the `git` command is recognized wherever you plan to run this
- python3 + pip

# Usage
Example chainsaw.json
```json
[
    {
        "prefix": "bingo",
        "remote": "https://github.com/nasa/bingo.git",
        "branch": "master"
    },
    {
        "prefix": "trick",
        "remote": "https://github.com/nasa/trick.git",
        "branch": "master"
    }
]
```

Adding subtrees:
```bash
# From a predefined chainsaw.json file
chainsaw add --all [--squash]

# From scratch (Subtrees will be added to chainsaw.json)
chainsaw add bingo https://github.com/nasa/bingo.git master [--squash]
```

List subtrees:
```bash
chainsaw ls
```
