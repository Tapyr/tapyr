# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.rst_harness
#
# Purpose
#    Harness for testing RESTful apis
#
# Revision Dates
#     9-Jan-2013 (CT) Creation (factor from RST)
#    31-Jan-2013 (CT) Change `_main` to use `Backend_Default_Path`
#    31-Jan-2013 (CT) Use `url.scheme` as default `db_name` extension in
#                     `run_server`
#    31-Jan-2013 (CT) Fix setting of `db_name` in `_main`
#    12-Feb-2013 (CT) Increase timeout and number of tries in `run_server`
#    28-Mar-2013 (CT) Add `skip_headers`
#    28-Mar-2013 (CT) Register `p.terminate` in `Scaffold.reset_callbacks`
#     2-May-2013 (CT) Add `sleep(1)` to begin of `run_server`
#                     to avoid spurious errors
#     3-May-2013 (CT) Add `scaffold_name` to `run_server`;
#                     add `normalize_json` to `show`; add `** kw` to `traverse`
#     3-May-2013 (CT) Add `date_cleaner`
#     4-May-2013 (CT) Add `set-copy` to`skip_headers`
#    31-Mar-2014 (CT) Add `default_value` for `<date instance>` to `date_cleaner`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW.__test__.Test_Command import *

from   _TFL.Regexp                import Multi_Re_Replacer, Re_Replacer, re

from   posixpath import join as pp_join

import multiprocessing
import requests
import subprocess
import sys
import time

skip_headers = set (["connection", "set-cookie", "x-frame-options"])

date_cleaner = Multi_Re_Replacer \
    ( Re_Replacer
        ( r"'date' : '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'"
        , r"'date' : <datetime>"
        )
    , Re_Replacer
        ( r"'default_value' : '\d{4}-\d{2}-\d{2}'"
        , r"'date' : <date instance>"
        )
    )

def req_json (r) :
    if r is not None and r.content :
        result = r.json
        if TFL.callable (result) :
            try :
                result = result ()
            except Exception :
                result = None
        return result
# end def req_json

def _run_server (Scaffold, args = []) :
    print (["run_server"] + server_args + args)
    result = Scaffold (["run_server"] + server_args + args)
    return result
# end def run_server

def run_server \
        ( test_module_name
        , db_url        = "hps://"
        , db_name       = None
        , scaffold_name = "Scaffold"
        ) :
    import socket
    import tempfile
    import _TFL.Url
    import _TFL.Caller
    time.sleep (1)
    url = TFL.Url (db_url)
    if not db_name :
        db_name = "test.%s" % (url.scheme, )
    cmd = \
        [ sys.executable, "-c"
        , "; ".join
            ( ( "import %s" % (test_module_name, )
              , "%s.%s" % (test_module_name, scaffold_name)
              + "( "
              + repr
                  ( ["run_server"]
                  + server_args
                  + ["-db_url", db_url, "-db_name", db_name]
                  )
              + ")"
              )
            )
        ]
    tf = tempfile.NamedTemporaryFile (delete = False)
    print \
        ( "Using", tf.name, "as stdout/stderr for server process"
        , file=sys.stderr
        )
    p = subprocess.Popen (cmd, stderr = tf, stdout = tf)
    s = socket.socket    (socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout         (2.0)
    i   = 0
    while True :
        try :
            s.connect (("localhost", 9999))
        except socket.error as exc :
            if i < 30 :
                i += 1
                time.sleep (1)
            else :
                break
        else :
            exc = None
            break
    s.close ()
    if exc is not None :
        print  ("Socket connect gave exception:", exc)
        p.kill ()
    caller_scope = TFL.Caller.Scope (1)
    caller_scope.Scaffold.reset_callbacks.append (p.terminate)
    return p
# end def run_server

def _normal (k, v) :
    if k in ("date", "last-modified") :
        v = "<datetime instance>"
    elif k in ("etag",) :
        v = "ETag value"
    elif k in ("RAT",) :
        v = "<REST authorization token>"
    elif k == "content-length" and int (v) != 0 :
        v = "<length>"
    elif k == "server" :
        v = "<server>"
    return k, v
# end def _normal

def show (r, ** kw) :
    normalize_json = kw.pop ("normalize_json", False)
    cleaner        = kw.pop ("cleaner", False)
    json = req_json (r)
    if json is not None :
        if normalize_json :
            json = dict ( _normal (k, v) for k, v in pyk.iteritems (json))
        kw ["json"] = json
    elif r.content :
        kw ["content"] = r.content.replace ("\r", "").strip ().split ("\n")
    output = formatted \
        ( dict
            ( status  = r.status_code
            , url     = r.url
            , ** kw
            )
        )
    if cleaner :
        output = cleaner (output)
    print (output)
    return r
# end def show

def showf (r, ** kw) :
    return show \
        ( r
        , headers = dict
            ( _normal (k, v) for k, v in pyk.iteritems (r.headers)
            if k.lower () not in skip_headers
            )
        , ** kw
        )
# end def showf

def traverse (url, level = 0, seen = None, ** kw) :
    if seen is None :
        seen = set ()
    rg    = requests.get     (url, ** kw)
    ro    = requests.options (url, ** kw)
    path  = requests.utils.urlparse (url).path or "/"
    if ro.ok :
        allow = ro.headers ["allow"]
        if allow not in seen :
            print (path, ":", allow)
            seen.add (allow)
    else :
        print (path, ":", ro.status_code, ro.content)
    if rg.ok :
        json = req_json (rg)
        if json :
            l = level + 1
            for e in json.get ("entries", ()) :
                traverse ("http://localhost:9999" + str (e), l, seen, ** kw)
# end def traverse

class Requester (TFL.Meta.Object) :
    """Wrapper for `requests`"""

    class W (TFL.Meta.Object) :

        def __init__ (self, name, prefix) :
            self.method = getattr (requests, name)
            self.prefix = prefix
        # end def __init__

        def __call__ (self, path, * args, ** kw) :
            kw.setdefault ("headers", { "Content-Type": "application/json" })
            url = pp_join (self.prefix, path.lstrip ("/"))
            return self.method (url, * args, ** kw)
        # end def __call__

    # end class W

    def __init__ (self, prefix) :
        self.prefix = prefix
    # end def __init__

    def __getattr__ (self, name) :
        return self.W (name, self.prefix)
    # end def __getattr__

# end class Requester

R = Requester ("http://localhost:9999")

server_args = \
    [ "-UTP=RST"
    , "-auto_reload=no"
    , "-debug=no"
    , "-load_I18N=no"
    , "-log_level=0"
    , "-port=9999"
    ]

def _main (Scaffold) :
    backend = sos.environ.get \
        ("GTW_test_backends", "HPS").split (":") [0].strip ()
    db_url  = Scaffold.Backend_Parameters.get   (backend, "hps://").strip ("'")
    db_name = Scaffold.Backend_Default_Path.get \
        (backend) or "test.%s" % (backend.lower (), )
    _run_server \
        (Scaffold, ["-db_url", db_url, "-db_name", db_name, "-debug", "no"])
# end def _main

### __END__ GTW.__test__.rst_harness
