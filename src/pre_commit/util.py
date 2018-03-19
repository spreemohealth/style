#!/usr/bin/env python3
from contextlib import contextmanager
from os import (
    chdir,
    getcwd
)


@contextmanager
def exec_in_dir(_dir):
    """
    A simple context manager to execute operations in a given directory.
    """
    if _dir:
        try:
            cwd = getcwd()
            chdir(_dir)
            yield
        except FileNotFoundError:    # noqa F821
            raise
        finally:
            chdir(cwd)
    else:
        yield
