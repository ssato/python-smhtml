#
# -*- coding: utf-8; mode: python -*-
#
# Copyright (C) 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=unused-import
r"""Simple and very experimental MHTML Parser

.. versionadded:: 0.0.1
"""
from __future__ import absolute_import

import base64
import email
import mimetypes
import quopri
import chardet


def detect_charset(bmsg, default="ascii"):
    r"""
    :param bmsg: A byte data to detect charset
    :return: A string represents charset such as 'utf-8', 'iso-2022-jp'

    >>> detect_charset(b"a")
    'ascii'
    >>> detect_charset(b"")
    'ascii'
    >>> detect_charset(u"あ".encode("utf-8"))
    'utf-8'
    """
    if not bmsg:
        return default

    return chardet.detect(bmsg)["encoding"]


def decode_part(part):
    """
    :param part: :class:`email.message.Message` object (MIME part)
    """
    cte = part.get_all("Content-Transfer-Encoding")[0]
    msg = part.get_payload()

    ctype = part.get_content_type()
    mtype = part.get_content_maintype()

    if cte == "base64":
        bdata = base64.b64decode(msg)
    elif cte == "quoted-printable":
        bdata = quopri.decodestring(msg)
    else:
        bdata = msg

    if mtype == "text":
        charset = detect_charset(bdata)
        data = bdata.decode(charset, "ignore")
    else:
        charset = None
        data = bdata

    return dict(type=ctype, encoding=charset, data=data,
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


def parse_itr(filepath):
    """
    :param filepath: :class:`pathlib.Path` object
    :return: A generator yields each part parsed from `filepath` opened
    """
    with open(filepath) as fobj:
        mhtml_data = email.message_from_file(fobj)

    if not mhtml_data.is_multipart():
        raise ValueError("Multi-part MIME data was not found in "
                         "'%s'" % filepath)

    for idx, part in enumerate(mhtml_data.walk()):
        if part.get_content_maintype() == "multipart":
            continue

        filename = get_or_gen_filename(part, idx=idx)
        info = decode_part(part)
        info["index"] = idx
        info["filename"] = filename

        yield info


def parse(filepath):
    """
    :param filepath: :class:`pathlib.Path` object
    :return: A list of parsed data
    """
    return list(parse_itr(filepath))

# vim:sw=4:ts=4:et:
