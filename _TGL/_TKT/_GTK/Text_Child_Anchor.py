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
#    TGL.TKT.GTK.Text_Child_Anchor
#
# Purpose
#    Wrapper for the GTK widget TextChildAnchor
#
# Revision Dates
#    28-Mar-2005 (MG) Automated creation
#    ��revision-date�����
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.G_Object

class Text_Child_Anchor (GTK.G_Object) :
    """Wrapper for the GTK widget TextChildAnchor"""

    GTK_Class        = GTK.gtk.TextChildAnchor
    __gtk_properties = \
        ( 
        )

# end class Text_Child_Anchor

if __name__ != "__main__" :
    GTK._Export ("Text_Child_Anchor")
### __END__ TGL.TKT.GTK.Text_Child_Anchor
