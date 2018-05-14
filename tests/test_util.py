#!/usr/bin/env python3
"""
Tests for the `pre_commit.util` submodule.
"""
from os import (
    getcwd,
    mkdir,
    path,
    remove
)
from shutil import rmtree
from unittest import (
    main,
    TestCase
)

from pre_commit.util import (
    get_config,
    exec_in_dir
)


class TestExecInDir(TestCase):

    cwd = getcwd()

    def test_no_dir_change(self):
        # write a test file in current directory and check its path

        try:
            # test
            with exec_in_dir(None):
                test_file_path = path.join(self.cwd, "foo.txt")
                with open(test_file_path, "w") as foo:
                    foo.write("a-ha!")

            self.assertEqual(path.abspath(getcwd()), path.abspath(self.cwd))
            self.assertTrue(path.isfile(path.abspath(test_file_path)))

        except Exception:
            raise

        finally:
            # clean up
            remove(path.abspath(test_file_path))

    def test_dir_change(self):
        # write a test file in a subdirectory and check its path

        try:
            # make subdirectory
            subdir = path.join(self.cwd, "foo_subdir")
            mkdir(subdir)

            # test
            with exec_in_dir(subdir):
                test_file_path = path.join(getcwd(), "foo_sub.txt")
                with open(test_file_path, "w") as foo:
                    foo.write("a-ha!")

            self.assertEqual(path.abspath(getcwd()), path.abspath(self.cwd))
            self.assertTrue(path.isfile(path.abspath(test_file_path)))

        except Exception:
            raise

        finally:
            # clean up
            rmtree(subdir)


class TestGetConfig(TestCase):

    cwd = getcwd()

    def test_get_config(self):

        try:
            # write a config file
            test_config_path = path.join(self.cwd, "config.conf")

            with open(test_config_path, "w") as foo:
                foo.write("[section1]\n")
                foo.write("option1 = foo\n")
                foo.write("[section2]\n")
                foo.write("option2 = bar\n")

            # test
            self.assertEqual(
                get_config("section1", "option1", test_config_path),
                "foo"
            )
            self.assertEqual(
                get_config("section2", "option2", test_config_path),
                "bar"
            )

        except Exception:
            raise

        finally:
            # clean up
            remove(path.abspath(test_config_path))


if __name__ == "__main__":
    main()
