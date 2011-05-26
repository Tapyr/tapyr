# -*- coding: iso-8859-15 -*-
# Copyright (C) 2001-2004 Mag. Christian Tanzer. All rights reserved
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
#    Ratio
#
# Purpose
#    Model ratio of two integer numbers
#
# Revision Dates
#     4-Sep-2001 (CT)  Creation
#     5-Sep-2001 (CT)  Error messages for `TypeError` improved
#    12-Aug-2003 (CT)  doctest fixed
#     9-Mar-2004 (CT)  `_doc_test` changed to not use `import`
#    28-Sep-2004 (CT)  Use `isinstance` instead of type comparison
#     8-Feb-2005 (CED) Various improvements
#     9-Feb-2005 (CED) Some simplifications done
#    24-Mar-2005 (CT)  Use `Math_Func.gcd` instead of `predicate.gcd`
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ��revision-date�����
#--



from   _TFL           import TFL
from   _TFL.Regexp    import Regexp, re

import Math_Func

class Ratio :
    """Model ratio of two integer numbers.

       >>> print Ratio (1, 2)
       1 / 2
       >>> print Ratio (2)
       2 / 1
       >>> print Ratio ("3/4")
       3 / 4
       >>> print Ratio ("3")
       3 / 1
       >>> print Ratio (1, 2) * Ratio (1, 4)
       1 / 8
       >>> print Ratio (1, 2) / Ratio (1, 4)
       2 / 1
       >>> print Ratio (1, 2) * Ratio ("3")
       3 / 2
       >>> print Ratio (1, 2) * 3
       3 / 2
       >>> print Ratio (1, 2) * 3.
       3 / 2
       >>> print 6 * Ratio (1, 2)
       3 / 1
       >>> print 6 / Ratio (1, 2)
       12 / 1
       >>> print Ratio (1, 2) / 6
       1 / 12
       >>> print Ratio (1, 2) / 6.
       1 / 12
       >>> print 1 / Ratio (1, 2)
       2 / 1
       >>> print Ratio (3, 4).reciprocal ()
       4 / 3
       >>> print Ratio (6, 8).normalized ()
       3 / 4
       >>> print Ratio (1, -2).normalized ()
       -1 / 2
       >>> print Ratio (1, 2).inversed ()
       -1 / 2
       >>> print Ratio (1, 3) + Ratio (1, 4)
       7 / 12
       >>> print Ratio (1, 3) - Ratio (1, 4)
       1 / 12
       >>> print 1 - Ratio (1, 3)
       2 / 3
    """

    pattern = Regexp \
        ( r"^\s*"
          r"(?P<n> \d+)"
          r"(?: "
          r"\s* / \s*"
          r"(?P<d> \d+)"
          r")?"
          r"\s*$"
        , re.X
        )

    def __init__ (self, n, d = None) :
        if isinstance (n, str) :
            if not d is None :
                raise TypeError, \
                    "Ratio() 2nd argument not allowed when 1st is a string"
            if self.pattern.match (n) :
                self.n = int (self.pattern.group ("n"))
                self.d = int (self.pattern.group ("d") or 1)
            else :
                raise ValueError, "invalid literal for Ratio(): %s" % (n, )
        elif isinstance (n, Ratio) :
            if not d is None :
                raise TypeError, \
                    "Ratio() 2nd argument not allowed when 1st is a Ratio"
            self.n = n.n
            self.d = n.d
        elif d == 0 :
            raise TypeError, "Ratio() zero not allowed for denominator"
        else :
            try :
                self.n = int (n)
                self.d = int (d or 1)
            except TypeError :
                print "invalid arguments for Ratio: (%r, %r)" % (n, d)
                raise
    # end def __init__

    def inversed (self) :
        result = self.__class__ (- self.n, self.d)
        return result
    # end def inversed

    def reciprocal (self) :
        result = self.__class__ (self.d, self.n)
        return result
    # end def reciprocal

    def normalize (self) :
        b = Math_Func.gcd (self.n, self.d)
        self.n //= b
        self.d //= b
        if self.d < 0 :
            self.n *= -1
            self.d *= -1
    # end def normalize

    def normalized (self) :
        result = self.__class__ (self)
        result.normalize ()
        return result
    # end def normalized

    def __int__ (self) :
        return int (self.n / self.d)
    # end def __int__

    def __float__ (self) :
        return float (self.n / (1.0 * self.d))
    # end def __float__

    def __str__ (self) :
        return "%s / %s" % (self.n, self.d)
    # end def __str__

    def __repr__ (self) :
        return "Ratio (%r)" % (str (self), )
    # end def __repr__

    def __imul__ (self, rhs) :
        if not isinstance (rhs, Ratio) :
            rhs = self.__class__ (rhs)
        self.n *= rhs.n
        self.d *= rhs.d
        self.normalize ()
        return self
    # end def __imul__

    def __mul__ (self, rhs) :
        result  = self.__class__ (self)
        result *= rhs
        return result
    # end def __mul__

    __rmul__ = __mul__

    def __idiv__ (self, rhs) :
        if not isinstance (rhs, Ratio) :
            rhs = self.__class__ (rhs)
        self   *= rhs.reciprocal ()
        return self
    # end def __idiv__

    def __div__ (self, rhs) :
        result  = self.__class__ (self)
        result /= rhs
        return result
    # end def __div__

    def __rdiv__ (self, lhs) :
        ### XXX CED: Originally this one did not return a `Ratio` instance,
        ### XXX but tried to keep the type of `lhs` ?
        ### XXX If this would be preferable, all the other `__rXXX__`
        ### XXX functions should do this also. Therefore `__rmul__`
        ### XXX and `__radd__` should be implemented
        return lhs * self.reciprocal ()
    # end def __rdiv__

    def __iadd__ (self, rhs) :
        if not isinstance (rhs, Ratio) :
            rhs = self.__class__ (rhs)
        self.n  = (self.n * rhs.d) + (rhs.n * self.d)
        self.d *= rhs.d
        self.normalize ()
        return self
    # end def __iadd__

    def __add__ (self, rhs) :
        result  = self.__class__ (self)
        result += rhs
        return result
    # end def __add__

    __radd__ = __add__

    def __isub__ (self, rhs) :
        if not isinstance (rhs, Ratio) :
            rhs = self.__class__ (rhs)
        self   += rhs.inversed ()
        return self
    # end def __isub__

    def __sub__ (self, rhs) :
        result  = self.__class__ (self)
        result -= rhs
        return result
    # end def __sub__

    def __rsub__ (self, lhs) :
        return lhs + self.inversed ()
    # end def __rsub__

    def __cmp__ (self, rhs) :
        if rhs is None :
            return cmp (float (self), rhs)
        else :
            if not isinstance (rhs, Ratio) :
                rhs = self.__class__ (rhs)
            return cmp (float (self), float (rhs))
    # end def __cmp__

# end class Ratio

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ Ratio
