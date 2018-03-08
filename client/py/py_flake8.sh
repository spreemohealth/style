#!/usr/bin/env bash
source .git/hooks/style/util.sh

REGEX='\.py$'

FILES=$(get_staged_files $REGEX)

ERRORS=0
for FILE in $FILES; do
    lint "py" $FILE
    let ERRORS=ERRORS+$?
done

exit $ERRORS