# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SRM.
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
#    GTW.OMP.SRM.Regatta
#
# Purpose
#    Model a sailing regatta for one class or handicap
#
# Revision Dates
#    15-Apr-2010 (CT) Creation
#    ��revision-date�����
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._SRM.Boat_Class
import _GTW._OMP._SRM.Regatta_Event

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Link1

class Regatta (_Ancestor_Essence) :
    """Sailing regatta for one class or handicap."""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Regatta event to which this regatta belongs."""

            role_type          = GTW.OMP.SRM.Regatta_Event
            auto_cache         = True
            role_name          = "event"

        # end class left

    # end class _Attributes

# end class Regatta

_Ancestor_Essence = Regatta

class Regatta_C (_Ancestor_Essence) :
    """Regatta for a single class of sail boats."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class boat_class (A_Object) :
            """Class of boats sailing in this regatta."""

            kind               = Attr.Primary
            Class              = GTW.OMP.SRM.Boat_Class

        # end class boat_class

    # end class _Attributes

# end class Regatta_C

_Ancestor_Essence = Regatta

class Regatta_H (_Ancestor_Essence) :
    """Regatta for boats in a handicap system."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class handicap (A_String) :
            """Name of handicap system used for this regatta."""

            kind               = Attr.Primary
            max_length         = 10

        # end class handicap

    # end class _Attributes

# end class Regatta_H

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Regatta