#
# Copyright (C) 2019 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import, with_statement

import os.path
import unittest

import smhtml.dumper as TT
import tests.common as TC


class Test(unittest.TestCase):

    def test_20_dumps__single_file(self):
        res = TT.dumps(__file__)
        self.assertTrue(res)


class TestWithIO(unittest.TestCase):

    def setUp(self):
        self.workdir = TC.setup_workdir()

    def tearDown(self):
        TC.cleanup_workdir(self.workdir)

    def test_20_dump__single_file(self):
        outpath = os.path.join(self.workdir, "test.mht")
        TT.dump(__file__, outpath)

        self.assertTrue(os.path.exists(outpath))

# vim:sw=4:ts=4:et:
