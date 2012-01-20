# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.__test__.
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
#    MOM.__test__.Sailor
#
# Purpose
#    Test SRM.Sailor creation and querying
#
# Revision Dates
#    27-Apr-2010 (CT) Creation
#     9-Sep-2011 (CT) Queries for `p` and `p.pid` added
#     9-Sep-2011 (CT) Tests for `Q.left.pid` added
#    ��revision-date�����
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> p = PAP.Person.instance_or_new ("Tanzer", "Christian")
    >>> p
    GTW.OMP.PAP.Person (u'tanzer', u'christian', u'', u'')
    >>> s = SRM.Sailor.instance_or_new (p, nation = "AUT", mna_number = "29676", raw = True) ### 1
    >>> s
    GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')
    >>> SRM.Sailor.instance (p.epk_raw, nation = "AUT", mna_number = "29676", raw = True)
    GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')
    >>> SRM.Sailor.instance_or_new (p.epk_raw, nation = "AUT", mna_number = "29676", raw = True)
    GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')
    >>> SRM.Sailor.instance_or_new (p.epk_raw, s.nation, s.mna_number)
    GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')

    >>> SRM.Sailor.query (left = p).all ()
    [GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')]
    >>> SRM.Sailor.query (left = p.pid).all ()
    [GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')]
    >>> SRM.Sailor.query (Q.left == p).all ()
    [GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')]
    >>> SRM.Sailor.query (Q.left == p.pid).all ()
    [GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')]
    >>> SRM.Sailor.query (Q.left.pid == p.pid).all ()
    [GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')]
    >>> SRM.Sailor.query (Q.left.pid == p).all ()
    [GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')]

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ MOM.__test__.Sailor
