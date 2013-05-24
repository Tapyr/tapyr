# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Search_Path
#
# Purpose
#    Model a search path
#
# Revision Dates
#    10-Sep-2009 (CT) Creation
#    11-Sep-2009 (CT) `expand_iter` factored
#    ��revision-date�����
#--

from   _TFL           import TFL
from   _TFL           import sos

import _TFL._Meta.Object
import _TFL.Filename

import errno

class Search_Path (TFL.Meta.Object) :
    """Model a search path.

       >>> @TFL.Contextmanager
       ... def expect_except (* Xs) :
       ...     try :
       ...         yield
       ...     except Xs as exc :
       ...         print (exc)

       >>> sp = Search_Path ("/a", "/b", "/c")
       >>> sp.find ("x", lambda z : z.startswith ("/a"))
       '/a/x'
       >>> sp.find ("x", lambda z : z.startswith ("/b"))
       '/b/x'
       >>> sp.find ("x", lambda z : z.startswith ("/c"))
       '/c/x'
       >>> sp.find ("x/y", lambda z : z.startswith ("/c"))
       '/c/x/y'
       >>> with expect_except (IOError) :
       ...     sp.find ("/x/y", lambda z : z.startswith ("/c"))
       [Errno 2] No such file '/x/y' in search path '/a/:/b/:/c/'
       >>> sp.find ("x/y", lambda z : True)
       '/a/x/y'
       >>> list (sp.find_iter ("x/y", lambda z : True))
       ['/a/x/y', '/b/x/y', '/c/x/y']
       >>> list (sp.find_iter ("x/y", lambda z : z.startswith ("/a")))
       ['/a/x/y']
       >>> list (sp.find_iter ("x/y", lambda z : z.startswith ("/b")))
       ['/b/x/y']
       >>> list (sp.find_iter ("x/y", lambda z : z.startswith ("/c")))
       ['/c/x/y']
    """

    def __init__ (self, * pathes, ** kw) :
        self.pathes       = [TFL.Dirname (p) for p in pathes]
        self.default_pred = kw.pop ("default_pred", sos.path.isfile)
        assert not kw
    # end def __init__

    def expand_iter (self, name) :
        for path in self.pathes :
            yield TFL.Filename (name, path, default_rel = True).name
    # end def expand_iter

    def find (self, name, pred = None) :
        for result in self.find_iter (name, pred) :
            return result
        raise IOError \
            ( errno.ENOENT
            , "No such file '%s' in search path '%s'" % (name, self)
            )
    # end def find

    def find_iter (self, name, pred = None) :
        if pred is None :
            pred = self.default_pred
        for n in self.expand_iter (name) :
            if pred (n) :
                yield n
    # end def find_iter

    def __str__ (self) :
        return sos.pathsep.join (p.name for p in self.pathes)
    # end def __str__

# end class Search_Path

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Search_Path
