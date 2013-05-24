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
#    TFL.I18N
#
# Purpose
#    Support for internationalization (I18N)
#
# Revision Dates
#    28-Oct-2009 (CT) Creation
#    19-Jan-2010 (CT) `_Tn` changed to make `plural` and `n` optional
#    21-Jan-2010 (MG) Real translation added
#    21-Jan-2010 (CT) Module-level aliases added, `I18N.ungettext` corrected
#    21-Jan-2010 (CT) `load_languages` and `use_language` added
#    21-Jan-2010 (MG) Reworked
#    21-Jan-2010 (MG) `save_eval` added
#    25-Jan-2010 (MG) Support list of languages in `use` and `context`
#    31-Jan-2010 (CT) `import  babel.support` moved inside functions
#    18-Feb-2010 (CT) `Name` added
#    22-Feb-2010 (CT) `choose` factored, `Config.choice` added
#    15-Apr-2010 (MG) `Translations` added and used
#    16-Jun-2010 (CT) `encoding` added
#    16-Jun-2010 (CT) `encoding` changed to Record with fields `file_system`,
#                     `input`, and `output`
#    16-Jun-2010 (CT) s/print/pyk.fprint/
#    17-Jun-2010 (CT) `encode_f` and `encode_o` added
#    18-Jun-2010 (CT) `Translations` factored to `TFL.Babel`
#    18-Jun-2010 (CT) `decode` added
#     4-Aug-2010 (MG) `load`: `log_level` added
#    30-Nov-2010 (CT) s/save_eval/safe_eval/ and removed `strip`-call from it
#    23-Mar-2011 (CT) `_T` defined (instead of aliased) to guard against
#                     empty argument
#    20-Jul-2011 (CT) `_Config_._properties` added
#    20-Jul-2011 (CT) Use encoding information from `TFL.user_config`
#    ��revision-date�����
#--

from   _TFL            import TFL
from   _TFL            import pyk
from   _TFL.Record     import Record
from   _TFL.predicate  import first, split_hst

import _TFL.Decorator
import _TFL.User_Config

import gettext
import locale
import sys

class _Config_ (Record) :

    _properties = ("choice", )

    @property
    def choice (self) :
        """Language choice."""
        return TFL.user_config.language
    # end def choice

    @choice.setter
    def choice (self, value) :
        TFL.user_config.language = value
    # end def choice

# end class _Config_

Config = _Config_ \
   ( Languages  = {"" : gettext.NullTranslations ()}
   , locale_dir = "locale"
   , domains    = ("messages", )
   )
Config.current = Config.Null = Config.Languages [""]

class _Name_ (TFL.Meta.Object) :
    """Translator for names"""

    def __getattr__ (self, name) :
        return _T (name)
    # end def __getattr__

    def __getitem__ (self, key) :
        return _T (key)
    # end def __getitem__

# end class _Name_

def add (self, * languages, ** kw) :
    locale_dir = kw.pop ("locale_dir", Config.locale_dir)
    domains    = kw.pop ("domains",    Config.domains)
    use_lang   = kw.pop ("use", "")
    _load_languages (locale_dir, languages, domains)
    if use_lang :
        use (use_lang)
# end def add

def choose (* lang) :
    def _gen (lang) :
        for l in lang :
            yield l, l
        for l in lang :
            if l :
                a, _, b = split_hst (l, "_")
                yield a, b or a
        yield "", ""
    return first (l for l in _gen (lang) if l [0] in Config.Languages)
# end def choose

