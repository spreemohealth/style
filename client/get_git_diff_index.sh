#!/usr/bin/env bash
get_git_diff_index () {
    if git rev-parse --verify HEAD &> /dev/null; then
        AGAINST=HEAD
    else
        AGAINST=4b825dc642cb6eb9a060e54bf8d69288fbee4904
    fi

    FILES=$(git diff-index --cached --name-only $AGAINST | grep -E "$1")

    echo $FILES
}