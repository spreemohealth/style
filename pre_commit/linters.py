#!/usr/bin/env python3
"""
This module defines the `Linter` class, a convenience class that can be used
to wrap linters for different programming languages.

In order to wrap additional linters,

1. subclass from the `Linter` class

2. set the `extension` attribute

3. implement the `linter_process()` method.

You are free to define linters for additional programming languages here.
"""
from subprocess import (
    Popen,
    PIPE,
    STDOUT
)


class Linter(object):
    """
    Convenience class to wrap linters for different programming languages.
    """

    # a tuple of one or more file extensions that determines to which files
    # the linter applies to, e.g. ".md", ".py", or (".r", ".R").
    extension = ""

    def linter_process(self, pth):
        """
        Create a subprocess to run the desired linter, e.g.
        ```
        pipe = Popen(
            ["flake8", pth],
            stdout=PIPE,
            stderr=PIPE,
        )
        return pipe
        ```

        Args:
            - pth: placeholder for a file path

        Returns:
            - a `subprocess.Popen` instance

        Make sure to send the linter's output to stdout!
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
                pipe = self.linter_process(_file)
                out, err = pipe.communicate()

                out = out.decode('utf-8')
                # if the liner outputs something, print the message to stdout
                if out:
                    print(out)

                # get exit status
                non_zero_exits += (1 if out else 0)

        return non_zero_exits


class MarkdownLinter(Linter):
    """
    A wrapper for "markdownlint".
    """

    extension = ".md"

    def linter_process(self, f):
        pipe = Popen(
            ["markdownlint", f],
            stdout=PIPE,
            # redirect stderr to stdout: markdownlint outputs linting
            # information to stderr...
            stderr=STDOUT,
        )
        return pipe


class PythonLinter(Linter):
    """
    A wrapper for "flake8".
    """

    extension = ".py"

    def linter_process(self, f):
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

    def linter_process(self, f):
        pipe = Popen(
            [
                "Rscript", "--slave", "--vanilla",
                "-e", "lintr::lint('%s')" % f
            ],
            stdout=PIPE,
            stderr=PIPE
        )
        return pipe
