# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Gl�ck. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    MOM.EMS.SA
#
# Purpose
#    Entity manager strategy using SQLAlchemy session as storeage
#
# Revision Dates
#    16-Oct-2009 (MG) Creation
#    ��revision-date�����
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._EMS
import _MOM.Entity

import _TFL._Meta.Object

import _TFL.defaultdict

import itertools

from   sqlalchemy import exc as SA_Exception

class Manager (TFL.Meta.Object) :
    """Entity manager using hash tables to hold entities."""

    type_name = "SA"

    def __init__ (self, scope) :
        self.scope   = scope
    # end def __init__

    @TFL.Meta.Once_Property
    def session (self) :
        return self.scope.dbw.session
    # end def session

    def add (self, entity) :
        ses = self.session
        ses.flush () ### add all pending operations to the database transaction
        max_c = entity.max_count
        if max_c and max_c <= self.s_count (entity.Essence) :
            raise MOM.Error.Too_Many_Objects (entity, entity.max_count)
        try :
            ses.add   (entity)
            ses.flush ()
        except SA_Exception.IntegrityError, exc :
            print exc
            raise MOM.Error.Name_Clash \
                (entity, self.instance (entity.Essence, entity.epk))
        ### XXX how to handle Roles ???
        ### if entity.Roles :
        ###     r_map = self._r_map
        ###     for r in entity.Roles :
        ###         r_map [r] [r.get_role (entity).id].add (entity)
    # end def add

    def exists (self, Type, epk) :
        Type     = getattr (Type, "_etype", Type)
        ses      = self.session
        epk_dict = dict (zip (Type.epk_sig, epk))
        return [e.type_name for e in ses.query (Type).filter_by (** epk_dict)]
    # end def exists

    def instance (self, Type, epk) :
        Type = getattr (Type, "_etype", Type)
        root = Type.relevant_root
        if root :
            epk_dict = dict (zip (Type.epk_sig, epk))
            return self.session.query (Type).filter_by (** epk_dict).first ()
        raise TypeError \
            ( "Cannot query `instance` of non-root type `%s`."
              "\n"
              "Use one of the types %s instead."
            % (Type.type_name, ", ".join (sorted (Type.relevant_roots)))
            )
    # end def instance

    def remove (self, entity) :
        self.session.delete (entity)
        ### if entity.Roles :
        ###     r_map = self._r_map
        ###     for r in entity.Roles :
        ###         r_map [r] [r.get_role (entity).id].remove (entity)
    # end def remove

    def rename (self, entity, new_epk, renamer) :
        old_entity = self.instance (entity.Essence, new_epk)
        if old_entity :
            raise MOM.Error.Name_Clash (entity, old_entity)
        self.remove (entity)
        renamer     ()
        self.add    (entity)
    # end def rename

    ### XXX May change depending on how inheritance is implemented
    def s_count (self, Type) :
        root = Type.relevant_root
        if root :
            return self.session.query (root).count ()
        return 0
    # end def s_count

    def s_extension (self, Type, sort_key = None) :
        root   = Type.relevant_root
        if root :
            return self.session.query (root)
        return ()
    # end def s_extension

    ### XXX don't know how roles will be handled
    def s_role (self, role, obj) :
        return self._r_map [role] [obj.id]
    # end def s_role

    def t_count (self, Type, seen = None) :
        if seen is None :
            seen = set ()
        result = self.s_count (Type)
        for n, c in Type.children.iteritems () :
            if n not in seen :
                seen.add (n)
                result += self.t_count (c, seen)
        return result
    # end def t_count

    def t_extension (self, Type , sort_key = None) :
        root   = Type.relevant_root
        tables = self._tables
        if root :
            result = tables [root.type_name].itervalues ()
        else :
            result = itertools.chain \
                (* (tables [t].itervalues () for t in Type.relevant_roots))
        return sorted (result, key = sort_key or Type.sorted_by)
    # end def t_extension

    def t_role (self, role, obj) :
        r_map = self._r_map
        i     = role.role_index
        return itertools.chain \
            ( r_map [role] [obj.id]
            , * ( r_map [c.Roles [i]] [obj.id]
                for c in role.assoc.children.itervalues ()
                )
            )
    # end def t_role

    def __iter__ (self) :
        return itertools.chain \
            (* (t.itervalues () for t in self._tables.itervalues ()))
    # end def __iter__

# end class Manager

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.SA
