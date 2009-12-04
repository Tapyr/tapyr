# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer All rights reserved
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
#    TFL.Q_Exp
#
# Purpose
#    Query expression language
#
# Revision Dates
#     4-Dec-2009 (CT) Creation
#    ��revision-date�����
#--

"""
This module implements a query expression language:

>>> from _TFL.Record import Record as R
>>> r1 = R (foo = 42, bar = 137, baz = 11)
>>> q0 = Q.foo
>>> q0.name
'foo'
>>> q0.predicate (r1)
42

>>> q1 = Q.foo == Q.bar
>>> q1
Q.foo == Q.bar
>>> q1.lhs.name, q1.rhs.name
('foo', 'bar')
>>> q1 = Q.foo == Q.bar
>>> q1.predicate (r1)
False

>>> q2 = Q.foo + Q.bar
>>> q2, q2.lhs, q2.rhs
(Q.foo + Q.bar, Q.foo, Q.bar)
>>> q2.predicate (r1)
179

>>> q3 = Q.foo % Q.bar == Q.baz
>>> q3, q3.lhs, q3.rhs
(Q.foo % Q.bar == Q.baz, Q.foo % Q.bar, Q.baz)
>>> q3.predicate (r1)
False
>>> q4 = Q.bar % Q.foo
>>> q4.predicate (r1), Q.baz.predicate (r1)
(11, 11)
>>> (q4 == Q.baz).predicate (r1)
True
>>> q3.lhs.predicate (r1)
42

>>> QQ = Q.__class__ (Ignore_Exception = AttributeError)
>>> QQ.qux.predicate (r1)
>>> Q.qux.predicate (r1)
Traceback (most recent call last):
  ...
AttributeError: qux

>>> Q [0] ((2,4))
2
>>> Q [1] ((2,4))
4
>>> Q [-1] ((2,4))
4
>>> Q [-2] ((2,4))
2

"""

from   _TFL                     import TFL

import _TFL._Meta.Object
import _TFL.Decorator

from   _TFL.predicate           import callable

import operator

class Base (TFL.Meta.Object) :
    """Query generator"""

    class Ignore_Exception (StandardError) : pass

    def __init__ (self, Ignore_Exception = None) :
        if Ignore_Exception is not None :
            self.Ignore_Exception = Ignore_Exception
    # end def __init__

    def __getattr__ (self, name) :
        assert "." not in name, name
        return self.Get (self, name, operator.attrgetter (name))
    # end def __getattr__

    def __getitem__ (self, item) :
        assert not isinstance (item, slice)
        return self.Get (self, item, operator.itemgetter (item))
    # end def __getitem__

# end class Base

@TFL.Add_New_Method (Base)
class Bin (TFL.Meta.Object) :
    """Binary query expression"""

    op_map        = dict \
        ( __add__ = "+"
        , __div__ = "/"
        , __eq__  = "=="
        , __ge__  = ">="
        , __gt__  = ">"
        , __le__  = "<="
        , __lt__  = "<"
        , __mod__ = "%"
        , __mul__ = "*"
        , __pow__ = "**"
        , __sub__ = "-"
        )

    predicate_precious_p = True

    def __init__ (self, lhs, op, rhs) :
        self.Q    = lhs.Q
        self.lhs  = lhs
        self.op   = op
        self.rhs  = rhs
    # end def __init__

    def predicate (self, obj) :
        l = self.lhs.predicate (obj)
        try :
            pred = self.rhs.predicate
        except AttributeError :
            r = self.rhs
        else :
            r = pred (obj)
        if l is not None and r is not None :
            return self.op (l, r)
    # end def predicate

    def __repr__ (self) :
        op = self.op.__name__
        return "%s %s %s" % (self.lhs, self.op_map.get (op, op), self.rhs)
    # end def __repr__

# end class Bin

@TFL.Add_New_Method (Base)
class Call (TFL.Meta.Object) :
    """Query expression calling a method."""

    predicate_precious_p = True

    def __init__ (self, lhs, op, * args, ** kw) :
        self.Q           = lhs.Q
        self.lhs         = lhs
        self.op          = op
        self.attr_args   = args
        self.attr_kw     = kw
    # end def __init__

    def predicate (self, obj) :
        l = self.lhs.predicate (obj)
        return self.op (l, * self.attr_args, ** self.attr_kw)
    # end def predicate

