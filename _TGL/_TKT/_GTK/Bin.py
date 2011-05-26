# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005 Martin Gl�ck. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    TGL.TKT.GTK.Bin
#
# Purpose
#    Wrapper for the GTK widget Bin
#
# Revision Dates
#    22-Mar-2005 (MG) Automated creation
#    22-Mar-2005 (MG) Creation continued
#    ��revision-date�����
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Container

class Bin (GTK.Container) :
    """Wrapper for the GTK widget Bin"""

    GTK_Class        = GTK.gtk.Bin
    __gtk_properties = ()

    def __init__ (self, child = None, ** kw) :
        self.__super.__init__ (** kw)
        if child :
            self.add (child)
    # end def __init__

    def child (self) :
        child = self.wtk_object.get_child ()
        if child :
            child = child.get_data ("ktw_object")
        return child
    child = property (child)

# end class Bin

if __name__ != "__main__" :
    GTK._Export ("Bin")
### __END__ TGL.TKT.GTK.Bin
