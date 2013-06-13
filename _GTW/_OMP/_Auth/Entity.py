# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
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
#    GTW.OMP.Auth.Entity
#
# Purpose
#    Common base class for essential classes of GTW.OMP.Auth
#
# Revision Dates
#    13-Jan-2010 (MG) Creation
#    16-Jan-2010 (CT) `Object` added
#     3-Feb-2010 (MG) `is_partial` added
#    13-Jun-2013 (CT) Pass `pns_alias` to `MOM.derive_pns_bases`
#    ��revision-date�����
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW

import _MOM.derive_pns_bases

import _GTW._OMP._Auth

MOM.derive_pns_bases (GTW.OMP.Auth, MOM, pns_alias = "Auth")

if __name__ != "__main__" :
    GTW.OMP.Auth._Export ("*")
### __END__ GTW.OMP.Auth.Entity
