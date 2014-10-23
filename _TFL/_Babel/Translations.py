# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package TFL.Babel.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TFL.Babel.Translations
#
# Purpose
#    Add better support for singular/plural to babel.support.Translations
#
# Revision Dates
#    18-Jun-2010 (CT) Creation (factored from TFL.I18N)
#    23-Oct-2014 (CT) Add `__future__` import of `print_function`
#    ««revision-date»»···
#--

from   __future__              import print_function

from   _TFL                    import TFL
from   _TFL.pyk                import pyk

import _TFL._Babel

import babel.support
import struct

class Translations (babel.support.Translations) :
    """Add better support for singular/plural"""

    def _parse (self, fp):
        """Slighly modifiey version of gettext.GNUTranslations._parse."""
        unpack   = struct.unpack
        filename = getattr (fp, "name", "")
        # Parse the .mo file header, which consists of 5 little endian 32
        # bit words.
        self._catalog = catalog = {}
        self.plural   = lambda n: int (n != 1) # germanic plural by default
        buf           = fp.read ()
        buflen        = len     (buf)
        # Are we big endian or little endian?
        magic = unpack ("<I", buf [:4]) [0]
        if magic == self.LE_MAGIC :
            version, msgcount, masteridx, transidx = unpack ("<4I", buf [4:20])
            ii = "<II"
        elif magic == self.BE_MAGIC:
            version, msgcount, masteridx, transidx = unpack (">4I", buf [4:20])
            ii = ">II"
        else:
            raise IOError (0, "Bad magic number", filename)
        # Now put all messages from the .mo file buffer into the catalog
        # dictionary.
        for i in pyk.xrange (0, msgcount) :
            mlen, moff = unpack (ii, buf [masteridx : masteridx + 8])
            tlen, toff = unpack (ii, buf [transidx  : transidx  + 8])
            mend       = moff + mlen
            tend       = toff + tlen
            if mend < buflen and tend < buflen:
                msg  = buf [moff:mend]
                tmsg = buf [toff:tend]
            else:
                raise IOError (0, "File is corrupt", filename)
            # See if we're looking at GNU .mo conventions for metadata
            if not mlen :
                # Catalog description
                lastk = k = None
                for item in tmsg.splitlines ():
                    item = item.strip ()
                    if not item:
                        continue
                    if ":" in item :
                        k, v           = item.split (":", 1)
                        k              = k.strip ().lower ()
                        v              = v.strip ()
                        self._info [k] = v
                        lastk          = k
                    elif lastk :
                        self._info [lastk] += "\n" + item
                    if k == "content-type" :
                        self._charset = v.split ("charset=") [1]
                    elif k == "plural-forms" :
                        v           = v.split     (";")
                        plural      = v [1].split ("plural=") [1]
                        self.plural = c2py        (plural)
            # Note: we unconditionally convert both msgids and msgstrs to
            # Unicode using the character encoding specified in the charset
            # parameter of the Content-Type header.  The gettext documentation
            # strongly encourages msgids to be us-ascii, but some appliations
            # require alternative encodings (e.g. Zope's ZCML and ZPT).  For
            # traditional gettext applications, the msgid conversion will
            # cause no problems since us-ascii should always be a subset of
            # the charset encoding.  We may want to fall back to 8-bit msgids
            # if the Unicode conversion fails.
            if "\x00" in msg :
                # Plural forms
                msgid1, msgid2 = msg.split  ("\x00")
                tmsg           = tmsg.split ("\x00")
                if self._charset:
                    msgid1 = pyk.text_type (msgid1, self._charset)
                    msgid2 = pyk.text_type (msgid2, self._charset)
                    tmsg   = [pyk.text_type (x, self._charset) for x in tmsg]
                for i, msg in enumerate (tmsg) :
                    catalog [(msgid1, i)] = msg
                ### In addtion to the two keys to the catalog as well to be
                ### able to have access to the singular and the last plural
                ### translation as well
                catalog [msgid1] = tmsg [ 0]
                catalog [msgid2] = tmsg [-1]
            else:
                if self._charset :
                    msg       = pyk.text_type (msg,  self._charset)
                    tmsg      = pyk.text_type (tmsg, self._charset)
                catalog [msg] = tmsg
            # advance to next entry in the seek tables
            masteridx += 8
            transidx  += 8
    # end def _parse

# end class Translations

if __name__ != "__main__" :
    TFL.Babel._Export ("*")
### __END__ TFL.Babel.Translations
