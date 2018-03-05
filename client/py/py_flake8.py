#!/usr/bin/env python
"""
This is just the pre-commit git hook that flake8 would install by default.
The only difference is the enforcement of `strict=True` and `lazy=False`.
"""
import sys

from flake8.main import git

sys.exit(
    git.hook(
        strict=True,
        lazy=False
    )
)
