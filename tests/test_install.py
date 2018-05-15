#!/usr/bin/env python3
"""
Tests for install/uninstall of the git hook.
"""
from configparser import ConfigParser
from os import path
from subprocess import (
    DEVNULL,
    Popen
)
from tempfile import TemporaryDirectory
from unittest import (
    main,
    TestCase
)

from tests.util import BasicRepo


class TestInstall(TestCase):

    def test_default_install(self):
        try:
            # create a temporary directory to host the target repo
            tmp = TemporaryDirectory()

            # create a repo in the temporary directory
            repo = BasicRepo(path=tmp.name, bare=False)

            # run the installer
            pipe = Popen(
                ["python", "install.py", repo.repo_path],
                stdout=DEVNULL
            )
            _ = pipe.communicate()  # noqa

            # test exit code of installer
            self.assertEqual(pipe.returncode, 0)

            # test that the `pre_commit` subdirectory was created in
            # .git/hooks/
            self.assertTrue(
                path.isdir(
                    path.join(repo.repo_path, ".git", "hooks", "pre_commit")
                )
            )

            # test that the `pre-commit` script was created in .git/hooks/
            self.assertTrue(
                path.exists(
                    path.join(repo.repo_path, ".git", "hooks", "pre-commit")
                )
            )

            # test that all options are `True` in `linters.conf`
            parser = ConfigParser()
            parser.read(path.join(
                repo.repo_path, ".git", "hooks", "pre_commit", "linters.conf"
            ))

            self.assertTrue(
                all(map(
                    lambda lang: parser["linters"][lang] == "True",
                    parser["linters"]
                ))
            )

        except Exception:
            raise

        finally:
            tmp.cleanup()

    def test_selective_install(self):
        # this assumes that the installation is succesful as we already
        # check for that in `test_default_install`
        try:
            # create a temporary directory to host the target repo
            tmp = TemporaryDirectory()

            # create a repo in the temporary directory
            repo = BasicRepo(path=tmp.name, bare=False)

            # run the installer with selective installation of linters
            pipe = Popen(
                ["python", "install.py", "-mp", repo.repo_path],
                stdout=DEVNULL
            )
            _ = pipe.communicate()  # noqa

            # test that only the "markdown" and "python" options are `True` in
            # `linters.conf`
            parser = ConfigParser()
            parser.read(path.join(
                repo.repo_path, ".git", "hooks", "pre_commit", "linters.conf"
            ))

            md = parser["linters"]["markdown"]
            py = parser["linters"]["python"]

            # markdown and python on
            self.assertTrue(md)
            self.assertTrue(py)

            # all others off
            others = set(parser["linters"]) - {"markdown", "python"}
            self.assertFalse(
                any([parser["linters"][lang] == "True" for lang in others])
            )

        except Exception:
            raise

        finally:
            tmp.cleanup()


class TestUninstall(TestCase):

    def test_uninstall(self):
        try:
            # install first
            # create a temporary directory to host the target repo
            tmp = TemporaryDirectory()

            # create a bare repo in the temporary directory
            repo = BasicRepo(path=tmp.name, bare=False)

            # run the installer
            pipe_inst = Popen(
                ["python", "install.py", repo.repo_path],
                stdout=DEVNULL
            )
            _ = pipe_inst.communicate()  # noqa

            # uninstall
            pipe_uninst = Popen([
                "python",
                path.join(
                    repo.repo_path,
                    ".git", "hooks", "pre_commit", "uninstall.py"
                )
            ], stdout=DEVNULL)
            _ = pipe_uninst.communicate()  # noqa

            # test exit code of uninstaller
            self.assertEqual(pipe_uninst.returncode, 0)

            # test that there is no `pre_commit` subdirectory in .git/hooks/
            self.assertFalse(
                path.isdir(
                    path.join(repo.repo_path, ".git", "hooks", "pre_commit")
                )
            )

            # test that there is no `pre-commit` script in .git/hooks/
            self.assertFalse(
                path.exists(
                    path.join(repo.repo_path, ".git", "hooks", "pre-commit")
                )
            )

        except Exception:
            raise

        finally:
            tmp.cleanup()


if __name__ == "__main__":
    main()
