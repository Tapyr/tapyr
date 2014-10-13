# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL._pyk3
#
# Purpose
#    Python3 specific implementation of TFL.pyk
#
# Revision Dates
#    16-Jun-2010 (CT) Creation
#     5-Jan-2011 (CT) `pickle` added
#    23-May-2013 (CT) Add `string_types`, `text_type`, `Classic_Class_Type`
#    23-May-2013 (CT) Add class decorator `adapt__bool__`
#    24-May-2013 (CT) Add `adapt__div__`, `adapt__str__`
#    24-May-2013 (CT) Add `iteritems`, `iterkeys`, `itervalues`, `xrange`
#    24-May-2013 (CT) Add `int_types`
#    25-May-2013 (CT) Add `new_instancemethod`, `izip`, `zip`
#    26-May-2013 (CT) Convert to class/instance to allow lazy imports
#    28-May-2013 (CT) Fix `new_instancemethod`
#     9-Oct-2013 (CT) Fix `zip`, `izip`
#    27-Nov-2013 (CT) Add `number_types`
#     3-Jan-2014 (CT) Add `encoded`, `user_config`
#    17-Feb-2014 (CT) Add `decoded`
#    22-Aug-2014 (CT) Allow multiple `encodings` for `encoded`
#     7-Oct-2014 (CT) Change `iter*` to wrap `result` in `iter`
#     7-Oct-2014 (CT) Add `config_parser`, `ifilter`, `reprify`
#     7-Oct-2014 (CT) Fix `encoded`
#     9-Oct-2014 (CT) Add `builtins`
#    10-Oct-2014 (CT) Add `urlencode`, `urlparse`
#    13-Oct-2014 (CT) Add `byte_type`
#    ««revision-date»»···
#--

import functools

def lazy_property (fct) :
    name = fct.__name__
    @functools.wraps (fct)
    def _ (self) :
        try :
            result = self.__dict__ [name]
        except KeyError :
            result = self.__dict__ [name] = fct (self)
        return result
    return property (_)
# end def lazy_property

class _Pyk_ (object) :
    """Python2 specific implementation of TFL.pyk.

       Use a class instead of module-level definitions to allow lazy imports.
    """

    @staticmethod
    def adapt__bool__ (cls) :
        dct = cls.__dict__
        if "__bool__" not in dct and "__nonzero__" in dct :
            setattr (cls, "__bool__", dct ["__nonzero__"])
        return cls
    # end def adapt__bool__

    @staticmethod
    def adapt__div__ (cls) :
        """Nothing to be done here"""
        return cls
    # end def adapt__div__

    @staticmethod
    def adapt__str__ (cls) :
        """Nothing to be done here"""
        return cls
    # end def adapt__str__

    @lazy_property
    def builtins (self) :
        import builtins
        return builtins
    # end def builtins

    byte_type  = bytes
    byte_types = (bytes, )

    @lazy_property
    def config_parser (self) :
        import configparser
        return configparser
    # end def config_parser

    Classic_Class_Type = None

    @staticmethod
    def decoded (v, * encodings) :
        if not encodings :
            encodings = [pyk.user_config.input_encoding]
        if isinstance (v, bytes) :
            for encoding in encodings :
                try :
                    v = v.decode (encoding, "replace")
                except Exception as exc :
                    pass
                else :
                    break
            else :
                raise exc
        elif not isinstance (v, str) :
            v = str (v)
        return v
    # end def decoded

    @staticmethod
    def encoded (v, encoding = None) :
        if encoding is None :
            encoding = pyk.user_config.output_encoding
        if not isinstance (v, str) :
            v = str (v)
        if isinstance (v, str) :
            v = v.encode (encoding, "replace")
        return v
    # end def encoded

    fprint             = staticmethod (print)
    int_types          = (int, )

    @staticmethod
    def iteritems (dct) :
        try :
            items = dct.items
        except AttributeError :
            items = dct.iteritems
        return iter (items ())
    # end def iteritems

    @staticmethod
    def iterkeys (dct) :
        try :
            keys = dct.keys
        except AttributeError :
            keys = dct.iterkeys
        return iter (keys ())
    # end def iterkeys

    @staticmethod
    def itervalues (dct) :
        try :
            values = dct.values
        except AttributeError :
            values = dct.itervalues
        return iter (values ())
    # end def itervalues

    ifilter    = staticmethod (filter)
    izip       = staticmethod (zip)
    long_types = (type ("no_longin_in_Py3", (object, ), {}), )

    @staticmethod
    def new_instancemethod (function, instance, cls) :
        if instance is None :
            @functools.wraps (function)
            def _ (* args, ** kw) :
                return function (* args, ** kw)
            return _
        else :
            return function
    # end def new_instancemethod

    number_types = (int, float)

    @lazy_property
    def pickle (self) :
        import pickle
        return pickle
    # end def pickle

    xrange = staticmethod (range)

    @staticmethod
    def range (* args, ** kw) :
        return list (range (* args, ** kw))
    # end def range

    @staticmethod
    def reprify (r) :
        return pyk.decoded (r)
    # end def reprify

    @lazy_property
    def StringIO (self) :
        import io
        return io.StringIO
    # end def StringIO

    string_types       = (str, )
    text_type          = str
    unichr             = chr

    @lazy_property
    def urlencode (self) :
        from urllib.parse import urlencode
        return urlencode
    # end def urlencode

    @lazy_property
    def urlparse (self) :
        from urllib import parse
        return parse
    # end def urlparse

    @lazy_property
    def user_config (self) :
        from   _TFL.User_Config import user_config
        return user_config
    # end def user_config

    def zip (self, * args) :
        return list (self.izip (* args))
    # end def zip

# end class _Pyk_

pyk = _Pyk_ ()

### __END__ TFL._pyk3
