# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    PMA.TKT.Application
#
# Purpose
#    Implement toolkit-specific functionality of PMA
#
# Revision Dates
#    20-May-2005 (CT) Creation
#    ��revision-date�����
#--

from   _PMA               import PMA
import _PMA._TKT
import _PMA._TKT.Mixin

class _Application_ (PMA.TKT.Mixin) :

    cmd                   = property (lambda s : s.model.cmd)
    verbose               = property (lambda s : s.model.verbose)

    def __init__ (self, model, ** kw) :
        self.__super.__init__ (model.AC, ** kw)
        self.message               = model.AC.ui_state.message = None
        self.gauge                 = model.AC.ui_state.gauge   = None
        self.State                 = model.AC.memory
        self.model                 = model
        self.queued_stdout         = None
    # end def __init__

    def echo (self, * msg, ** kw) :
        verbose = kw.get ("verbose", self.default_verbosity)
        if self.verbose >= verbose :
            for m in msg :
                print m,
            if msg :
                print
    # end def echo

    def _destroy (self) :
        self.queued_stdout.destroy ()
    # end def _destroy

    def _kill_interact (self, event = None) :
        model = self.model
        if model.ipreter :
            model.ipreter.destroy ()
            model.ipreter = None
    # end def _kill_interact

    def _setup_clipboard (self) : ### XXX ???
        self.clipboard = self.AC.ui_state.clipboard = self.ANS.UI.Clipboard \
            (AC = self.AC)
    # end def _setup_clipboard

    def _setup_context_menu (self) :
        pass
    # end def _setup_context_menu

    def _setup_stdout_redirect (self) :
        self.queued_stdout = self.TNS.Queued_Stdout \
            (self.message, redirect_stderr = True)
    # end def _setup_stdout_redirect

    def _write_bug_info (self, file) :
        if self.message :
            sep   = "\n" + ("-" * 79) + "\n"
            write = file.write
            write (sep)
            write ("Contents of message window")
            write (sep)
            write (self.message.get ())
            write ("\n")
    # end def _write_bug_info

Application = _Application_

if __name__ != "__main__" :
    PMA.TKT._Export ("*")
### __END__ PMA.TKT.Application
