# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.EVT.
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
#    GTW.OMP.EVT.Event
#
# Purpose
#    Model a calendary event
#
# Revision Dates
#    10-Mar-2010 (CT) Creation
#    16-Mar-2010 (CT) `_change_callback` added
#    18-Aug-2010 (CT) `dates.computed` changed to use `recurrence.dates`
#    18-Aug-2010 (CT) Attribute `rule` removed
#    18-Aug-2010 (CT) `recurrence` changed from `A_Recurrence_Rule` to
#                     `A_Recurrence_Rule_Set`
#     6-Sep-2010 (CT) `recurrence` changed from list of composite attributes
#                     to `Link1`
#     7-Sep-2010 (CT) `_change_callback` guarded by
#                     `date in change.attr_changes`
#     8-Sep-2010 (CT) `dates.computed` changed to use temporary
#                     `Recurrence_Rule` if not explicit one is given
#    17-Nov-2010 (CT) `left.sort_rank` set to `10` to have events sort by
#                     (`date`,`time`,`left`) instead of (`left`,`date`,`time`)
#    22-Dec-2010 (CT) `Event_occurs.electric` redefined as `Const` with `True`
#    ��revision-date�����
#--

from   _MOM.import_MOM            import *
from   _MOM._Attr.Type            import *
from   _MOM._Attr.Date_Interval   import *
from   _MOM._Attr.Time_Interval   import *

from   _GTW                       import GTW

import _GTW._OMP._EVT.Entity

from   _TFL.I18N                  import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.EVT.Link1

class Event (_Ancestor_Essence) :
    """Model a calendary event (or set of recurring events)"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Object which this event is bound to."""

            ### XXX
            import _GTW._OMP._SWP.Page
            role_type          = GTW.OMP.SWP.Page
            role_name          = "object"

            ### give `date` and `time` priority for sorting
            sort_rank          = 10

            auto_cache         = "events"

        # end class left

        class date (A_Date_Interval) :
            """Date interval of event (for non-recurring events, only `start` is relevant)"""

            kind               = Attr.Primary_Optional

        # end class date

        class time (A_Time_Interval) :
            """Time interval of event (for a full-day event, this is empty)"""

            kind               = Attr.Primary_Optional

        # end class time

        ### Non-primary attributes

        class dates (A_Blob) :

            kind               = Attr.Computed

            def computed (self, obj) :
                rr = obj.recurrence
                if not rr :
                    if not obj.date :
                        return []
                    ### create temporary Recurrence_Spec and Recurrence_Rule
                    ### without putting them into `home_scope`
                    scope = obj.home_scope
                    rs = scope.EVT.Recurrence_Spec._etype (obj, scope = scope)
                    rr = scope.EVT.Recurrence_Rule._etype (rs,  scope = scope)
                return list (rr.occurrences)
            # end def computed

        # end class dates

        class detail (A_String) :
            """Information about event."""

            kind               = Attr.Optional
            max_length         = 160

        # end class detail

        class short_title (A_String) :

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Computed_Mixin, )

            def computed (self, obj) :
                if obj :
                    return obj.detail or (obj.object and obj.object.short_title)
            # end def computed

        # end class short_title

        class title (A_String) :

            kind               = Attr.Computed

            def computed (self, obj) :
                if obj :
                    return obj.object.title
            # end def computed

        # end class title

    # end class _Attributes

    def compute_occurrences (self) :
        scope = self.home_scope
        ETM   = self.home_scope ["GTW.OMP.EVT.Event_occurs"]
        for o in list (self.occurs) :
            o.destroy ()
        for d in self.dates :
            ETM (self, date = d, time = self.time)
    # end def compute_occurrences

    @classmethod
    def _change_callback (cls, scope, change) :
        if "date" in change.attr_changes or isinstance \
               (change, MOM.SCM.Change.Create):
            self = change.entity (scope)
            self.compute_occurrences ()
    # end def _change_callback

# end class Event

MOM.SCM.Change.Create.add_callback         (Event, Event._change_callback)
MOM.SCM.Change.Attr.add_callback           (Event, Event._change_callback)

_Ancestor_Essence = GTW.OMP.EVT.Link1

class Event_occurs (_Ancestor_Essence) :
    """Occurrence of a calendary event."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Event that occurs"""

            role_type          = Event
            role_name          = "event"
            auto_cache         = "occurs"

            ### give `date` and `time` priority for sorting
            sort_rank          = 10

        # end class left

        class date (A_Date) :
            """Date of occurrence"""

            kind               = Attr.Primary

        # end class date

        class time (A_Time_Interval) :
            """Time (interval) of occurrence"""

            kind               = Attr.Primary_Optional

        # end class time

        ### Non-primary attributes

        class detail (A_String) :

            kind               = Attr.Computed

            def computed (self, obj) :
                if obj and obj.event :
                    return obj.event.detail
            # end def computed

        # end class detail

        class electric (_Ancestor.electric) :

            kind       = Attr.Const
            default    = True

        # end class electric

        class essence (_A_Entity_) :

            kind               = Attr.Computed

            def computed (self, obj) :
                if obj and obj.event :
                    return obj.event.object
            # end def computed

        # end class essence

        class short_title (A_String) :

            kind               = Attr.Computed

            def computed (self, obj) :
                if obj and obj.event :
                    return obj.event.short_title
            # end def computed

        # end class short_title

        class title (A_String) :

            kind               = Attr.Computed

            def computed (self, obj) :
                if obj :
                    return obj.event.title
            # end def computed

        # end class title

    # end class _Attributes

# end class Event_occurs

if __name__ != "__main__" :
    GTW.OMP.EVT._Export ("*")
### __END__ GTW.OMP.EVT.Event
