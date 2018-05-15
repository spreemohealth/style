#!/usr/bin/env python3
"""
Tests for the `pre_commit.git` submodule.
"""
from os import path
from tempfile import TemporaryDirectory
from unittest import (
    main,
    TestCase
)

from pre_commit.git import (
    ForbiddenCharacterError,
    GitHandle,
    RepositoryError
)

from tests.util import BasicRepo


class TestGitHandle(TestCase):

    def test_get_git_root(self):

        try:
            # initialize repo
            repo = BasicRepo()

            # initialize git handle
            git_handle = GitHandle(repo.repo_path)

            # test
            self.assertEqual(
                path.abspath(git_handle.root),
                path.abspath(repo.repo_path)
            )

        except Exception:
            raise

        finally:
            repo.delete()

    def test_check_path_is_allowed(self):

        try:
            # initialize repo
            repo = BasicRepo()

            # initialize git handle
            git_handle = GitHandle(repo.repo_path)

            # test some bad paths and file names...
            with self.assertRaises(ForbiddenCharacterError):
                git_handle._check_path_is_allowed("a bad/path")

            with self.assertRaises(ForbiddenCharacterError):
                git_handle._check_path_is_allowed("/a\nice/path/")

            with self.assertRaises(ForbiddenCharacterError):
                git_handle._check_path_is_allowed("this_is_/'the'/_path")

            with self.assertRaises(ForbiddenCharacterError):
                git_handle._check_path_is_allowed(
                    path.join("\\", "a_path")
                )

            with self.assertRaises(ForbiddenCharacterError):
                git_handle._check_path_is_allowed(
                    path.join("/some/path", "this is_bad.ext")
                )

        except Exception:
            raise

        finally:
            repo.delete()

    def test_get_head_hash_bare(self):

        try:
            # initialize repo
            repo = BasicRepo()

            # initialize git handle
            git_handle = GitHandle(repo.repo_path)

            # test
            self.assertEqual(
                git_handle.get_head_hash(),
                "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
            )

        except Exception:
            raise

        finally:
            repo.delete()

    def test_get_head_hash_not_bare(self):

        try:
            # initialize repo
            repo = BasicRepo(bare=False)

            # initialize git handle
            git_handle = GitHandle(repo.repo_path)

            # test commit
            test_commit_file = path.join(repo.repo_path, "test_commit")
            with open(test_commit_file, "w") as foo:
                foo.write("test commit")
            repo.repo.git.add(test_commit_file)
            repo.repo.git.commit("-m", "test commit")

            self.assertEqual(
                git_handle.get_head_hash(),
                repo.repo.head.commit.hexsha
            )

        except Exception:
            raise

        finally:
            repo.delete()

    def test_get_staged_file_paths(self):

        try:
            # initialize repo
            repo = BasicRepo(bare=False)

            # initialize git handle
            git_handle = GitHandle(repo.repo_path)

            # test staging
            test_staged_file = path.join(repo.repo_path, "test_staged_file")
            with open(test_staged_file, "w") as foo:
                foo.write("test stage")

            test_staged_file1 = path.join(repo.repo_path, "test_staged_file1")
            with open(test_staged_file1, "w") as foo:
                foo.write("test stage1")

            # stage
            repo.repo.git.add([test_staged_file, test_staged_file1])

            self.assertEqual(
                set(git_handle.get_staged_files_paths()),
                set([
                    path.relpath(test_staged_file, repo.repo_path),
                    path.relpath(test_staged_file1, repo.repo_path)
                ])
            )

        except Exception:
            raise

        finally:
            repo.delete()

    def test_staged_file_content(self):

        try:
            # initialize repo
            repo = BasicRepo(bare=False)

            # initialize git handle
            git_handle = GitHandle(repo.repo_path)

            # write file
            test_staged_file = path.join(repo.repo_path, "test_staged_file")
            with open(test_staged_file, "w") as foo:
                foo.write("test stage")

            # stage
            repo.repo.git.add([test_staged_file])

            # edit the file again
            with open(test_staged_file, "a") as foo:
                foo.write("\nmore")

            # get staged file path
            pth = git_handle.get_staged_files_paths()[0]

            self.assertEqual(
                git_handle.get_staged_file_content(pth),
                b"test stage"
            )

        except Exception:
            raise

        finally:
            repo.delete()


class TestGitHandleErrors(TestCase):

    def test_repository_error(self):
        try:
            tmp = TemporaryDirectory()
            with self.assertRaises(RepositoryError):
                GitHandle(tmp.name)

        except Exception:
            raise

        finally:
            tmp.cleanup()


if __name__ == "__main__":
    main()
