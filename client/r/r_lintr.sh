#!/usr/bin/env bash
#
# This is a modified version of https://gist.github.com/wookietreiber/afdb946625c6090f96012ee1da316a73#file-git-hook-lintr-r
#
if git rev-parse --verify HEAD &> /dev/null; then
    AGAINST=HEAD
else
    AGAINST=4b825dc642cb6eb9a060e54bf8d69288fbee4904
fi

FILES=$(git diff-index --cached --name-only $AGAINST | grep -E '\.[rR]$')

if [[ -n $FILES ]]; then
    Rscript --vanilla .git/hooks/style/r_lintr.R $FILES || exit 1
fi