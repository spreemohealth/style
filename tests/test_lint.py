#!/usr/bin/env python3
"""
Tests for the `pre_commit.lint` submodule.
"""
from contextlib import redirect_stdout
from io import StringIO
from os import (
    mkdir,
    path
)
from unittest import (
    main,
    TestCase
)

from pre_commit.git import GitHandle
from pre_commit.lint import Lint
from pre_commit.linters import (
    MarkdownLinter,
    PythonLinter,
    RLinter
)
from tests.util import (
    BasicRepo,
    Writer
)


class TestLint(TestCase):

    def test_get_linters_single(self):
        # test ability to detect single linter
        ell = Lint(
            git_handle=GitHandle(),
            linters=[MarkdownLinter()]
        )
        self.assertEqual(
            sum(map(lambda x: isinstance(x, MarkdownLinter), ell.linters)),
            1
        )

    def test_get_linters_multiple(self):
        # test ability to detect multiple linters
        ell = Lint(
            git_handle=GitHandle(),
            linters=[MarkdownLinter(), PythonLinter(), RLinter()]
        )
        self.assertEqual(
            sum(
                map(
                    lambda x: isinstance(x, MarkdownLinter) or
                    isinstance(x, PythonLinter) or isinstance(x, RLinter),
                    ell.linters
                )
            ),
            3
        )

    def test_lint_single(self):
        # test ability to execute `run` method with single linter
        try:
            # initialize repo
            repo = BasicRepo(bare=False)

            # write a bad markdown file
            test_staged_file = path.join(repo.repo_path, "foo.md")
            w = Writer(test_staged_file)
            w.write("# Bad markdown")
            w.write("There should be an empty line before this!")
            w.write("Also, this is way too long" * 300)

            # stage it
            repo.repo.git.add(test_staged_file)

            # initialize a `GitHandle`
            git_handle = GitHandle(path=repo.repo_path)

            # initialize a `Lint` object
            ell = Lint(git_handle=git_handle, linters=[MarkdownLinter()])

            # execute the main method of the  `Lint` object
            f = StringIO()
            with redirect_stdout(f):
                n_files_with_problems = ell.run()

            self.assertEqual(n_files_with_problems, 1)

        except Exception:
            raise

        finally:
            # clean up
            w.delete()
            repo.delete()

    def test_lint_multiple(self):
        # test ability to execute `run` method with multiple linters
        try:
            # initialize repo
            repo = BasicRepo(bare=False)

            # write a bad markdown file
            test_staged_file = path.join(repo.repo_path, "foo.md")
            w = Writer(test_staged_file)
            w.write("# Bad markdown")
            w.write("There should be an empty line before this!")
            w.write("Also, this is way too long" * 300)

            # write a bad R file
            test_staged_file1 = path.join(repo.repo_path, "bar.R")
            w1 = Writer(test_staged_file1)
            w1.write("# Bad R")
            w1.write("f=function(x) print( 'Hello' )")
            w1.write("a=5")

            # stage it
            repo.repo.git.add([test_staged_file, test_staged_file1])

            # initialize a `GitHandle`
            git_handle = GitHandle(path=repo.repo_path)

            # initialize a `Lint` object
            ell = Lint(
                git_handle=git_handle,
                linters=[MarkdownLinter(), RLinter()]
            )

            # execute the main method of the  `Lint` object
            f = StringIO()
            with redirect_stdout(f):
                n_files_with_problems = ell.run()

            self.assertEqual(n_files_with_problems, 2)

        except Exception:
            raise

        finally:
            # clean up
            w.delete()
            w1.delete()
            repo.delete()

    def test_run(self):
        # test ability to execute `run` method with multiple linters when
        # only a subset of the files are staged;
        # also check that linting works for staged files that live in
        # subdirectories
        try:
            # initialize repo
            repo = BasicRepo(bare=False)

            # write a bad markdown file
            test_staged_file = path.join(repo.repo_path, "foo.md")
            w = Writer(test_staged_file)
            w.write("# Bad markdown")
            w.write("There should be an empty line before this!")
            w.write("Also, this is way too long" * 300)

            # write a bad R file
            test_staged_file1 = path.join(repo.repo_path, "bar.R")
            w1 = Writer(test_staged_file1)
            w1.write("# Bad R")
            w1.write("f=function(x) print( 'Hello' )")
            w1.write("a=5")

            # write a bad Python file
            test_staged_file2 = path.join(repo.repo_path, "foof.py")
            w2 = Writer(test_staged_file2)
            w2.write("# Bad Python")
            w2.write(" a=2")
            w2.write("from os import path")
            w2.write("a==2")

            # write another bad Python in a subdirectory
            subdir = path.join(repo.repo_path, "subdir")
            mkdir(subdir)
            test_staged_file3 = path.join(subdir, "fooffer.py")
            w3 = Writer(test_staged_file3)
            w3.write("# Bad Pyrhon")
            w3.write("# Wrong indentation")
            w3.write("class Foo(object):")
            w3.write("  pass")

            # stage these files
            repo.repo.git.add([
                test_staged_file,
                test_staged_file1,
                test_staged_file2,
                test_staged_file3
            ])

            # write another file which is problematic but not staged!
            test_non_staged_file = path.join(repo.repo_path, "lmao.py")
            w3 = Writer(test_non_staged_file)
            w3.write("# An unnecessary import")
            w3.write("from os import getcwd")
            w3.write("# A test on an undefined variable")
            w3.write("# And missing blank line at the end")
            w3.write("a==3", newline=False)

            # initialize a `GitHandle`
            git_handle = GitHandle(path=repo.repo_path)

            # initialize a `Lint` object
            ell = Lint(
                git_handle=git_handle,
                linters=[MarkdownLinter(), PythonLinter(), RLinter()]
            )

            # execute the main method of the  `Lint` object
            f = StringIO()
            with redirect_stdout(f):
                n_files_with_problems = ell.run()

            self.assertEqual(n_files_with_problems, 4)

        except Exception:
            raise

        finally:
            # clean up
            w.delete()
            w1.delete()
            w2.delete()
            w3.delete()
            repo.delete()


if __name__ == "__main__":
    main()
