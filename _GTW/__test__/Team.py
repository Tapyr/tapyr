# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.__test__.Team
#
# Purpose
#    Test creation and querying of SRM.Team
#
# Revision Dates
#    24-Jan-2012 (CT) Creation
#    ��revision-date�����
#--

from   __future__  import unicode_literals

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SRM  = scope.SRM
    >>> bc   = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> rev0 = SRM.Regatta_Event (u"Teamrace", dict (start = u"20100918", raw = True), raw = True)
    >>> reg0 = SRM.Regatta_C (rev0, boat_class = bc, raw = True)
    >>> rev1 = SRM.Regatta_Event (u"Teamrace", dict (start = u"20111015", raw = True), raw = True)
    >>> reg1 = SRM.Regatta_C (rev1, boat_class = bc, raw = True)
    >>> t1  = SRM.Team (reg0, "Wien/1")
    >>> t2  = SRM.Team (reg0, "Wien/2")
    >>> t3  = SRM.Team (reg0, "Tirol/1")
    >>> t4  = SRM.Team (reg0, "Vorarlberg/1")
    >>> t5  = SRM.Team (reg1, "Wien/3")
    >>> t6  = SRM.Team (reg1, "Wien/4")
    >>> t7  = SRM.Team (reg1, "Tirol/2")
    >>> t8  = SRM.Team (reg1, "Vorarlberg/2")

    >>> scope.commit ()

    >>> t1.regatta.event.date.start
    datetime.date(2010, 9, 18)

    >>> SRM.Team.query ().order_by (TFL.Sorted_By ("name")).all ()
    [GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'tirol/1'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2011/10/15', finish = u'2011/10/15')), (u'Optimist', )), u'tirol/2'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'vorarlberg/1'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2011/10/15', finish = u'2011/10/15')), (u'Optimist', )), u'vorarlberg/2'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'wien/1'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'wien/2'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2011/10/15', finish = u'2011/10/15')), (u'Optimist', )), u'wien/3'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2011/10/15', finish = u'2011/10/15')), (u'Optimist', )), u'wien/4')]

    >>> scope.rollback ()

    >>> SRM.Team.query (Q.regatta.event.date.start == t1.regatta.event.date.start).order_by (TFL.Sorted_By ("name")).all ()
    [GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'tirol/1'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'vorarlberg/1'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'wien/1'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'wien/2')]

    >>> scope.rollback ()

    >>> SRM.Team.query ().order_by (TFL.Sorted_By ("-left.left.date.start", "name")).all ()
    [GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2011/10/15', finish = u'2011/10/15')), (u'Optimist', )), u'tirol/2'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2011/10/15', finish = u'2011/10/15')), (u'Optimist', )), u'vorarlberg/2'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2011/10/15', finish = u'2011/10/15')), (u'Optimist', )), u'wien/3'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2011/10/15', finish = u'2011/10/15')), (u'Optimist', )), u'wien/4'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'tirol/1'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'vorarlberg/1'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'wien/1'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'wien/2')]

    >>> scope.rollback ()

    >>> SRM.Team.query ().order_by (TFL.Sorted_By ("-regatta.event.date.start", "name")).all ()
    [GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2011/10/15', finish = u'2011/10/15')), (u'Optimist', )), u'tirol/2'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2011/10/15', finish = u'2011/10/15')), (u'Optimist', )), u'vorarlberg/2'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2011/10/15', finish = u'2011/10/15')), (u'Optimist', )), u'wien/3'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2011/10/15', finish = u'2011/10/15')), (u'Optimist', )), u'wien/4'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'tirol/1'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'vorarlberg/1'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'wien/1'), GTW.OMP.SRM.Team (((u'teamrace', dict (start = u'2010/09/18', finish = u'2010/09/18')), (u'Optimist', )), u'wien/2')]


"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict \
    ( dict
        ( normal  = _test_code
        )
    )

### __END__ GTW.__test__.Team