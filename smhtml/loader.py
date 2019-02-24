#
# Copyright (C) 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=unused-import
r"""Load and parse MHTML data.

.. versionadded:: 0.0.1
"""
from __future__ import absolute_import

import email
import mimetypes

import smhtml.utils


def decode_part(part):
    """
    :param part: :class:`email.message.Message` object (MIME part)
    """
    bdata = part.get_payload(decode=True)
    ctype = part.get_content_type()
    mtype = part.get_content_maintype()

    if mtype == "text":
        charset = smhtml.utils.detect_charset(bdata)
        data = bdata.decode(charset, "ignore")
    else:
        charset = None
        data = bdata

    return dict(type=ctype, encoding=charset, data=data, payload=bdata,
                location=part.get_all("Content-Location"))


def get_or_gen_filename(part, idx=0):
    """
    :param part: :class:`email.message.Message` object (MIME part)
    """
    filename = part.get_filename()
    if not filename:
        fileext = mimetypes.guess_extension(part.get_content_type())
        if not fileext:
            fileext = ".bin"
        filename = "part-%03d%s" % (idx, fileext)

    return filename


def parse_itr(mdata):
    """
    :param mdata: Input Multi-part MIME data
    :return: A generator yields each part in `mdata`
    """
    for idx, part in enumerate(mdata.walk()):
        if part.get_content_maintype() == "multipart":
            continue

        filename = get_or_gen_filename(part, idx=idx)
        info = decode_part(part)
        info["index"] = idx
        info["filename"] = filename

        yield info


def loads_itr(content):
    """
    :param content: Input MHTML data as a string
    :return: A generator yields each part parsed from `content`
    """
    mdata = email.message_from_string(content)

    if not mdata.is_multipart():
        raise ValueError("Multi-part MIME data was not found in "
                         "given string: %s ..." % content[:100])

    for info in parse_itr(mdata):
        yield info


def load_itr(filepath):
    """
    :param filepath: :class:`pathlib.Path` object
    :return: A generator yields each part parsed from `filepath` opened
    """
    with open(filepath) as fobj:
        mdata = email.message_from_file(fobj)

    if not mdata.is_multipart():
        raise ValueError("Multi-part MIME data was not found in "
                         "'%s'" % filepath)

    for info in parse_itr(mdata):
        yield info


def loads(content):
    """
    :param content: Input MHTML data as a string
    :return: A list of parsed data
    """
    return list(loads_itr(content))


def load(filepath):
    """
    :param filepath: :class:`pathlib.Path` object
    :return: A list of parsed data
    """
    return list(load_itr(filepath))

# vim:sw=4:ts=4:et:
