#!/bin/sh
#
# This is a modified version of https://gist.github.com/wookietreiber/afdb946625c6090f96012ee1da316a73#file-git-hook-lintr-r
#
if git rev-parse --verify HEAD &> /dev/null ; then
    against=HEAD
else
    against=4b825dc642cb6eb9a060e54bf8d69288fbee4904
fi

files=$(git diff-index --cached --name-only $against | grep -E '\.[rR]$')

if [[ -n $files ]] ; then
    if ! command -v Rscript &> /dev/null ; then
        echo "Commit aborted: something is wrong with the Rscript command." >&2
        exit 1
    fi

    if ! Rscript --vanilla -e 'library(lintr)' &> /dev/null ; then
        echo "Commit aborted: please install the lintr package in R." >&2
        exit 1
    fi
fi

Rscript --vanilla .git/hooks/r_lintr.R $files || exit 1
