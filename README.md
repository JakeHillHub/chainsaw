# Chainsaw
A lightweight wrapper around git subtrees that lets you work with many subtrees at once

# Installation
```bash
pip install git-chainsaw
```

# Usage
Create a chainsaw.json file in your top level directory

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

Add all subtrees: 
```bash
chainsaw add --all --squash
```

List subtrees:
```bash
chainsaw ls
```
