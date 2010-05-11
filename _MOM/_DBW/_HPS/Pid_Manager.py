# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.DBW.HPS.
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
#    MOM.DBW.HPS.Pid_Manager
#
# Purpose
#    HPS specific manager for permanent ids
#
# Revision Dates
#    11-May-2010 (CT) Creation
#    ��revision-date�����
#--

from   _MOM       import MOM
from   _TFL       import TFL

import _MOM._DBW._HPS
import _MOM._DBW.Pid_Manager

class Pid_Manager (MOM.DBW.Pid_Manager) :
    """HPS specific manager for permanent ids."""

    def __init__ (self) :
        self.max_pid = 0
        self.table   = {}
    # end def __init__

    def new (self, entity) :
        self.max_pid += 1
        result = self.max_pid
        self.table [result] = entity
        return result
    # end def new

    def query (self, pid) :
        return self.table [pid]
    # end def query

    def reserve (self, entity, pid) :
        table = self.table
        if pid in table :
            raise ValueError \
                ( "Cannot reserve pid %s of existing object %r"
                % (pid, table [pid])
                )
        elif pid <= self.max_pid :
            raise ValueError \
                ( "Cannot reserve pid %s < maximum used pid %s"
                % (pid, self.max_pid)
                )
        self.max_pid = pid + 1
        table [pid] = entity
        return pid
    # end def reserve

# end class Pid_Manager

if __name__ != "__main__" :
    MOM.DBW.HPS._Export ("*")
### __END__ MOM.DBW.HPS.Pid_Manager
