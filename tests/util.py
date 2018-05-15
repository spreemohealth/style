#!/usr/bin/env python3
"""
Testing utilities.
"""
from os import (
    getcwd,
    path,
    remove
)
from shutil import rmtree

from git import Repo


class BasicRepo(object):
    def __init__(self, path=path.join(getcwd(), "test_repo"), bare=True):
        self.repo_path = path
        self.repo = Repo.init(self.repo_path, bare=bare)  # noqa

        # set basic git configuration
        self.repo.git.config("user.email", "foo@foo.bar")
        self.repo.git.config("user.name", "Foo")

    def delete(self):
        rmtree(self.repo_path)


class Writer(object):

    def __init__(self, path):
        self.path = path

    def write(self, contents, newline=True):
        if path.isfile(self.path):
            mode = "a"
        else:
            mode = "w"
        with open(self.path, mode) as f:
            if newline:
                contents += "\n"
            f.write(contents)

    def delete(self):
        remove(self.path)
