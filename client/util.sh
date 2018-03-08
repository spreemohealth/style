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
    # make file name for staged file
    TMP_FILE_NAME="(staged) $2"

    # write staged version to file
    git show ":$2" > "$TMP_FILE_NAME"

    # make temp file for output of linter
    LINT_OUTPUT=$(mktemp)

    # run linter and write to temp file
    case "$1" in

        "py")
            flake8 "$TMP_FILE_NAME" > "$LINT_OUTPUT";;

        "r")
            R --slave -e "lintr::lint('$TMP_FILE_NAME')" > "$LINT_OUTPUT";;
    esac

    # display linter output
    cat "$LINT_OUTPUT"

    # form output
    if [ -s "$LINT_OUTPUT" ]; then
        OUTPUT=1
    else
        OUTPUT=0
    fi

    # clean
    rm "$LINT_OUTPUT"
    rm "$TMP_FILE_NAME"

    return $OUTPUT
}