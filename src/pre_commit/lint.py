#!/usr/bin/env python3
"""
This module is where all of the linting logic is defined.

Adding linters for additional languages is easy: just add a new
"lint_<language_name>" method to the `Lint` class.

A "lint_<language_name>" method must implement the following behavior:
1) accept a list of file paths as input
2) select only the files that are relevant to <language_name>
   (e.g. by looking at file extensions that relate to <language_name>)
3) produce two pieces of output:
    - send all linting information to stdout (if any issues are detected)
    - return the number of files that have linting issues.

Note that you can use the `Linter` convenience class in the
`src.pre_commit.linters` module to implement additional linters.
"""
import inspect
import re

from os import (
    makedirs,
    path,
    walk
)
from tempfile import TemporaryDirectory

from src.pre_commit.git import GitHandle
from src.pre_commit.linters import (
    PythonLinter,
    RLinter
)


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

        Please follow the naming convention "lint_<language_name>" if you
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
        # get staged files
        staged_files_paths = self.git_handle.get_staged_files_paths()

        # check that paths and file names are ok
        for _path in staged_files_paths:
            self.git_handle.check_staged_file_path_is_allowed(_path)

        # get the root of the project
        root = self.git_handle.get_git_root()

        # get the available linters
        linters = self.get_linters()

        # create a temporary directory
        tmp_dir = TemporaryDirectory()

        # get the paths of the staged files, relative to the root of the git
        # repository
        staged_files_rel_paths = [
            path.relpath(file, root) for file in staged_files_paths
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

        # get all files in the temporary directory
        files_in_tmp_dir = [
            path.relpath(path.join(root, name), tmp_dir.name)
            for root, dirs, files in walk(tmp_dir.name)
            for name in files
        ]

        # initialize a counter to count how many linters return a non-zero
        # exit status
        non_zero_linters = 0
        for linter in linters:
            # run the linters
            non_zero_linters += linter(files_in_tmp_dir)

        return non_zero_linters

    def lint_python(self, dir_content):
        """
        Linter method for Python.
        """
        return PythonLinter(dir_content=dir_content, extension=".py").lint()

    def lint_r(self, dir_content):
        """
        Linter methon for R.
        """
        return RLinter(dir_content=dir_content, extension=(".r", ".R")).lint()
