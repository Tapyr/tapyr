# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
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
#    GTW.RST.TOP.Console
#
# Purpose
#    Interactive console running in web page
#
# Revision Dates
#    13-Jul-2012 (CT) Creation (based on GTW.NAV.Console)
#    ��revision-date�����
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

from   _TFL._Meta.Once_Property import Once_Property

import _GTW._RST.HTTP_Method
import _GTW._RST._TOP.Dir
import _GTW._RST._TOP.Page

import _TFL.I18N
import _TFL.Py_Interpreter

from   collections              import deque
from   traceback                import format_exception_only
from   xml.sax.saxutils         import escape

import code
import re
import sys

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
RegexType     = type(_paragraph_re)

def _add_subclass_info (inner, obj, base) :
    if isinstance (base, tuple) :
        for b in base :
            if type (obj) is b :
                return inner
    elif type (obj) is base :
        return inner
    module = ""
    if obj.__class__.__module__ not in ("__builtin__", "exceptions") :
        module = '<span class="module">%s.</span>' % obj.__class__.__module__
    return "%s%s(%s)" % (module, obj.__class__.__name__, inner)
# end def _add_subclass_info

class HTML_Repr_Generator (TFL.Meta.Object) :
    """Borrowed from werkzeug: werkzeug.debug.repr"""

    def __init__ (self) :
        self._stack = []
    # end def __init__

    def _sequence_repr_maker (left, right, base = object (), limit = 8) :
        def proxy (self, obj, recursive) :
            if recursive :
                return _add_subclass_info (left + '...' + right, obj, base)
            buf                   = [left]
            have_extended_section = False
            for idx, item in enumerate (obj) :
                if idx :
                    buf.append (', ')
                if idx == limit :
                    buf.append ('<span class="extended">')
                    have_extended_section = True
                buf.append (self.repr (item))
            if have_extended_section :
                buf.append ('</span>')
            buf.append     (right)
            return _add_subclass_info (u''.join (buf), obj, base)
        # end def proxy
        return proxy
    # end def _sequence_repr_maker

    list_repr      = _sequence_repr_maker ('[',           ']',  list)
    tuple_repr     = _sequence_repr_maker ('(',           ')',  tuple)
    set_repr       = _sequence_repr_maker ('set([',       '])', set)
    frozenset_repr = _sequence_repr_maker ('frozenset([', '])', frozenset)

    if deque is not None:
        deque_repr = _sequence_repr_maker \
            ('<span class="module">collections.</span>deque([', '])', deque)
    del _sequence_repr_maker

    def regex_repr (self, obj) :
        pattern = repr (obj.pattern).decode ('string-escape', 'ignore')
        if pattern [:1] == 'u' :
            pattern = 'ur' + pattern [1:]
        else:
            pattern = 'r'  + pattern
        return u're.compile(<span class="string regex">%s</span>)' % pattern
    # end def regex_repr

    def string_repr (self, obj, limit = 70) :
        buf     = ['<span class="string">']
        escaped = escape (obj)
        a       = repr   (escaped [:limit])
        b       = repr   (escaped [limit:])
        if isinstance (obj, unicode) :
            buf.append ('u')
            a = a [1:]
            b = b [1:]
        if b != "''" :
            buf.extend ((a [:-1], '<span class="extended">', b [1:], '</span>'))
        else:
            buf.append (a)
        buf.append     ('</span>')
        return _add_subclass_info (u''.join (buf), obj, (str, unicode))
    # end def string_repr

    def dict_repr (self, d, recursive, limit = 5) :
        if recursive :
            return _add_subclass_info (u'{...}', d, dict)
        buf = ['{']
        have_extended_section = False
        for idx, (key, value) in enumerate (d.iteritems ()) :
            if idx :
                buf.append (', ')
            if idx == (limit - 1) :
                buf.append ('<span class="extended">')
                have_extended_section = True
            buf.append \
                ( '<span class="pair"><span class="key">%s</span>: '
                  '<span class="value">%s</span></span>'
                % (self.repr (key), self.repr (value))
                )
        if have_extended_section :
            buf.append ('</span>')
        buf.append     ('}')
        return _add_subclass_info (u''.join (buf), d, dict)
    # end def dict_repr

    def object_repr (self, obj) :
        return \
            ( u'<span class="object">%s</span>'
            % escape (repr(obj).decode ('utf-8', 'replace'))
            )
    # end def object_repr

    def dispatch_repr (self, obj, recursive) :
        if isinstance (obj, (int, long, float, complex)) :
            return u'<span class="number">%r</span>' % (obj, )
        if isinstance (obj, basestring) :
            return self.string_repr    (obj)
        if isinstance (obj, RegexType) :
            return self.regex_repr     (obj)
        if isinstance (obj, list) :
            return self.list_repr      (obj, recursive)
        if isinstance (obj, tuple) :
            return self.tuple_repr     (obj, recursive)
        if isinstance (obj, set) :
            return self.set_repr       (obj, recursive)
        if isinstance (obj, frozenset) :
            return self.frozenset_repr (obj, recursive)
        if isinstance (obj, dict) :
            return self.dict_repr      (obj, recursive)
        if isinstance (obj, deque) :
            return self.deque_repr     (obj, recursive)
        return self.object_repr        (obj)
    # end def dispatch_repr

    def fallback_repr (self) :
        try:
            info = ''.join (format_exception_only (* sys.exc_info () [:2]))
        except :
            info = '?'
        return \
            ( u'<span class="brokenrepr">&lt;broken repr (%s)&gt;'
              u'</span>' % escape (info.decode ('utf-8', 'ignore').strip ())
            )
    # end def fallback_repr

    def repr (self, obj) :
        recursive = False
        for item in self._stack :
            if item is obj :
                recursive = True
                break
        self._stack.append (obj)
        try :
            try :
                return self.dispatch_repr (obj, recursive)
            except :
                return self.fallback_repr ()
        finally :
            self._stack.pop ()
    # end der repr

