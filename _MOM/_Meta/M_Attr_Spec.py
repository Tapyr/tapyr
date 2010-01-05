# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    MOM.Meta.M_Attr_Spec
#
# Purpose
#    Metaclass for MOM.Attr.Spec classes
#
# Revision Dates
#    29-Sep-2009 (CT) Creation (factored from TOM.Meta.M_Attr_Spec)
#    ��revision-date�����
#--

from   _MOM                import MOM

import _MOM._Meta.M_Prop_Spec
import _MOM.Error

class M_Attr_Spec (MOM.Meta.M_Prop_Spec) :
    """Meta class for `MOM.Attr.Spec`. It gathers all (including all
       inherited) members of `Spec` which are derived from `A_Attr_Type` and
       puts them into the class attribute `_names`.

       Setting a member to `None` in a derived `Spec` will remove the
       attribute from the `Spec`.
    """

    def _m_inconsistent_prop (cls, n, v, _names, dict) :
        return MOM.Error.Inconsistent_Attribute, \
            ( "%s: Attribute `%s = %r` clashes with %s"
            ) % (dict ["__module__"], n, type (v), _names [n])
    # end def _m_inconsistent_prop

# end class M_Attr_Spec

__doc__ = """
Class `MOM.Meta.M_Attr_Spec`
============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. autoclass:: M_Attr_Spec

"""

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Attr_Spec
