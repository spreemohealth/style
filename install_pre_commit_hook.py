#!/usr/bin/env python3
import os
import shutil
import stat
import sys

from argparse import ArgumentParser

#
# Parse arguments
#
parser = ArgumentParser(
    description="Install the 'style' pre-commit hook in one or multiple "
    "repositories."
)

parser.add_argument(
    "repositories",
    metavar="repo",
    type=str,
    nargs="+",
    help="a target git repository")

args = parser.parse_args()

#
# Get absolute paths of the parsed repositories
#
repos = [os.path.abspath(repo) for repo in args.repositories]

#
# Create a dictionary of the type {repo_name: "sucess"/"failure"} to
# summarize installation
#
summary_dict = {repo: False for repo in args.repositories}

#
# Iterate over repositories and try to install the hook
#
# get base directory (root of this project)
base_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

# attempt installation on each repository
for repo in repos:

    # the target path is the ".git/hooks" subdirectory of the git repository
    target_path = os.path.join(repo, '.git', 'hooks')

    # check whether the repository has this subdirectory:
    # if so, intall the hook;
    # if not, abort the installation and alert the user.
    if os.path.isdir(target_path):

        # copy source to target path (overwriting any previous installation)
        target_src_dir = os.path.join(target_path, "pre_commit")
        if os.path.isdir(target_src_dir):
            shutil.rmtree(target_src_dir)
        shutil.copytree(
            os.path.join(base_dir, "pre_commit"), target_src_dir
        )

        # move the pre-commit hook to top (overwriting any previous
        # installation)
        target_pre_commit_hook = os.path.join(target_path, "pre-commit")
        if os.path.exists(target_pre_commit_hook):
            os.remove(target_pre_commit_hook)
        shutil.move(
            os.path.join(target_path, "pre_commit", "pre-commit"),
            os.path.join(target_path, "pre-commit")
        )
        # make the pre-commit file executable
        current_target_pre_commit_hook_stat = os.stat(target_pre_commit_hook)
        os.chmod(
            target_pre_commit_hook,
            current_target_pre_commit_hook_stat.st_mode | stat.S_IEXEC
        )

        # mark installation as successful
        summary_dict[repo] = True

    else:
        print(
            "\nAborting installation on %s.\n"
            "I can't find the '.git/hooks/' subdirectory.\n"
            "Are you sure this is a git repository?" % repo
        )

#
# Summary of installation
#
success_repos = {repo: value for repo, value in summary_dict.items() if value}
success_repos = sorted(success_repos.keys())

if len(success_repos) > 0:
    print(
        "\nThe installation was successfull "
        "for the following repositories:\n%s" % "\n".join(success_repos)
    )
