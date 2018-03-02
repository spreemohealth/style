#!/usr/bin/env bash

# install flake8
pip install flake8

# add the git pre-commit hook
flake8 --install-hook git

# force flake8 to be strict: commits are not allowed
# if flake8 has non-zero exit status
git config --bool flake8.strict true

