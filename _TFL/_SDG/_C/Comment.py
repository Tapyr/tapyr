# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TFL.SDG.C.Comment
#
# Purpose
#    Model comments in the code in a C file
#
# Revision Dates
#    26-Jul-2004 (CT) Creation
#    27-Jul-2004 (CT) Creation continued
#    28-Jul-2004 (CT) Creation continued...
#    11-Aug-2004 (MG) `Documentation_Block` added
#    12-Aug-2004 (MG) `cgi` set to None
#    12-Aug-2004 (MG) `textwrap` added and new `comp_prec` format used
#    13-Aug-2004 (MG) formats changed (use new attribte `ht_width` to ensure
#                     alignment)
#    24-Aug-2004 (CT) `formatted` redefined to guard with `level <= out_level`
#    15-Sep-2004 (CT) `_description` changed to enforce minimum width for
#                     textwrap.TextWrapper
#    15-Sep-2004 (MG) `_description` use `max` instead of min
#    ��revision-date�����
#--

from   _TFL              import TFL
import _TFL._SDG._C.Node
import textwrap

"""
from _TFL._SDG._C.Comment import *
c = Comment ("abc", "def", "xyzzzzz")
c.write_to_h_stream()
print repr (c)

"""

class Comment (TFL.SDG.Leaf, TFL.SDG.C.Node) :
    """Comment in a C file"""

    cgi                  = None
    rest_args            = "description"

    init_arg_defaults    = dict \
        ( level          = 1
        , stars          = 1
        , eol            = 0
        , new_line_col   = 0
        , tail_column    = 79
        )

    out_level            = 1
    eol_comment_head     = 40
    eol_comment_tail     = 79
    electric_break       = 1

    if 0 :
        ### just as demonstration how to use a different but still correct
        ### layout
        h_format = c_format  = """
            /%("*" * stars)s %(:sep=%("*" * stars)s* :.description:)s
            %("*" * stars)s/
        """

    h_format = c_format  = \
        ("""%(:head=/%("*" * stars)s """
         """�tail= %("*" * stars)s/"""
         """:@_description:)"""
            """-{output_width - indent_anchor - ht_width - stars*2 - 4}s"""
        )

    def formatted (self, format_name, * args, ** kw) :
        if self.level <= self.out_level :
            return self.__super.formatted (format_name, * args, ** kw)
        else :
            return ()
    # end def formatted

    def _convert_c_comment (self, name, value, ** kw) :
        return value ### avoid endless recursion
    # end def _convert_c_comment

    def _description (self, ** kw) :
        format_prec = max (int (kw ["format_prec"]), 40)
        wrapper     = textwrap.TextWrapper (width = format_prec)
        for desc in self.description :
            for l in wrapper.wrap (desc) :
                yield l
    # end def _description

# end class Comment

class Documentation_Block (Comment) :
    """A block used for the automatic documentation generation"""

    init_arg_defaults    = dict \
        ( block_name     = "Description"
        )

    _autoconvert         = dict \
        ( block_name     = lambda s, k, v : v and "%s:" % (v, ) or None
        )

    h_format = c_format  = """
        %(:head=/%("*" * stars)s �tail= %("*" * stars)s/:.block_name:)s
        %(:head=/%("*" * stars)s      �tail= %("*" * stars)s/:.description:)s
    """

# end class Documentation_Block

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.Comment
