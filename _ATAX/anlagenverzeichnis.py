#!/swing/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002-2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
# ****************************************************************************
# This python module is part of Christian Tanzer's public python library
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
#    anlagenverzeichnis
#
# Purpose
#    Manage depreciations (as required by Austrian tax law)
#
# Revision Dates
#    12-Feb-2002 (CT) Creation (rewrite of perl code)
#    19-Jan-2003 (CT) Rest value made dependent on target_currency, instead
#                     of source_currency
#    19-Jan-2003 (CT) `-Start_year` added
#    19-Jan-2003 (CT) Don't show entries totally depreciated
#    22-Dec-2003 (CT) `Anlagen_Entry.evaluate` changed to not add
#                     non-contemporary entries to totals
#    19-Feb-2006 (CT) Import from packages _ATAX and _TFL
#    11-Feb-2007 (CT) `string` functions replaced by `str` methods
#    ��revision-date�����
#--

from _ATAX.accounting import *
from _TFL.Regexp      import *

class _Base :

    def _setup_dates (self, target_year) :
        self.head_date       = "1.1.%s"   % (target_year, )
        self.midd_date       = "30.6.%s"  % (target_year, )
        self.tail_date       = "31.12.%s" % (target_year, )
        self.head_time       = Date (self.head_date)
        self.midd_time       = Date (self.midd_date)
        self.tail_time       = Date (self.tail_date)
        self.target_year     = int  (target_year)
    # end def _setup_dates

# end class _Base

class Anlagen_Entry (_Base) :

    rate_pattern   = r"(?P<rate> [-+*/().0-9\s]+)"
    first_rate_pat = Regexp (rate_pattern, re.X)
    later_rate_pat = Regexp \
        ( r"(?P<year> \d\d (?: \d\d)?) \s* : \s* " + rate_pattern
        , re.X
        )

    def __init__ (self, line, anlagenverzeichnis) :
        try :
            ( self.desc, self.supplier, self.flags
            , self.birth_date, self.a_value, self.afa_spec, self.ifb
            , self.death_date
            )                = split_pat.split     (line, 8)
        except ValueError, exc :
            print line
            raise
        final                = "31.12.2037"
        self.birth_time      = Date (self.birth_date)
        self.death_time      = Date (self.death_date or final)
        self.alive           = self.death_time > anlagenverzeichnis.tail_time
        if int (self.death_time.year) < int (anlagenverzeichnis.year) :
            self._setup_dates (self.death_time.year)
        else :
            self._setup_dates (anlagenverzeichnis.year)
        self.half_date       = "1.7.%s" % (self.birth_time.year, )
        if "~" in self.flags :
            self.half_date   = "1.1.%s" % (self.birth_time.year + 1, )
        self.half_time       = Date (self.half_date)
        self.desc            = desc_strip_pat.sub  ("", self.desc)
        self.ifb             = int (self.ifb or 0) / 100.0
        currency_match       = currency_pat.search (self.a_value)
        a_value              = self.a_value
        source_currency      = anlagenverzeichnis.source_currency
        if currency_match :
            source_currency  = EU_Currency.Table   [currency_match.group (1)]
            a_value          = currency_pat.sub    ("", a_value)
        if EUC.target_currency is not ATS :
            self.zero        = source_currency     (0.0)
        else :
            self.zero        = source_currency     (1.0)
        self.source_currency = source_currency
        self.birth_value     = source_currency     (eval (a_value, {}, {}))
        self.new_value       = source_currency     (0.0)
        self.out_value       = source_currency     (0.0)
        self.ifb_value       = source_currency     (0.0)
        self.contemporary    = \
            (   self.birth_time <= anlagenverzeichnis.tail_time
            and self.death_time >= anlagenverzeichnis.head_time
            )
    # end def __init__

    def evaluate (self) :
        self._calc_rates ()
        self.current_depreciation = \
            self.birth_value * (self.current_rate / 100.0)
        if "=" not in self.flags :
            self.head_value = max \
                ( self.birth_value * ((100.0 - self.past_total_rate) / 100.)
                , self.zero
                )
            self.tail_value = self.head_value - self.current_depreciation
            if self.tail_value < self.zero :
                self.tail_value = self.zero
                self.current_depreciation -= self.zero
        else :
            self.head_value = self.tail_value = self.birth_value
        if self.birth_time >= self.head_time :
            self.head_value = self.source_currency (0.0)
            self.new_value  = self.birth_value
        if not self.alive :
            self.out_value  = self.tail_value
            self.tail_value = self.source_currency (0.0)
        elif self.ifb and self.birth_time.year + 4 > self.target_year :
            self.ifb_value  = self.birth_value * self.ifb
        self.new_ifb        = self.ifb and self.birth_time > self.head_time
        if self.tail_value.target_currency is not EU_Currency :
            self.birth_value          = self.birth_value.rounded_as_target ()
            self.head_value           = self.head_value.rounded_as_target  ()
            self.tail_value           = self.tail_value.rounded_as_target  ()
            self.new_value            = self.new_value.rounded_as_target   ()
            self.out_value            = self.out_value.rounded_as_target   ()
            self.ifb_value            = self.ifb_value.rounded_as_target   ()
            self.current_depreciation = \
                self.current_depreciation.rounded_as_target ()
    # end def evaluate

    def _calc_rates (self) :
        rates          = [x.strip () for x in self.afa_spec.split (",")]
        first_rate     = rates [0]
        first_rate_pat = self.first_rate_pat
        later_rate_pat = self.later_rate_pat
        if not first_rate_pat.match (first_rate) :
            raise ValueError, \
                  "%s doesn't match a depreciation rate" % (first_rate, )
        later_rates = []
        for r in rates [1:] :
            if not later_rate_pat.match (r) :
                raise ValueError, \
                      "%s doesn't match a depreciation rate" % (r, )
            y = Time_Tuple (later_rate_pat.year).year
            later_rates.append ((y, eval (later_rate_pat.rate, {}, {}) * 1.0))
        y_rate  = self.base_rate = eval (first_rate_pat.rate, {}, {}) * 1.0
        if later_rates :
            later_rates.append ((self.target_year, later_rates [-1] [1]))
        else :
            later_rates.append ((self.target_year, y_rate))
        y_rates = self.y_rates   = \
                  [y_rate * ((0.5, 1.0) [self.birth_time < self.half_time])]
        if self.birth_time < self.head_time :
            current_year = self.birth_time.year + 1
            for target_year, next_rate in later_rates :
                while current_year < target_year :
                    y_rates.append (y_rate)
                    current_year += 1
                y_rate = self.base_rate = next_rate
            y_rates.append \
                (y_rate * ((0.5, 1.0) [self.midd_time < self.death_time]))
        self.current_rate     = y_rates [-1]
        past_total_rate       = 0
        for y_rate in y_rates [:-1] :
            past_total_rate  += y_rate
        self.past_total_rate  = min (past_total_rate, 100.0)
        if self.past_total_rate + self.current_rate > 100.0 :
            self.current_rate = 100.0 - self.past_total_rate
    # end def _calc_rates

