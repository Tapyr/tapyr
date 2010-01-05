# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.Meta.M_Object
#
# Purpose
#    Meta class of object-types of MOM meta object model
#
# Revision Dates
#    23-Sep-2009 (CT) Creation (factored from `TOM.Meta.M_Object`)
#    18-Oct-2009 (CT) `_m_new_e_type_dict` redefined (add `Roles`)
#    27-Oct-2009 (CT) s/Scope_Proxy/E_Type_Manager/
#     4-Nov-2009 (CT) s/E_Type_Manager_O/E_Type_Manager.Object/
#    24-Nov-2009 (CT) `link_map` added
#    ��revision-date�����
#--

from   _MOM import MOM
from   _TFL import TFL

import _MOM._Meta.M_Entity
import _MOM.E_Type_Manager

import _TFL._Meta.Once_Property
import _TFL.defaultdict

class M_Object (MOM.Meta.M_Id_Entity) :
    """Meta class of MOM.Object."""

    def _m_new_e_type_dict (cls, app_type, etypes, bases, ** kw) :
        result = cls.__m_super._m_new_e_type_dict \
            ( app_type, etypes, bases
            , _all_link_map = None
            , _own_link_map = TFL.defaultdict (set)
            , Roles         = None
            , ** kw
            )
        return result
    # end def _m_new_e_type_dict

# end class M_Object

@TFL.Add_To_Class ("M_E_Type", M_Object)
class M_E_Type_Object (MOM.Meta.M_E_Type_Id) :
    """Meta class for essence of MOM.Object."""

    Manager = MOM.E_Type_Manager.Object

    @property
    def link_map (cls) :
        result = cls._all_link_map
        if result is None :
            result = cls._all_link_map = TFL.defaultdict (set)
            refuse = cls.refuse_links
            for b in cls.__bases__ :
                for k, v in getattr (b, "link_map", {}).iteritems () :
                    if k not in refuse :
                        result [k].update (v)
            for k, v in cls._own_link_map.iteritems () :
                result [k].update (v)
        return result
    # end def link_map

# end class M_E_Type_Object

__doc__ = """
Class `MOM.Meta.M_Object`
=========================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: M_Object

    `MOM.Meta.M_Object` provides the meta machinery for defining
    essential object types and instances. It is based on
    :class:`~_MOM._Meta.M_Entity.M_Entity`.


"""

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Object
