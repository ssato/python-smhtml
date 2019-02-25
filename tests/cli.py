#
# Copyright (C). 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import, with_statement

import glob
import os.path

import smhtml.cli as TT
import tests.common as TC


class TestWithIO(TC.TestWithIO):

    def test_10_invalid_options(self):
        self.assertRaises(SystemExit, TT.main, [__file__, "--unknown-opt-a"])

    def test_20_extract(self):
        ipath = os.path.join(TC.selfdir(), "res/python-smhtml.mhtml")
        opath = os.path.join(self.workdir, "out")
        TT.main([__file__, "-q", "-o", opath, ipath])

        self.assertTrue(os.path.exists(opath))
        self.assertTrue(glob.glob(os.path.join(opath, "*.htm*")))

    def test_30_dump(self):
        ipath = os.path.join(TC.selfdir(), "..", "smhtml")
        opath = os.path.join(self.workdir, "out.mht")
        TT.main([__file__, "-q", "-o", opath, ipath])

        self.assertTrue(os.path.exists(opath))

# vim:sw=4:ts=4:et:
