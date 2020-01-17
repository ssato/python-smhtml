#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""CLI frontend to process MHTML data.
"""
from __future__ import absolute_import
from __future__ import print_function

import argparse
import logging
import os.path
import sys

import smhtml

LOGGER = logging.getLogger("smhtml")
LOGGER.addHandler(logging.StreamHandler())


def option_parser():
    """
    :return: Option parsing object :: optparse.OptionParser
    """
    defaults = dict(output='-', verbose=1)

    psr = argparse.ArgumentParser()
    psr.set_defaults(**defaults)

    psr.add_argument("input", type=str, nargs="?",
                     help="Input file or dir path")
    psr.add_argument("-o", "--output", help="Output filename [stdout]")
    psr.add_argument("-v", "--verbose", action="store_const", const=0,
                     help="Verbose mode")
    psr.add_argument("-q", "--quiet", action="store_const", const=2,
                     dest="verbose", help="Quiet mode")
    psr.add_argument("--path_names_only", action='store_true',
                     help="Use the leaf, not full path, of attached files")
    return psr


def set_log_level(level):
    """
    Set log level.
    """
    try:
        lvl = [logging.DEBUG, logging.INFO, logging.WARN][level]
    except IndexError:
        lvl = logging.INFO

    LOGGER.setLevel(lvl)


def main(argv=None):
    """
    Entrypoint.
    """
    if argv is None:
        argv = sys.argv

    psr = option_parser()
    args = psr.parse_args(argv[1:])
    set_log_level(args.verbose)

    if not args.input:
        psr.print_usage()
        sys.exit(0)

    (_fname, fext) = os.path.splitext(args.input)
    if fext and fext in (".mht", ".mhtml"):
        try:  # Try to extract given MHTML data
            LOGGER.info("'%s' looks a MHTML data and try to extract files "
                        "from it", args.input)
            smhtml.extract(args.input, args.output, args.path_names_only)
        except (ValueError, OSError) as exc:
            print(str(exc), file=sys.stderr)
    else:
        # Try to make MHTML data from given file or files under it.
        LOGGER.info("'%s' does not look a MHTML data and try to make "
                    "a MHTML from it", args.input)
        smhtml.dump(args.input, args.output)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