# end class HTML_Repr_Generator

class _Py_Console_ (code.InteractiveInterpreter) :

    class HTML_String_O (TFL.Meta.Object) :
        """A StringO version which escapes HTML entities."""

        def __init__ (self) :
            self._lines   = []
            self.repr_gen = HTML_Repr_Generator ()
        # end def __init__

        def consume (self) :
            result      = "".join (self._lines)
            self._lines = []
            return result
        # end def consume

        def write (self, line) :
            self._write (escape (line))
        # end def write

        def _write (self, line) :
            self._lines.append (line)
        # end def _write

        def displayhook (self, obj) :
            self._write (self.repr_gen.repr (obj))
        # end def displayhook

    # end class HTML_String_O

    def __init__ (self, locls = None, globls = None) :
        self.globals      = globls if globls is not None else globals ()
        self._history     = []
        self._histptr     = 0
        self.output       = self.HTML_String_O ()
        self.more         = False
        self.input_buffer = []
        code.InteractiveInterpreter.__init__ \
            (self, locls if locls is not None else {})
    # end def __init__

    def update_locals (self, ** kw) :
        self.locals.update (kw)
    # end def update_locals

    def runsource (self, source) :
        source = source.rstrip() + '\n'
        prompt = self.more and '... ' or '>>> '
        try :
            source_to_eval = ''.join (self.input_buffer + [source])
            with TFL.Context.attr_let \
                ( sys
                , stdout      = self.output
                , displayhook = self.output.displayhook
                ) :
                if code.InteractiveInterpreter.runsource \
                    (self, source_to_eval, "<debugger>", "single") :
                    self.more = True
                    self.input_buffer.append (source)
                else:
                    self.more          = False
                    self.input_buffer  = []
        finally :
            output = self.output.consume ()
        return prompt + source + output
    # end def runsource

    def runcode (self, code) :
        try:
            exec code in self.globals, self.locals
        except:
            self.showtraceback ()
    # end def runcode

    def showtraceback (self) :
        from werkzeug.debug.tbtools import get_current_traceback
        tb = get_current_traceback (skip=1)
        sys.stdout._write (tb.render_summary ())
    # end def showtraceback

    def showsyntaxerror (self, filename = None) :
        from werkzeug.debug.tbtools import get_current_traceback
        tb = get_current_traceback (skip=4)
        sys.stdout._write (tb.render_summary ())
    # end def showsyntaxerror

    def write (self, data) :
        sys.stdout.write (data)
    # end def write

    def __call__ (self, cmd) :
        return self.runsource (cmd)
    # end def __call__

# end class _Py_Console_

_Ancestor = GTW.RST.TOP.Page

class Console (_Ancestor) :
    """Interactive console running in web page."""

    template_name     = "console"
    completion_cutoff = None

    class Console_GET (_Ancestor.GET) :

        _real_name             = "GET"
        _renderers             = \
            _Ancestor.GET._renderers + (GTW.RST.Mime_Type.JSON, )

        def _get_renderer (self, resource, request, response) :
            req_data = request.req_data
            cmd      = req_data.get ("cmd")
            complete = req_data.get ("complete")
            if cmd or complete :
                return GTW.RST.Mime_Type.JSON (self, resource, request)
            else :
                return self.__super._get_renderer (resource, request, response)
        # end def _get_renderer

        def _response_body (self, resource, request, response) :
            req_data = request.req_data
            cmd      = req_data.get ("cmd")
            complete = req_data.get ("complete")
            console  = resource.console
            if complete :
                input, cands = TFL.complete_command \
                    (complete, console.globals, console.locals)
                cands        = cands.strip ().split (",")
                completed    = False
                if len (cands) == 1 :
                    if len (input) >= len (complete) :
                        completed = True
                    else :
                        input     = complete
                elif (   (resource.completion_cutoff is not None)
                     and (len (cands) > resource.completion_cutoff)
                     ) :
                    cands        = \
                        [ TFL.I18N._T
                           ("There are %s possible completions" % (len (cands)))
                        ]
                return dict \
                    ( input     = input
                    , cands     = ", ".join (cands)
                    , completed = completed
                    )
            elif cmd :
                console.update_locals \
                    ( request  = request
                    , response = response
                    )
                return dict \
                    ( html = console (cmd)
                    , more = console.more
                    )
            else :
                top     = resource.top
                referer = request.referrer
                if top and referer :
                    url = TFL.Url (referer)
                    console.update_locals \
                        ( last_page      = top.resource_from_href (url.path)
                        , last_request   = request
                        , last_response  = response
                        , referrer       = url
                        , request        = request
                        , response       = response
                        )
                return self.__super._response_body (resource, request, response)
        # end def _response_body

    # end class Console_GET


    @Once_Property
    def console (self) :
        top = self.top
        return _Py_Console_ \
            ( dict
                ( getattr (top, "console_context", {})
                , NAV   = top
                , page  = self
                , scope = top.scope
                )
            )
    # end def console

# end class Console

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("*")
### __END__ GTW.RST.TOP.Console