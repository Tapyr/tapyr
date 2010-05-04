# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.NAV.E_Type.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.NAV.E_Type.SRM
#
# Purpose
#    Navigation directory and pages for instances of SRM
#
# Revision Dates
#    30-Apr-2010 (CT) Creation
#    ��revision-date�����
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW.FO
import _GTW._NAV.Base
import _GTW._NAV._E_Type.Manager
import _GTW._NAV._E_Type.Mixin

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.I18N                import _, _T, _Tn

from   posixpath                import join  as pjoin

class Regatta_Event (GTW.NAV.E_Type.Instance_Mixin, GTW.NAV.Dir) :
    """Navigation directory for a single regatta event."""

    def __init__ (self, manager, obj, ** kw) :
        kw ["src_dir"] = kw ["sub_dir"] = obj.perma_name
        self.__super.__init__ (manager, obj, ** kw)
    # end def __init__

    ### XXX implement _get_child

    def _get_objects (self) :
        ### XXX add regatta info (registration list, results, ...)
        return self._get_pages ()
    # end def _get_objects

    def _get_pages (self) :
        T     = GTW.NAV.E_Type.Instance
        kw    = self.page_args
        rev   = self.obj
        query = self.scope.SRM.Page.query_s (event = rev)
        return [T (self, o, page_args = kw, ** kw) for o in query]
    # end def _get_pages

# end class Regatta_Event

class SRM (GTW.NAV.E_Type.Manager_T_Archive_Y) :
    """Navigation directory listing regatta events by year."""

    Page            = Regatta_Event

    def __init__ (self, src_dir, ** kw) :
        self.__super.__init__ (src_dir = src_dir, ** kw)
        top   = self.top
        scope = top.scope
        for et in (scope.SRM.Page,) : ### XXX ???
            etn = et.type_name
            if etn not in top.E_Types :
                top.E_Types [etn] = self
    # end def __init__

    def href_display (self, obj) :
        scope = self.top.scope
        comps = [self.abs_href, str (obj.year)]
        if isinstance (obj, scope.SRM.Page._etype) :
            comps.append (obj.event.perma_name)
        comps.append (obj.perma_name)
        return pjoin (* comps)
    # end def href_display

    ### XXX implement _get_child

# end class SRM

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.SRM