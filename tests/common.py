#
# Copyright (C) 2019 Satoru SATOH <satoru.satoh at gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import difflib
import os.path
import os
import tempfile
import unittest


def selfdir():
    """
    :return: module path itself
    """
    return os.path.dirname(__file__)


def setup_workdir():
    """
    :return: Path of the created working dir
    """
    return tempfile.mkdtemp(dir="/tmp", prefix="python-tests-")


def cleanup_workdir(workdir):
    """
    FIXME: Danger!
    """
    os.system("rm -rf " + workdir)


def diff(result, exp):
    """
    Print unified diff.

    :param result: Result string
    :param exp: Expected result string
    """
    diff_ = difflib.unified_diff(result.splitlines(), exp.splitlines(),
                                 'Result', 'Expected')
    return "\n'" + "\n".join(diff_) + "'"


class TestWithIO(unittest.TestCase):

    def setUp(self):
        self.workdir = setup_workdir()

    def tearDown(self):
        cleanup_workdir(self.workdir)

# vim:sw=4:ts=4:et:
