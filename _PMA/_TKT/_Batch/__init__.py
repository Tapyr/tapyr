# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    PMA.TKT.Batch.__init__
#
# Purpose
#    Package providing Batch toolkit support for PMA
#
# Revision Dates
#    29-Mar-2005 (CT) Creation
#    ��revision-date�����
#--

from   _TFL.Package_Namespace import Derived_Package_Namespace
from   _PMA                   import PMA
from   _TGL                   import TGL
import _TGL._TKT._Batch
import _PMA._TKT

Batch = Derived_Package_Namespace (parent = TGL.TKT.Batch)
PMA.TKT._Export ("Batch")

del Derived_Package_Namespace

### __END__ PMA.TKT.Batch.__init__
