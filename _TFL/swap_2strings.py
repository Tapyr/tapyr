# -*- coding: iso-8859-15 -*-
# Copyright (C) 2002-2008 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    swap_2strings
#
# Purpose
#    Swap all occurences of two strings in some text
#
# Revision Dates
#    26-Jan-2002 (CT) Creation
#    20-Aug-2003 (CT) s/\n/\\n/ to avoid
#                         `ValueError: inconsistent leading whitespace`
#                     from the $%&@*$ doc-test
#    ��revision-date�����
#--

from _TFL.Regexp import *

class String_Swapper :
    """Swaps all occurences of two strings in some text"""

    def __init__ (self, s1, s2) :
        self.s1   = s1
        self.s2   = s2
        self._map = { s1 : s2, s2 : s1 }
        self._pat = Regexp ("(%s|%s)" % (re.escape (s1), re.escape (s2)))
    # end def __init__

    def __call__ (self, text) :
        """Swap all occurences of `self.s1` and `self.s2` in `text`"""
        return self._pat.sub (self._replace, text)
    # end def __call__

    def _replace (self, match) :
        return self._map [match.group (1)]
    # end def _replace

# end class String_Swapper

def swap_2strings (s1, s2, text) :
    """Swap all occurences of `s1` and `s2` in `text`

       >>> swap_2strings ("a", "b", "ab" * 5)
       'bababababa'
       >>> swap_2strings ("sda", "sdb", "/dev/sda1 /  \\n/dev/sdb1 /alt  ")
       '/dev/sdb1 /  \\n/dev/sda1 /alt  '
       >>> swap_2strings ("sda", "sdb", "/dev/sda2 /b \\n/dev/sdb2 /alt/b")
       '/dev/sdb2 /b \\n/dev/sda2 /alt/b'
    """
    return String_Swapper (s1, s2) (text)
# end def swap_2strings

if __name__ == "__main__" :
    from   _TFL.Command_Line import Command_Line
    import sys
    cmd = Command_Line \
        ( arg_spec =
            ( "s1:S"
            , "s2:S"
            )
        , min_args = 2
        , max_args = 2
        )
    print swap_2strings (cmd.s1, cmd.s2, sys.stdin.read ()),
### __END__ swap_2strings