# end class Anlagen_Entry

class Anlagenverzeichnis (_Base) :

    assignment_pat = Regexp \
        ( r"^\$ "
          r"(?P<var> account_file | source_currency)"
          r"\s* = \s*"
          r"(?P<value> .*)"
          r"\s* ;"
        , re.X
        )

    header_format = "%-48s  %-8s  %10s  %10s  %8s  %10s  %10s"
    entry1_format = "%-45s%3s  %8s  %10.2f  %10.2f     %5.2f  %10.2f  %10.2f"
    newifb_format = "  %-46s  %8s  %10s  %10s  %8s  %10.2f  %10s"
    alive_format  = "  %-46s  %8s  %10s  %10s  %8s"
    dying_format  = "  %-36.31s%10s  %8s  %10s  %10s  %8s  %10.2f  %10s"
    footer_format = "\n%-48s  %8s  %10.2f  %10.2f  %8s  %10.2f  %10.2f"
    new_format    = "%-48s  %8s  %10s  %10.2f"
    out_format    = "%-48s  %8s  %10s  %10s  %8s  %10.2f"

    account_format = \
        " 31.12 & & & %10.2f & b & %-5s & 2100 & - & %-3s & & %-6s %s\n"

    def __init__ (self, year, start_year, file_name, source_currency) :
        self.year               = year
        self.start_time         = Date ("1.1.%s" % (start_year, ))
        self.file_name          = file_name
        self.source_currency    = source_currency
        self.account_file       = None
        self.entries            = []
        self.total_birth_value  = source_currency (0.0)
        self.total_head_value   = source_currency (0.0)
        self.total_tail_value   = source_currency (0.0)
        self.total_new_value    = source_currency (0.0)
        self.total_out_value    = source_currency (0.0)
        self.total_ifb_value    = source_currency (0.0)
        self.total_depreciation = source_currency (0.0)
        self._setup_dates (year)
        self.add_file     (file_name)
    # end def __init__

    def add_file (self, file_name) :
        assignment_pat = self.assignment_pat
        file           = open (file_name)
        for line in file.readlines () :
            if ignor_pat.match (line) : continue
            line                      = ws_head_pat.sub ("", line, count = 1)
            line                      = ws_tail_pat.sub ("", line, count = 1)
            if not line               : continue
            if assignment_pat.match (line) :
                self.eval_line (line, assignment_pat)
            else :
                self.add_line  (line)
        file.close ()
    # end def add_file

    def eval_line (self, line, match) :
        name       = match.var
        expression = match.value.replace \
                         ("$target_year", str (self.target_year))
        value      = eval (expression, {}, {})
        if name == "source_currency" :
            value  = EUC.Table [value]
        setattr (self, name, value)
    # end def eval_line

    def add_line (self, line) :
        self.entries.append (Anlagen_Entry (line, self))
    # end def add_line

    def evaluate (self) :
        for e in self.entries :
            if (not e.contemporary) or e.birth_time < self.start_time :
                e.contemporary = 0
                continue
            e.evaluate ()
            if e.contemporary and e.current_depreciation > 0 :
                self.total_birth_value   += e.birth_value
                self.total_head_value    += e.head_value
                self.total_tail_value    += e.tail_value
                self.total_new_value     += e.new_value
                self.total_out_value     += e.out_value
                self.total_depreciation  += e.current_depreciation
            elif e.new_ifb :
                self.total_ifb_value += e.ifb_value
    # end def evaluate

    def write (self) :
        print ( self.header_format
              % ( "", "", "Anschaff/", "Buchwert", " Afa ", "Afa", "Buchwert")
              )
        print ( self.header_format
              % ( "Text", "Datum", "Teil-Wert", "1.1.", "  %  "
                , "IFB/Abgang", "31.12."
                )
              )
        print "\n%s\n" % ("=" * 116, )
        for e in self.entries :
            if e.contemporary and e.current_depreciation > 0 :
                self._write_entry (e)
        print "\n%s\n" % ("=" * 116, )
        print ( self.footer_format
              % ( "Summe", ""
                , self.total_birth_value
                , self.total_head_value
                , "Afa"
                , self.total_depreciation
                , self.total_tail_value
                )
              )
        print self.new_format % ("Neuzug�nge", "", "", self.total_new_value)
        print ( self.out_format
              % ( "Abg�nge", "", "", "", "", self.total_out_value)
              )
        print ( self.out_format
              % ( "Investitionsfreibetrag", "", "", ""
                , "IFB"
                , self.total_ifb_value
                )
              )
    # end def write

    def _write_entry (self, e) :
        print ( self.entry1_format
              % ( e.desc
                , ("", "IFB") [e.ifb_value > 0]
                , e.birth_time.formatted ("%d.%m.%y")
                , e.birth_value
                , e.head_value
                , e.base_rate
                , e.current_depreciation
                , e.tail_value
                )
              )
        if e.new_ifb :
            print ( self.newifb_format
                  % ( e.supplier, "", "", "", "IFB", e.ifb_value, "")
                  )
        elif e.ifb_value :
            print "  %-36s%10.2f" % (e.supplier, e.ifb_value)
        elif e.alive :
            print ( self.alive_format
                  % (e.supplier, "", "", "", ("", "ewig") ["=" in e.flags])
                  )
        else :
            print ( self.dying_format
                  % ( e.supplier
                    , "Abgang"
                    , e.death_time.formatted ("%d.%m.%y")
                    , "", "", ("", "ewig") ["=" in e.flags]
                    , e.out_value
                    , ""
                    )
                  )
    # end def _write_entry

    def update_accounts (self) :
        if self.account_file :
            file = open (self.account_file, "w")
        else :
            file = sys.stdout
        for e in self.entries :
            if e.contemporary :
                self._update_account_entry (e, file)
        if self.account_file :
            file.close ()
    # end def update_accounts

    def _update_account_entry (self, e, file) :
        if e.current_depreciation :
            file.write \
                ( self.account_format
                % (e.current_depreciation, 7800, "fe",  "Afa",    e.desc)
                )
        if e.new_ifb :
            file.write \
                ( self.account_format
                % (e.ifb_value,            7802, "fue", "IFB",    e.desc)
                )
        if not e.alive :
            file.write \
                ( self.account_format
                % (e.out_value,            7801, "fue", "Abgang", e.desc)
                )
    # end def _update_account_entry

