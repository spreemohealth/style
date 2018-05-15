#!/usr/bin/env python3
"""
Tests for the `pre_commit.linters` submodule.
"""
from contextlib import redirect_stdout
from io import StringIO
from os import (
    getcwd,
    path
)
from unittest import (
    main,
    TestCase
)

from pre_commit.linters import (
    MarkdownLinter,
    PythonLinter,
    RLinter
)

from tests.util import Writer


class TestMarkdownLinter(TestCase):

    cwd = getcwd()

    def test_exit_code(self):
        try:
            # write a bad markdown file
            file_path = path.join(self.cwd, "test.md")
            w = Writer(file_path)
            w.write("# Section")
            w.write("Missing a blank line after header.")

            # instantiate the linter (sink STDOUT in testing)
            f = StringIO()
            with redirect_stdout(f):
                return_value = MarkdownLinter().lint([w.path])

            self.assertEqual(return_value, 1)

        except Exception:
            raise

        finally:
            # clean up
            w.delete()


class TestPythonLinter(TestCase):

    cwd = getcwd()

    def test_exit_code(self):
        try:
            # write a bad python file
            file_path = path.join(self.cwd, "test.py")
            w = Writer(file_path)
            w.write("# No space around =")
            w.write("foo=1")

            # instantiate the linter
            f = StringIO()
            with redirect_stdout(f):
                return_value = PythonLinter().lint([w.path])

            self.assertEqual(return_value, 1)

        except Exception:
            raise

        finally:
            # clean up
            w.delete()


class TestRLinter(TestCase):

    cwd = getcwd()

    def test_exit_code(self):
        try:
            # write a bad python file
            file_path = path.join(self.cwd, "test.R")
            w = Writer(file_path)
            w.write("# Use = instead of <-")
            w.write("bar = 0")

            # instantiate the linter
            f = StringIO()
            with redirect_stdout(f):
                return_value = RLinter().lint([w.path])

            self.assertEqual(return_value, 1)

        except Exception:
            raise

        finally:
            # clean up
            w.delete()


if __name__ == "__main__":
    main()
