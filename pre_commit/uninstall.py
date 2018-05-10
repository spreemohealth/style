#!/usr/bin/env python3
from os import (
    path,
    remove
)
import shutil

# remove pre-commit hook
try:
    remove(
        path.abspath(
            path.join(path.dirname(path.dirname(__file__)), "pre-commit")
        )
    )
except FileNotFoundError:
    pass

# remove pre_commit subdirectory
shutil.rmtree(
    path.abspath(path.join(path.dirname(__file__))),
    ignore_errors=True
)

print(
    "\nThe pre-commit hook was successfully uninstalled."
)
