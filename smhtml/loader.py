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
import os.path
import os

import smhtml.utils
from smhtml.globals import LOGGER


def decode_part(part):
    """
    Decode a part of MIME multi-part data.

    :param part: :class:`email.mime.base.MIMEBase` object
    :return: A dict contains various info of given MIME `part` data
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
    Get the filename from given MIME `part` data or generate filename to be
    used to save its payload later.

    :param part: :class:`email.mime.base.MIMEBase` object
    :return: A filename as a string
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
    An iterator to yield each info from given MIME multi-part data.

    :param mdata: :class:`email.message.Message` object
    :return: A generator yields info of each part in `mdata`
    """
    for idx, part in enumerate(mdata.walk()):
        if part.get_content_maintype() == "multipart":
            continue

        filename = get_or_gen_filename(part, idx=idx)
        info = decode_part(part)
        info["index"] = idx
        info["filename"] = filename

        LOGGER.debug("part#%d: filename=%s", idx, filename)

        yield info


def loads_itr(content):
    """
    An iterator to yield each info from given MIME multi-part data as a string
    after some checks.

    :param content: Input MHTML data as a string
    :return: A generator yields info of each part loaded from `content`
    :raises: ValueError
    """
    mdata = email.message_from_string(content)

    if not mdata.is_multipart():
        raise ValueError("Multi-part MIME data was not found in "
                         "given string: %s ..." % content[:100])

    for info in parse_itr(mdata):
        yield info


def load_itr(filepath):
    """
    An iterator to yield each info from given MIME multi-part data as a file
    after some checks.

    :param filepath: :class:`pathlib.Path` object or a string represents path
    :return: A generator yields each part parsed from `filepath` opened
    :raises: ValueError
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
    Load and return a list of info of each part of MIME multi-part data from
    given data as a string.

    :param content: Input MHTML data as a string
    :return: A list of info of each part of MIME multi-part data
    :raises: ValueError
    """
    return list(loads_itr(content))


def load(filepath):
    """
    Load and return a list of info of each part of MIME multi-part data from
    given data as a file.

    :param filepath: :class:`pathlib.Path` object or a string represents path
    :return: A list of info of each part of MIME multi-part data
    :raises: ValueError
    """
    return list(load_itr(filepath))


def extract(filepath, output, path_names_only=False):
    """
    Load and extract each part of MIME multi-part data as files from given data
    as a file.

    :param filepath: :class:`pathlib.Path` object represents input
    :param output: :class:`pathlib.Path` object represents output dir
    :param path_names_only: Use the leaf, not full path, of attached files
    :raises: ValueError
    """
    if output == "-":
        raise ValueError("Output dir must be given to extract")

    if os.path.exists(output) and os.path.isfile(output):
        raise OSError("Output '%s' already exists as a file!" % output)

    os.makedirs(output)
    for inf in load_itr(filepath):
        filename = inf["filename"]
        if path_names_only:
            filename = os.path.split(filename)[-1]

        outpath = os.path.join(output, filename)
        outdir = os.path.dirname(outpath)

        LOGGER.debug("Extract %s from %s", filename, filepath)

        if not os.path.exists(outdir):
            os.makedirs(outdir)

        with open(outpath, "wb") as out:
            out.write(inf["payload"])

# vim:sw=4:ts=4:et:
