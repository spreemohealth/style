#!/usr/bin/env python3
"""
This module defines the `GitHandle` class which encapsulates the logic of all
of the necessary interaction with git.
"""
from os import path
from shlex import shlex
from subprocess import (
    Popen,
    PIPE
)


class GitError(Exception):
    pass


class ForbiddenCharacterError(GitError):
    """
    Exception raised if a path or a file name has forbidden characters in it.
    """
    pass


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

        # strip the trailing '\n' from the path
        root = out.decode('utf-8').rstrip('\n')
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

        # strip the trailing '\n'
        head_hash = out.decode('utf-8').rstrip('\n')

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
            .rstrip('\n')    # remove trailing '\n'
            .split('\n')
        )

        # drop nulls produce by split, if any
        staged_files = [file for file in staged_files if file]

        staged_files_paths = [
            path.abspath(file) for file in staged_files
        ]

        return staged_files_paths

    def get_staged_file_content(self, staged_file_path):
        """
        Gets the contents of a given staged file.
        """
        # quote the staged_file name or path in order to take care of
        # escaping in the shell
        pipe = Popen(
            ["git", "show", ":%s" % staged_file_path],
            stdout=PIPE,
            stderr=PIPE
        )
        out, err = pipe.communicate()

        return out

    def check_staged_file_path_is_allowed(self, staged_file_path):
        """
        Checks that paths and file names in the staging area do not contain
        forbidden characters (such as whitespace, quotes, ...) that make it
        complicated to execute shell commands.
        """
        forbidden = ''.join([
            shlex().whitespace,
            shlex().quotes,
            shlex().escape
        ])

        if any(map(lambda x: x in forbidden, list(staged_file_path))):
            raise ForbiddenCharacterError(
                "Please do not use special characters "
                "in file names and paths: %s" % staged_file_path
            )
