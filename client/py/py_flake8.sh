#!/usr/bin/env bash
if git rev-parse --verify HEAD &> /dev/null; then
    AGAINST=HEAD
else
    AGAINST=4b825dc642cb6eb9a060e54bf8d69288fbee4904
fi

files=$(git diff-index --cached --name-only $AGAINST | grep -E '\.py$')

if [[ -n $files ]]; then
    python .git/hooks/style/py_flake8.py $files
fi