# end class Anlagenverzeichnis

def command_spec (arg_array = None) :
    from   Command_Line import Command_Line, Opt_L
    from   predicate    import sorted
    currencies = sorted (EU_Currency.Table.keys ())
    return Command_Line ( option_spec =
                            ( Opt_L ( selection   = currencies
                                    , name        = "source_currency"
                                    , type        = "S"
                                    , default     = "EUR"
                                    , description = "Source currency"
                                    )
                            , Opt_L ( selection   = currencies
                                    , name        = "target_currency"
                                    , type        = "S"
                                    , default     = "EUR"
                                    , description = "Target currency"
                                    )
                            , "-Start_year:S=1988"
                                "?Skip all entries before `Start_year`"
                            , "-update_accounts:B"
                                "?Add depreciation entries to account file"
                            )
                        , arg_spec    =
                            ( "year:S?Year of interest"
                            , "anlagenverzeichnis:S"
                                "?File defining depreciation data"
                            )
                        , min_args    = 2
                        , max_args    = 2
                        , description = "Calculate depreciations for `year`"
                        , arg_array   = arg_array
                        )
# end def command_spec

def main (cmd) :
    source_currency     = EUC.Table [cmd.source_currency]
    EUC.target_currency = EUC.Table [cmd.target_currency]
    year                = cmd.year
    start               = cmd.Start_year
    file_name           = cmd.anlagenverzeichnis
    anlagenverzeichnis  = Anlagenverzeichnis \
        (year, start, file_name, source_currency)
    anlagenverzeichnis.evaluate ()
    anlagenverzeichnis.write    ()
    if cmd.update_accounts :
        anlagenverzeichnis.update_accounts ()
    return anlagenverzeichnis
# end def main

if __name__ == "__main__":
    main (command_spec ())
### __END__ anlagenverzeichnis
