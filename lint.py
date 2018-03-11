#!/usr/bin/env python3
import inspect
import re

from os import (
    chdir,
    getcwd,
    listdir,
    makedirs,
    path
)
from subprocess import (
    Popen,
    PIPE
)
from tempfile import TemporaryDirectory

from git import GitHandle


class Lint(object):
    """
    This class implements all linting operations.
    """

    def __init__(self, *args, **kwargs):
        # initialize a git handle
        self.git_handle = GitHandle()

    def get_linters(self):
        """
        Discovers all available linters from the class methods.

        Any method implemented in this class that begins with "lint_" is
        interpreted as a linter.

        Please follow the naming convention "lint_<name_of_language>" if you
        implement additional linters.
        """
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        regex = "lint_.+"
        linters = [m[1] for m in methods if re.search(regex, m[0])]

        return linters

    def run(self):
        """
        Main method that executes all of the available linters.
        """
        # get the root of the project
        root = self.git_handle.get_git_root()

        # get the available linters
        linters = self.get_linters()

        # get staged files
        staged_files = self.git_handle.get_staged_files_paths()

        # create a temporary directory
        tmp_dir = TemporaryDirectory()

        # get the paths of the staged files, relative to the root of the git
        # repository
        staged_files_rel_paths = [
            path.relpath(file, root) for file in staged_files
        ]

        # write the content of the staged files to temporary files
        for rel_path in staged_files_rel_paths:
            # ensure parent directory of a staged file exists inside of
            # `tmp_dir`
            makedirs(
                path.join(tmp_dir.name, path.dirname(rel_path)), exist_ok=True
            )
            # write content of staged file to a temporary file
            with open(path.join(tmp_dir.name, rel_path), "wb") as tmp_file:
                content = self.git_handle.get_staged_file_content(rel_path)
                tmp_file.write(content)

        # get the current directory
        cwd = getcwd()

        # change directory to `tmp_dir` (this is just a trick to ensure that
        # output from the linters is relative to the root of the git
        # repository)
        chdir(tmp_dir.name)

        # initialize a counter to count how many linters return a non-zero
        # exit status
        non_zero_linters = 0
        for linter in linters:
            # run the linters
            non_zero_linters += linter(listdir())

        # change directory to original directory
        chdir(cwd)

        return non_zero_linters

    def lint_py(self, dir_content):
        """
        flake8 linter for Python.
        """
        # get all ".py" files from the list of staged files
        py_files = [file for file in dir_content if file.endswith(".py")]

        # initialize a counter for files with linting problems
        non_zero_exits = 0
        # run flake8 on each ".py" file
        for file in py_files:
            pipe = Popen(
                ["flake8", file],
                stdout=PIPE,
                stderr=PIPE
            )
            out, err = pipe.communicate()

            out = out.decode('utf-8')
            # if the flake8 outputs something, print the message to stdout
            if out:
                print(out)

            # get exit status from flake8
            non_zero_exits += pipe.returncode

        return non_zero_exits

    # def lint_r(self, dir_content):
    #     """
    #     TODO: Add description.
    #     """
    #     pass
