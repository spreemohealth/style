#!/usr/bin/env python3
from os import path
from subprocess import (
    Popen,
    PIPE
)


class GitHandle(object):
    """
    This class provides a handle to perform git-related operations in the
    context of linting staged files.
    """

    def get_git_root(self):
        """
        Gets the absolute path of the root of the git repository.
        """
        pipe = Popen(
            ["git", "rev-parse", "--show-toplevel"],
            stdout=PIPE,
            stderr=PIPE
        )
        out, err = pipe.communicate()

        root = out.decode('utf-8').rstrip()
        root_path = path.abspath(root)

        return root_path

    def get_head_hash(self):
        """
        Gets the current HEAD's hash.
        """
        pipe = Popen(
            ["git", "rev-parse", "--verify", "HEAD"],
            stdout=PIPE,
            stderr=PIPE
        )
        out, err = pipe.communicate()

        head_hash = out.decode('utf-8').rstrip()

        # use the special hash if there is no HEAD
        if not head_hash:
            head_hash = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

        return head_hash

    def get_staged_files_paths(self):
        """
        Gets the absolute paths of all staged files.
        """
        head_hash = self.get_head_hash()

        pipe = Popen(
            ["git", "diff", "--cached", "--name-only", head_hash],
            stdout=PIPE,
            stderr=PIPE
        )
        out, err = pipe.communicate()

        staged_files = (
            out
            .decode('utf-8')
            .strip()
            .split('\n')
        )

        staged_files_paths = [
            path.abspath(file) for file in staged_files
        ]

        return staged_files_paths

    def get_staged_file_content(self, staged_file):
        """
        Gets the content of a given staged file.
        """
        pipe = Popen(
            ["git", "show", ":%s" % staged_file],
            stdout=PIPE,
            stderr=PIPE
        )
        out, err = pipe.communicate()

        return out
