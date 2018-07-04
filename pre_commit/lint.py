#!/usr/bin/env python3
"""
This module is where all of the linting logic is defined.

Note that you can use the `Linter` convenience class in the
`pre_commit.linters` module to implement additional linters.
"""
from os import (
    makedirs,
    path
)
from tempfile import TemporaryDirectory

from pre_commit.linters import Linter
from pre_commit.util import exec_in_dir


class Lint(object):
    """
    This class implements all linting operations.

    The main method is `run()`, which executes all available linters.
    """

    def __init__(self, git_handle, linters, *args, **kwargs):
        """
        Args:
            git_handle: a `GitHandle` instance for the repository of interest.
            linters: an iterable of `Linter` objects
                (see `pre_commit.linters`).
        """
        # get the input git handle
        self.git_handle = git_handle

        # get the available linters
        self.linters = self._get_linters(linters)

    def _get_linters(self, linters):
        """
        Discovers all available linters.
        """
        linters = [ell for ell in linters if isinstance(ell, Linter)]

        return linters

    def run(self):
        """
        Main method that executes all of the available linters.

        Returns:
            An integer corresponding to the number of staged files with
            linting problems.
        """
        try:
            # get staged files
            staged_files_paths = self.git_handle.get_staged_files_paths()

            # check that paths and file names are ok
            for _path in staged_files_paths:
                self.git_handle._check_path_is_allowed(_path)

            # create a temporary directory
            tmp_dir = TemporaryDirectory()

            # write the content of the staged files to temporary files
            files_in_tmp_dir = []   # list for rel paths of temporary files
            for rel_path in staged_files_paths:
                # ensure parent directory of a staged file exists inside of
                # `tmp_dir`
                makedirs(path.join(
                    tmp_dir.name,
                    path.dirname(rel_path)
                ), exist_ok=True)
                # write content of staged file to a temporary file and
                # collect relative path in the list
                tmp_file_path = path.join(tmp_dir.name, rel_path)
                with open(tmp_file_path, "wb") as tmp_file:
                    content = self.git_handle.get_staged_file_content(rel_path)
                    tmp_file.write(content)
                    files_in_tmp_dir.append(
                        path.relpath(tmp_file_path, tmp_dir.name)
                    )

            # get current directory and change directory to temporary directory
            # (this is to ensure that relative paths are correctly displayed
            # during linting and that linters run on the staged version of the
            # files, which are the ones saved in the temporary files);
            # not changing directory can cause the paths to be interpreted
            # relatively to the git repository root, which can cause the
            # linters to run on the version of the files that is currently
            # in the tree!
            with exec_in_dir(tmp_dir.name):
                # initialize a counter to count how many linters return a
                # non-zero exit status
                non_zero_linters = 0
                for linter in self.linters:
                    # run the linters
                    non_zero_linters += linter.lint(files_in_tmp_dir)

                return non_zero_linters

        except Exception:
            raise

        finally:
            tmp_dir.cleanup()
