#
# Copyright (C). 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import, with_statement

import os.path
import os
import unittest

import smhtml.loader as TT
import tests.common as TC


class Test(unittest.TestCase):

    def test_20_load(self):
        ipath = os.path.join(TC.selfdir(), "res/python-smhtml.mhtml")
        res = TT.load(ipath)
        self.assertTrue(res)

# vim:sw=4:ts=4:et:
