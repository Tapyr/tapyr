# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Butcon
#
# Purpose
#    Model simple Button Control widget
#
# Revision Dates
#    17-Feb-2005 (RSC) Creation
#    25-Feb-2005 (ABR) Fixed doctest (uses png's instead of xbm's)
#    25-Feb-2005 (RSC) Re-added bitmaps that fail TGW doctest
#    ��revision-date�����
#--

from   _TFL                 import TFL
import _TFL._TKT.Mixin

class Butcon (TFL.TKT.Mixin) :
    """Model simple Button Control widget."""

    _interface_test   = """
        >>> w = Butcon ()
        >>> w.apply_bitmap ('arrow_down')
        >>> w.apply_bitmap ('arrow_left')
        >>> w.apply_bitmap ('arrow_right')
        >>> w.apply_bitmap ('open_node')
        >>> w.apply_bitmap ('closed_node')
        >>> w.apply_bitmap ('circle')
    """

    def apply_bitmap (self, bitmap) :
        """Apply `bitmap` to our widget, replacing existing bitmap."""
        raise NotImplementedError, \
            "%s must define apply_bitmap" % (self.__class__.__name__, )
    # end def apply_bitmap

    def apply_style (self, style) :
        """Apply `style` to our widget."""
        raise NotImplementedError, \
            "%s must define apply_style" % (self.__class__.__name__, )
    # end def apply_style

    def remove_style (self, style) :
        """Remove `style` from our widget."""
        raise NotImplementedError, \
            "%s must define remove_style" % (self.__class__.__name__, )
    # end def apply_style

# end class Butcon

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TFL.TKT.Tk.Text
