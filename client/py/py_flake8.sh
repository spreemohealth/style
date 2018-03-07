#!/usr/bin/env bash
source .git/hooks/style/get_git_diff_index.sh

REGEX='\.py$'

FILES=$(get_git_diff_index $REGEX)

if [[ -n $FILES ]]; then
    python .git/hooks/style/py_flake8.py $FILES
fi