#!/usr/bin/env python
"""
The `hack=True` version tries to avoid the "first commit problem"
where if your first commit in a new repo is a file with issues in
the code, then this file somehow isn't checked by flake8.
"""
import sys

from flake8.main.git import (
    make_temporary_directory,
    copy_indexed_files_to,
    update_excludes,
    update_paths
)


#
# The definition of `hook` is taken from `flake8.main.git`
#
def hook(lazy=False, strict=False, hack=True):
    """Execute Flake8 on the files in git's index.
    Determine which files are about to be committed and run Flake8 over them
    to check for violations.
    :param bool lazy:
        Find files not added to the index prior to committing. This is useful
        if you frequently use ``git commit -a`` for example. This defaults to
        False since it will otherwise include files not in the index.
    :param bool strict:
        If True, return the total number of errors/violations found by Flake8.
        This will cause the hook to fail.
    :returns:
        Total number of errors found during the run.
    :rtype:
        int
    """
    # NOTE(sigmavirus24): Delay import of application until we need it.
    from flake8.main import application
    app = application.Application()
    with make_temporary_directory() as tempdir:
        if hack:
            filepaths = sys.argv[1:]    # here is the hack!
            app.initialize(['.'])
            app.options.exclude = update_excludes(app.options.exclude, tempdir)
            app.options._running_from_vcs = True
            if filepaths:
                app.run_checks(filepaths)

        else:
            filepaths = list(copy_indexed_files_to(tempdir, lazy))
            app.initialize(['.'])
            app.options.exclude = update_excludes(app.options.exclude, tempdir)
            app.options._running_from_vcs = True
            # Apparently there are times when there are no files to check
            # (e.g., when amending a commit). In those cases, let's not try to
            # run checks against nothing.
            if filepaths:
                app.run_checks(filepaths)

    # If there were files to check, update their paths and report the errors
    if filepaths:
        update_paths(app.file_checker_manager, tempdir)
        app.report_errors()

    if strict:
        return app.result_count
    return 0


sys.exit(
    hook(lazy=False, strict=True, hack=True)
)
