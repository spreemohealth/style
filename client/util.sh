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
    # create temporary directory
    TMP="$(mktemp -d)"

    # get dirname and basename of staged file
    FILE_DIRNAME="$(dirname $2)"
    FILE_BASENAME="$(basename $2)"

    # make a temporary copy of the staged file in the temporary directory
    mkdir -p "$TMP/$FILE_DIRNAME"
    TMP_FILE="$TMP/$FILE_DIRNAME/$FILE_BASENAME"
    git show ":$2" > "$TMP_FILE"

    # make temporary file for linter's output
    LINT_OUTPUT=$(mktemp)

    # get relative path of the copy of the staged file
    TMP_FILE_REL_PATH="$(realpath $TMP_FILE --relative-to $TMP)"

    # run linter and write to temporary linter's output file
    case "$1" in

        "py")
            flake8 "$TMP_FILE_REL_PATH" > "$LINT_OUTPUT";;

        "r")
            R --slave -e "lintr::lint('$TMP_FILE_REL_PATH')" > "$LINT_OUTPUT";;
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
    rm -rf "$TMP"

    return $OUTPUT
}