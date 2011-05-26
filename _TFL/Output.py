# -*- coding: iso-8859-15 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Output
#
# Purpose
#    Classes for output redirection and stacking
#
# Revision Dates
#    27-Aug-2008 (CT) Creation
#    28-Aug-2008 (CT) `Tee` added
#    ��revision-date�����
#--

from   _TFL           import TFL

import _TFL._Meta.Object

import sys

class Redirect_Std (TFL.Meta.Object) :
    """Redirection of sys.stdout and/or sys.stderr"""

    std_streams = set (("stdout", "stderr"))
    target      = None

    def __init__ (self, target, redirects = ("stdout", )) :
        assert all ((r in self.std_streams) for r in redirects), redirects
        self.target    = target
        self.redirects = map = {}
        for r in redirects :
            map [r] = getattr (sys, r)
            setattr (sys, r, self)
    # end def __init__

    def destroy (self) :
        for r, orig in self.redirects.iteritems () :
            if getattr (sys, r, None) is self :
                setattr (sys, r, orig)
        self.redirects = {}
        try :
            t_destroy = self.target.destroy
        except AttributeError :
            pass
        else :
            t_destroy ()
        self.target = None
    # end def destroy

    def flush (self) :
        try :
            f = self.target.flush
        except AttributeError :
            pass
        else :
            f ()
    # end def flush

    def write (self, text) :
        if self.target is not None :
            self.target.write (text)
    # end def write

# end class Redirect_Std

class Tee (TFL.Meta.Object) :
    """Write output to several streams."""

    def __init__ (self, * streams) :
        self.streams = list (streams)
    # end def __init__

    def add_stream (self, s) :
        streams = self.streams
        if s not in streams :
            streams.append (s)
    # end def add_stream

    def destroy (self) :
        streams = self.streams
        for s in streams :
            try :
                s_destroy = s.destroy
            except AttributeError :
                pass
            else :
                s_destroy ()
        self.streams = []
    # end def destroy

    def flush (self) :
        for s in self.streams :
            try :
                f = s.flush
            except AttributeError :
                pass
            else :
                f ()
    # end def flush

    def remove_stream (self, s) :
        streams = self.streams
        if s in streams :
            streams.remove (s)
    # end def remove_stream

    def write (self, text) :
        for s in self.streams :
            s.write (text)
    # end def write

    def writelines (self, seq) :
        for s in self.streams :
            s.writelines (seq)
    # end def writelines

# end class Tee

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.Output
