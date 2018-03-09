#!/usr/bin/env bash
get_staged_files () {
    if git rev-parse --verify HEAD &> /dev/null; then
        AGAINST=HEAD
    else
        AGAINST=4b825dc642cb6eb9a060e54bf8d69288fbee4904
    fi

    FILES=$(git diff --cached --name-only $AGAINST | grep -E "$1")
    echo $FILES
}

lint () {
    # temporary location
    TMP="/tmp"

    # make temporary file name for staged file
    TMP_FILE_NAME="$TMP/style/$2"

    # ensure that dirname of temporary file exists
    TMP_FILE_DIR=$(dirname $TMP_FILE_NAME)
    mkdir -p "$TMP_FILE_DIR"

    # write staged version to temporary file
    git show ":$2" > "$TMP_FILE_NAME"

    # make temp file for linter's output
    LINT_OUTPUT=$(mktemp)

    # run linter and write to temporary linter's output file
    case "$1" in

        "py")
            flake8 "$TMP_FILE_NAME" > "$LINT_OUTPUT";;

        "r")
            R --slave -e "lintr::lint('$TMP_FILE_NAME')" > "$LINT_OUTPUT";;
    esac

    # display linter's output file
    cat "$LINT_OUTPUT"

    # form return code for this function
    if [ -s "$LINT_OUTPUT" ]; then
        OUTPUT=1
    else
        OUTPUT=0
    fi

    # clean
    rm "$LINT_OUTPUT"
    rm -rf "$TMP_FILE_DIR"

    return $OUTPUT
}