# end class Call

def __binary (op, Class) :
    name = op.__name__
    op   = getattr (operator, op.__name__)
    def _ (self, rhs) :
        return getattr (self.Q, Class) (self, op, rhs)
    _.__doc__    = op.__doc__
    _.__name__   = name
    _.__module__ = op.__module__
    return _
# end def __binary

def _binary (op) :
    return __binary (op, "Bin_Expr")
# end def _binary

def _boolean (op) :
    return __binary (op, "Bin_Bool")
# end def _boolean

def _method (meth) :
    name = meth.__name__
    op   = meth ()
    def _ (self, * args, ** kw) :
        return self.Q.Call (self, op, * args, ** kw)
    _.__doc__    = op.__doc__
    _.__name__   = name
    _.__module__ = meth.__module__
    return _
# end def _method

@TFL.Add_New_Method (Base)
class Exp (TFL.Meta.Object) :
    """Query expression"""

    ### Boolean queries
    @_boolean
    def __eq__ (self, rhs) : pass

    @_boolean
    def __ge__ (self, rhs) : pass

    @_boolean
    def __gt__ (self, rhs) : pass

    @_boolean
    def __le__ (self, rhs) : pass

    @_boolean
    def __lt__ (self, rhs) : pass

    @_boolean
    def __ne__ (self, rhs) : pass

    def __hash__ (self) :
        ### Override `__hash__` just to silence DeprecationWarning:
        ###     Overriding __eq__ blocks inheritance of __hash__ in 3.x
        raise NotImplementedError
    # end def __hash__

    ### Binary non-boolean queries
    @_binary
    def __add__ (self, rhs) : pass

    @_binary
    def __div__ (self, rhs) : pass

    @_binary
    def __mod__ (self, rhs) : pass

    @_binary
    def __mul__ (self, rhs) : pass

    @_binary
    def __pow__ (self, rhs) : pass

    @_binary
    def __sub__ (self, rhs) : pass

    ### Method calls
    @_method
    def between () :
        def between (val, lhs, rhs) :
            """between(val, lhs, rhs) -- Returns result of `lhs <= val <= rhs`"""
            return lhs <= val <= rhs
        return between
    # end def between

    @_method
    def contains () :
        return operator.contains
    # end def contains

    @_method
    def endswith () :
        return str.endswith
    # end def endswith

    @_method
    def in_ () :
        def in_ (val,  rhs) :
            """in_(val, lhs) -- Returns result of `val in rhs`"""
            return val in rhs
        return in_
    # end def in_

    @_method
    def startswith () :
        return str.startswith
    # end def startswith

# end class Exp

@TFL.Add_New_Method (Base)
class Get (Exp) :
    """Query getter"""

    predicate_precious_p = True

    def __init__ (self, Q, name, getter) :
        self.Q      = Q
        self.name   = name
        self.getter = getter
    # end def __init__

    def predicate (self, obj) :
        try :
            return self.getter (obj)
        except self.Q.Ignore_Exception :
            pass
    # end def predicate

    def __call__ (self, obj) :
        return self.predicate (obj)
    # end def __call__

    def __repr__ (self) :
        return "Q.%s" % self.name
    # end def __repr__

# end class Get

@TFL.Add_New_Method (Base)
class _Q_Exp_Bin_Bool_ (Bin) :
    """Binary query expression evaluating to boolean"""

    _real_name = "Bin_Bool"

Bin_Bool = _Q_Exp_Bin_Bool_ # end class

@TFL.Add_New_Method (Base)
class _Q_Exp_Bin_Expr_ (Bin, Exp) :
    """Binary query expression"""

    _real_name = "Bin_Expr"

Bin_Expr = _Q_Exp_Bin_Expr_ # end class

Q = Base ()

if __name__ != "__main__" :
    TFL._Export ("Q")
    TFL._Export_Module ()
### __END__ TFL.Q_Exp
