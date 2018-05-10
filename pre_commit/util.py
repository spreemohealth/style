#!/usr/bin/env python3
from configparser import ConfigParser
from contextlib import contextmanager
from os import (
    chdir,
    getcwd
)


@contextmanager
def exec_in_dir(_dir):
    """
    A simple context manager to execute operations in a given directory.
    """
    if _dir:
        try:
            cwd = getcwd()
            chdir(_dir)
            yield
        except FileNotFoundError:    # noqa F821
            raise
        finally:
            chdir(cwd)
    else:
        yield


def get_config(section, option, conf_file_path):
    """
    Returns the value of an option stored in a section
    of a configuration file

    Args:
        section: a string corresponding to the name of a section of a
            configuration file
        option: a string corresponding to an option contained in a section
            of a configuration file
        conf_file_path: full path to the configuration file

    Returns:
        a string, corresponding to the value of the target option in the
        target section
    """
    parser = ConfigParser()

    parser.read(conf_file_path)

    return parser.get(section, option)
