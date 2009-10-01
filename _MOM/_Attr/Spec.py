# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Attr.Spec
#
# Purpose
#    Attribute specification for essential entities of the MOM meta object model
#
# Revision Dates
#    24-Sep-2009 (CT) Creation (factored from TOM.Attr.Spec)
#    ��revision-date�����
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Attr.Type
import _MOM._Attr.Kind
import _MOM._Meta.M_Attr_Spec
import _MOM._Prop.Spec

import _TFL._Meta.Property
import _TFL.Alias_Dict

class Spec (MOM.Prop.Spec) :
    """Attribute specification for MOM entities (objects and links).

       A :class:`~_MOM.Entity.Entity` class contains a descendent of `Spec`
       with declarations for all attributes (which are descendents of
       :class:`~_MOM._Attr.Type.A_Attr_Type`) provided by that class.

       :class:`MOM.Meta.M_E_Type<_MOM._Meta.M_E_Type.M_E_Type>` instantiates
       the `Spec`: this results in the assignment of all attribute
       properties, i.e., for all attributes `attr` defined in the `Spec` a
       property named by `attr.name` and instantiated as ::

           attr.kind (attr)

       is added to the `E_Type`.
    """

    __metaclass__   = MOM.Meta.M_Attr_Spec

    _Prop_Pkg       = MOM.Attr
    _Prop_Spec_Name = "_Attributes"
    _prop_dict_cls  = TFL.Alias_Dict
    _prop_dict      = TFL.Meta.Alias_Property ("_attr_dict")
    _prop_kind      = TFL.Meta.Alias_Property ("_attr_kind")

    def __init__ (self, e_type) :
        self._user_attr   = []
        self._syncable    = []
        self.__super.__init__ (e_type)
        e_type.user_attr  = self._user_attr
        e_type.attributes = self._prop_dict
    # end def __init__

    def _setup_alias (self, e_type, alias_name, real_name) :
        setattr (e_type, alias_name, TFL.Meta.Alias_Property (real_name))
        self._prop_dict.add_alias (alias_name, real_name)
    # end def _setup_alias

    def _setup_prop (self, e_type, name, kind, prop) :
        self.__super._setup_prop (e_type, prop.name, kind, prop)
        if name != prop.name :
            self._setup_alias (e_type, name, prop.name)
        if not prop.electric :
            self._user_attr.append (prop)
        if callable (prop.sync) :
            self._syncable.append (prop)
    # end def _setup_prop

# end class Spec

__doc__ = """
Class `MOM.Attr.Spec`
=====================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. autoclass:: Spec

"""

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Spec
