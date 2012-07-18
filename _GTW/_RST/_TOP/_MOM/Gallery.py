# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.MOM.
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
#    GTW.RST.TOP.MOM.Gallery
#
# Purpose
#    Page displaying a gallery of pictures
#
# Revision Dates
#    18-Jul-2012 (CT) Creation
#    ��revision-date�����
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST._TOP._MOM.Mixin
import _GTW._RST._TOP.Dir
import _GTW._RST._TOP.Page

from   _MOM.import_MOM          import MOM, Q

from   _TFL._Meta.Property      import Alias_Property
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import first

from   posixpath                import join as pp_join

_Ancestor = GTW.RST.TOP.Page

class Picture (_Ancestor) :

    implicit = True

    def __init__ (self, ** kw) :
        obj = kw ["obj"]
        if "name" not in kw :
            kw ["name"] = obj.name
        self.__super.__init__ (** kw)
    # end def __init__

    @Once_Property
    def permalink (self) :
        return self.parent.href_display (self.obj)
    # end def permalink

    @Once_Property
    def photo (self) :
        return self.obj.photo
    # end def photo

    @Once_Property
    def short_title (self) :
        return "%s: %s %s/%s" % \
            ( self.parent.obj.short_title
            , _T ("picture")
            , self.obj.name
            , self.parent.count
            )
    # end def short_title

    @Once_Property
    def thumb (self) :
        return self.obj.thumb
    # end def thumb

# end class Picture

_Ancestor = GTW.RST.TOP.Dir_V

class Gallery \
          ( GTW.RST.TOP.MOM.Entity_Mixin_Base
          , GTW.RST.TOP.MOM.E_Type_Mixin
          , _Ancestor
          ) :
    """Page displaying a gallery of pictures."""

    Entity              = Picture

    dir_template_name   = "gallery"
    page_template_name  = "photo"
    pictures            = Alias_Property ("entries")
    sort_key            = TFL.Sorted_By  ("number")

    _greet_entry        = None

    @Once_Property
    def change_query_filters (self) :
        result = \
            ( Q.pid.IN (self.ETM.query (Q.left == self.obj.pid).attr ("pid"))
            ,
            )
        return result
    # end def change_query_filters

    @Once_Property
    def max_height_photo (self) :
        if self.pictures :
            return max (p.photo.height for p in self.pictures)
        return 0
    # end def max_height_photo

    @Once_Property
    def max_height_thumb (self) :
        if self.pictures :
            return max (p.thumb.height for p in self.pictures)
        return 0
    # end def max_height_thumb

    @Once_Property
    def max_width_photo (self) :
        if self.pictures :
            return max (p.photo.width for p in self.pictures)
        return 0
    # end def max_width_photo

    @Once_Property
    def max_width_thumb (self) :
        if self.pictures :
            return max (p.thumb.width for p in self.pictures)
        return 0
    # end def max_width_thumb

    @Once_Property
    def query_filters (self) :
        return (Q.left == self.obj.pid, )
    # end def query_filters

    def href_display (self, obj) :
        return pp_join (self.abs_href, obj.name)
    # end def href_display

    def is_current_dir (self, page) :
        return False
    # end def is_current_dir

    def is_current_page (self, page) :
        return self.href in (page.href, page.parent.href)
    # end def is_current_page

    def _get_child (self, child, * grandchildren) :
        self.entries ### trigger load from database
        result = self.__super._get_child (child, * grandchildren)
        if result and result.name in self._entry_map :
            ### make sure to use result from `_entry_map`
            ### that allows `1`, `01`, `001`, `0001`, ...
            result = self._entry_map [result.name]
        return result
    # end def _get_child

    def _get_child_query (self, child) :
        try :
            number = int (child.split (".") [0])
        except (TypeError, ValueError) :
            result = None
        else :
            n, result = self.ETM.query_1 (number = number, * self.query_filters)
        if result is None :
            result = self.__super._get_child_query (child)
        return result
    # end def _get_child_query

# end class Gallery

_Ancestor = GTW.RST.TOP.MOM.Display.E_Type_Archive_DSY

class Gallery_Archive (_Ancestor) :
    """Archive of galleries organized by year."""

    class _Gallery_Year_ (_Ancestor.Year) :

        _real_name = "Year"

        Entity     = Gallery

    Year = _Gallery_Year_ # end class

# end class Gallery_Archive

if __name__ != "__main__" :
    GTW.RST.TOP.MOM._Export ("*")
### __END__ GTW.RST.TOP.MOM.Gallery