@TFL.Contextmanager
def context (* lang) :
    """Temporarily change the translation language
    ### Let's fake some Translations
    >>> from _TFL._Babel.Translations import Translations
    >>> Config.Languages ["l1"] = l1 = Translations ()
    >>> Config.Languages ["l2"] = l2 = Translations ()
    >>> l1._catalog = dict (text1 = u"L1: Text 1", text2 = u"L1: Text 2")
    >>> l2._catalog = dict (text1 = u"L2: Text 1", text2 = u"L2: Text 2")
    >>> _T ("text1")
    u'text1'
    >>> with context ("l1") :
    ...     _T ("text1")
    ...     _T ("text2")
    u'L1: Text 1'
    u'L1: Text 2'
    >>> with context ("l2") :
    ...     _T ("text1")
    ...     _T ("text2")
    u'L2: Text 1'
    u'L2: Text 2'
    """
    old = Config.current, Config.choice
    try :
       use (* lang)
       yield
    finally :
        Config.current, Config.choice = old
# end def context

def decode (s, errors = "replace") :
    """Decode `s` using `TFL.user_config.input_encoding`."""
    if isinstance (s, str) :
        s = pyk.text_type (s, TFL.user_config.input_encoding, errors)
    return s
# end def decode

def encode_f (s, errors = "replace") :
    """Encodes `s` using `TFL.user_config.file_system_encoding`."""
    return s.encode (TFL.user_config.file_system_encoding, errors)
# end def encode_f

def encode_o (s, errors = "replace") :
    """Encodes `s` using `TFL.user_config.output_encoding`."""
    return s.encode (TFL.user_config.output_encoding, errors)
# end def encode_o

def load (* languages, ** kw) :
    locale_dir        = kw.pop ("locale_dir", Config.locale_dir)
    domains           = kw.pop ("domains",    Config.domains)
    use_lang          = kw.pop ("use",        "")
    log_level         = kw.pop ("log_level",  5)
    Config.domains    = domains
    Config.locale_dir = locale_dir
    _load_languages (locale_dir, languages, domains, log_level)
    if use_lang:
        use (use_lang)
# end def load

def _load_languages (locale_dir, languages, domains, log_level) :
    from _TFL._Babel.Translations import Translations
    if not isinstance (domains, (list, tuple)) :
        domains = (domains, )
    first_dom   = domains [0]
    domains     = domains [1:]
    for lang in languages :
        Config.Languages [lang] = lang_trans = Translations.load \
            (locale_dir, lang, first_dom)
        if not isinstance (lang_trans, Translations) and log_level >= 5 :
            pyk.fprint \
                ( "*** Warning, language %s for domain %s not found!"
                % (lang, first_dom)
                )
        for d in domains :
            new_domain = Translations.load (locale_dir, lang, d)
            if not isinstance (new_domain, Translations) and log_level >= 5 :
                pyk.fprint \
                    ( "*** Warning, language %s for domain %s not found!"
                    % (lang, d)
                    )
            lang_trans.merge (new_domain)
# end def _load_languages

def mark (text):
    """Mark `text` for translation."""
    return pyk.text_type (text)
# end def mark

def safe_eval (value, encoding = None) :
    # Found in babel....
    # Unwrap quotes in a safe manner, maintaining the string's encoding
    # https://sourceforge.net/tracker/?func=detail&atid=355470&aid=617979&group_id=5470
    if encoding :
        value = "# coding=%s\n%s" % (encoding, value)
    result = TFL.r_eval (value)
    return result
# end def safe_eval

def ugettext (text, trans = None) :
    """Return the localized translation of `text` (as unicode)."""
    return (trans or Config.current).ugettext (text)
# end def ugettext

def ungettext (singular, plural = None, n = 99, trans = None) :
    """Return the localized translation of `text` for the plural form
       appropriate for `n` (as unicode).
    """
    if plural is None :
        plural = singular + "s"
    return (trans or Config.current).ungettext (singular, plural, n)
# end def ungettext

def use (* lang) :
    Config.choice  = (l, v) = choose (* lang)
    Config.current = Config.Languages [l]
# end def use

_    = mark

def _T (s) :
    if s :
        return ugettext (s)
    return s
# end def _T

_Tn  = ungettext

Name = _Name_ ()

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.I18N
