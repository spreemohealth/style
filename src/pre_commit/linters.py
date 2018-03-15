#!/usr/bin/env python3
"""
This module defines the `Linter` class, a convenience class that can be used
to wrap linters for different programming languages.

You are free to define linters for additional programming languages here.
"""
from subprocess import (
    Popen,
    PIPE
)


class Linter(object):
    """
    Convenience class to wrap linters for different programming languages.
    """

    # a tuple of one or more file extensions that determines to which files
    # the linter applies to, e.g. ".py" or (".r", ".R").
    extension = None

    def create_subprocess(self, path):
        """
        Create a subprocess to run the desired linter, e.g.
        ```
        pipe = Popen(
            ["flake8", file],
            stdout=PIPE,
            stderr=PIPE,
        )
        return pipe
        ```

        Make sure to set `stdout=PIPE` and `stderr=PIPE` in your
        implementation.
        """
        raise NotImplementedError

    def lint(self, dir_content):
        """
        Main method to perform linting.

        Args:
            dir_content: a list of file paths corresponding to files on which
                to run the linter.

        Returns:
            An integer corresponding to the number of files with the specified
            extension that have linting problems in `dir_content`.
        """
        # initialize a counter for files with linting problems
        non_zero_exits = 0

        # grab all files with the relevant extension from a list of file paths
        if self.extension:
            self.relevant_files = [
                _file for _file in dir_content
                if _file.endswith(self.extension)
            ]

            # run the linter on each file
            for _file in sorted(self.relevant_files):
                pipe = self.create_subprocess(_file)
                out, err = pipe.communicate()

                out = out.decode('utf-8')
                # if the liner outputs something, print the message to stdout
                if out:
                    print(out)

                # get exit status
                non_zero_exits += (1 if out else 0)

        return non_zero_exits


class PythonLinter(Linter):
    """
    A wrapper for "flake8".
    """

    extension = ".py"

    def create_subprocess(self, f):
        pipe = Popen(
            ["flake8", f],
            stdout=PIPE,
            stderr=PIPE,
        )
        return pipe


class RLinter(Linter):
    """
    A wrapper for "lintr".
    """

    extension = (".r", ".R")

    def create_subprocess(self, f):
        pipe = Popen(
            [
                "Rscript", "--slave", "--vanilla",
                "-e", "lintr::lint('%s')" % f
            ],
            stdout=PIPE,
            stderr=PIPE
        )
        return pipe
