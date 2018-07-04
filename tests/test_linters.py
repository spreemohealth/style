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

    def test_zero_exit_code(self):
        try:
            # write a bad markdown file
            file_path = path.join(self.cwd, "test.md")
            w = Writer(file_path)
            w.write("# Section")
            w.write("")
            w.write("This is ok!")

            # instantiate the linter (sink STDOUT in testing)
            f = StringIO()
            with redirect_stdout(f):
                return_value = MarkdownLinter().lint([w.path])

            self.assertEqual(return_value, 0)

        except Exception:
            raise

        finally:
            # clean up
            w.delete()

    def test_non_zero_exit_code(self):
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

    def test_linter_config_file(self):
        try:
            # write the `markdownlint.json` config file instructing to
            # except "MD022/blanks-around-headers"
            config_file_path = path.join(self.cwd, ".markdownlint.json")
            w_conf = Writer(config_file_path)
            w_conf.write("{")
            w_conf.write('    "MD022": false')
            w_conf.write("}")

            # write a bad markdown file
            file_path = path.join(self.cwd, "test.md")
            w = Writer(file_path)
            w.write("# Section")
            w.write("Missing a blank line after header.")

            # instantiate the linter (sink STDOUT in testing)
            f = StringIO()
            with redirect_stdout(f):
                return_value = (
                    MarkdownLinter(config_path=w_conf.path).lint([w.path])
                )

            # return value will be 0 if MD022 is correctly ignored
            self.assertEqual(return_value, 0)

        except Exception:
            raise

        finally:
            # clean up
            w_conf.delete()
            w.delete()


class TestPythonLinter(TestCase):

    cwd = getcwd()

    def test_zero_exit_code(self):
        try:
            # write a bad python file
            file_path = path.join(self.cwd, "test.py")
            w = Writer(file_path)
            w.write("# This is ok")
            w.write("a = 3")
            w.write("b = 4")
            w.write("a < 4")

            # instantiate the linter (sink STDOUT in testing)
            f = StringIO()
            with redirect_stdout(f):
                return_value = PythonLinter().lint([w.path])

            self.assertEqual(return_value, 0)

        except Exception:
            raise

        finally:
            # clean up
            w.delete()

    def test_non_zero_exit_code(self):
        try:
            # write a bad python file
            file_path = path.join(self.cwd, "test.py")
            w = Writer(file_path)
            w.write("# No space around =")
            w.write("foo=1")

            # instantiate the linter (sink STDOUT in testing)
            f = StringIO()
            with redirect_stdout(f):
                return_value = PythonLinter().lint([w.path])

            self.assertEqual(return_value, 1)

        except Exception:
            raise

        finally:
            # clean up
            w.delete()

    def test_linter_config_file(self):
        try:
            # write the `.flake8` config file instructing to
            # except "E225"
            config_file_path = path.join(self.cwd, ".flake8")
            w_conf = Writer(config_file_path)
            w_conf.write("[flake8]")
            w_conf.write("ignore = E225")

            # write a bad python file
            file_path = path.join(self.cwd, "test.py")
            w = Writer(file_path)
            w.write("# No space around =")
            w.write("foo=1")

            # instantiate the linter (sink STDOUT in testing)
            f = StringIO()
            with redirect_stdout(f):
                return_value = (
                    PythonLinter(config_path=w_conf.path).lint([w.path])
                )

            # return value will be 0 if E225 is correctly ignored
            self.assertEqual(return_value, 0)

        except Exception:
            raise

        finally:
            # clean up
            w_conf.delete()
            w.delete()


class TestRLinter(TestCase):

    cwd = getcwd()

    def test_zero_exit_code(self):
        try:
            # write a bad R file
            file_path = path.join(self.cwd, "test.R")
            w = Writer(file_path)
            w.write("# This is ok")
            w.write("a <- 3")
            w.write("b <- 4")
            w.write("a < 4")

            # instantiate the linter (sink STDOUT in testing)
            f = StringIO()
            with redirect_stdout(f):
                return_value = RLinter().lint([w.path])

            self.assertEqual(return_value, 0)

        except Exception:
            raise

        finally:
            # clean up
            w.delete()

    def test_non_zero_exit_code(self):
        try:
            # write a bad R file
            file_path = path.join(self.cwd, "test.R")
            w = Writer(file_path)
            w.write("# Use = instead of <-")
            w.write("bar = 0")

            # instantiate the linter (sink STDOUT in testing)
            f = StringIO()
            with redirect_stdout(f):
                return_value = RLinter().lint([w.path])

            self.assertEqual(return_value, 1)

        except Exception:
            raise

        finally:
            # clean up
            w.delete()

    def test_linter_config_file(self):
        try:
            # write the `.lintr` config file instructing to
            # deactivate the "assignment_linter"
            config_file_path = path.join(self.cwd, ".lintr")
            w_conf = Writer(config_file_path)
            w_conf.write("linters: with_defaults(assignment_linter = NULL)")

            # write a bad R file
            file_path = path.join(self.cwd, "test.R")
            w = Writer(file_path)
            w.write("# Use = instead of <-")
            w.write("bar = 0")

            # instantiate the linter
            f = StringIO()
            with redirect_stdout(f):
                return_value = (
                    RLinter(config_path=w_conf.path).lint([w.path])
                )

            # return value will be 0 if the "assignment_linter" is correctly
            # deactivated
            self.assertEqual(return_value, 0)

        except Exception:
            raise

        finally:
            # clean up
            w_conf.delete()
            w.delete()


if __name__ == "__main__":
    main()
