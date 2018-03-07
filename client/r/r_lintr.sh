#!/usr/bin/env bash
#
# This is a modified version of https://gist.github.com/wookietreiber/afdb946625c6090f96012ee1da316a73#file-git-hook-lintr-r
#
source .git/hooks/style/get_git_diff_index.sh

REGEX='\.[rR]$'

FILES=$(get_git_diff_index $REGEX)

if [[ -n $FILES ]]; then
    Rscript .git/hooks/style/r_lintr.R $FILES || exit 1
fi