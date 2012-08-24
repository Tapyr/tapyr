# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.SRM_Graph
#
# Purpose
#    Test SRM.Graph
#
# Revision Dates
#    17-Aug-2012 (CT) Creation
#    ��revision-date�����
#--

from   __future__  import unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> g = graph (scope.app_type)

    >>> for v in g.nodes () :
    ...   print "%%-45s %%s" %% (v, v.label)
    <Graph.Link2  SRM.Boat_in_Regatta>            _in_
    <Graph.Link1  SRM.Regatta>                    SRM.Regatta
    <Graph.Object SRM.Regatta_Event>              SRM.Regatta_Event
    <Graph.Object SRM.Club>                       SRM.Club
    <Graph.Link2  SRM.Crew_Member>                SRM.Crew_Member
    <Graph.Link2  SRM.Team_has_Boat_in_Regatta>   _has_
    <Graph.Link1  SRM.Team>                       SRM.Team
    <Graph.Link1  SRM.Regatta_C>                  SRM.Regatta_C
    <Graph.Link1  SRM.Race_Result>                SRM.Race_Result
    <Graph.Link1  SRM.Boat>                       SRM.Boat
    <Graph.Object SRM.Boat_Class>                 SRM.Boat_Class
    <Graph.Link1  SRM.Sailor>                     SRM.Sailor
    <Graph.Object PAP.Person>                     PAP.Person
    <Graph.Object PAP.Subject>                    PAP.Subject

    >>> for v in g.nodes () :
    ...   print "%%-45s %%s" %% (v, v.label_parts)
    <Graph.Link2  SRM.Boat_in_Regatta>            (u'_in_',)
    <Graph.Link1  SRM.Regatta>                    (u'SRM', u'.Regatta')
    <Graph.Object SRM.Regatta_Event>              (u'SRM', u'.Regatta', u'_Event')
    <Graph.Object SRM.Club>                       (u'SRM', u'.Club')
    <Graph.Link2  SRM.Crew_Member>                (u'SRM', u'.Crew', u'_Member')
    <Graph.Link2  SRM.Team_has_Boat_in_Regatta>   (u'_has_',)
    <Graph.Link1  SRM.Team>                       (u'SRM', u'.Team')
    <Graph.Link1  SRM.Regatta_C>                  (u'SRM', u'.Regatta', u'_C')
    <Graph.Link1  SRM.Race_Result>                (u'SRM', u'.Race', u'_Result')
    <Graph.Link1  SRM.Boat>                       (u'SRM', u'.Boat')
    <Graph.Object SRM.Boat_Class>                 (u'SRM', u'.Boat', u'_Class')
    <Graph.Link1  SRM.Sailor>                     (u'SRM', u'.Sailor')
    <Graph.Object PAP.Person>                     (u'PAP', u'.Person')
    <Graph.Object PAP.Subject>                    (u'PAP', u'.Subject')

    >>> for v in g.nodes (sort_key = TFL.Getter.type_name) :
    ...   print "%%-45s %%-45s %%s" %% (v, v.anchor, v.pos)
    <Graph.Object PAP.Person>                     <Graph.Link1  SRM.Sailor>                     N*3
    <Graph.Object PAP.Subject>                    <Graph.Object PAP.Person>                     E*2 + N*3
    <Graph.Link1  SRM.Boat>                       <Graph.Link2  SRM.Boat_in_Regatta>            W
    <Graph.Object SRM.Boat_Class>                 <Graph.Link1  SRM.Boat>                       W*2
    <Graph.Link2  SRM.Boat_in_Regatta>            None                                          (0,0)
    <Graph.Object SRM.Club>                       <Graph.Object SRM.Regatta_Event>              NE*2
    <Graph.Link2  SRM.Crew_Member>                <Graph.Link2  SRM.Boat_in_Regatta>            NE
    <Graph.Link1  SRM.Race_Result>                <Graph.Link2  SRM.Boat_in_Regatta>            SW
    <Graph.Link1  SRM.Regatta>                    <Graph.Link2  SRM.Boat_in_Regatta>            E
    <Graph.Link1  SRM.Regatta_C>                  <Graph.Link1  SRM.Team>                       E + S*2
    <Graph.Object SRM.Regatta_Event>              <Graph.Link1  SRM.Regatta>                    E*2
    <Graph.Link1  SRM.Sailor>                     <Graph.Link2  SRM.Boat_in_Regatta>            N*2
    <Graph.Link1  SRM.Team>                       <Graph.Link2  SRM.Team_has_Boat_in_Regatta>   S*2
    <Graph.Link2  SRM.Team_has_Boat_in_Regatta>   <Graph.Link2  SRM.Boat_in_Regatta>            S

    >>> for v in g.nodes (sort_key = TFL.Getter.type_name) :
    ...     print v.type_name, v.e_type.Roles
    PAP.Person ()
    PAP.Subject ()
    SRM.Boat (Boat_Class `left`,)
    SRM.Boat_Class ()
    SRM.Boat_in_Regatta (Boat `left`, Regatta `right`)
    SRM.Club ()
    SRM.Crew_Member (Boat_in_Regatta `left`, Sailor `right`)
    SRM.Race_Result (Boat_in_Regatta `left`,)
    SRM.Regatta (Regatta_Event `left`,)
    SRM.Regatta_C (Regatta_Event `left`,)
    SRM.Regatta_Event ()
    SRM.Sailor (Person `left`,)
    SRM.Team (Regatta_C `left`,)
    SRM.Team_has_Boat_in_Regatta (Team `left`, Boat_in_Regatta `right`)

    >>> for v in g.nodes () :
    ...     if v.rel_map :
    ...         for a, l in sorted (v.rel_map.iteritems ()) :
    ...             print l
    <Graph.Relation.Role SRM.Boat_in_Regatta.left -> SRM.Boat>
    <Graph.Relation.Role SRM.Boat_in_Regatta.right -> SRM.Regatta>
    <Graph.Relation.Attr SRM.Boat_in_Regatta.skipper -> SRM.Sailor>
    <Graph.Relation.Role SRM.Regatta.left -> SRM.Regatta_Event>
    <Graph.Relation.Attr SRM.Regatta_Event.club -> SRM.Club>
    <Graph.Relation.Role SRM.Crew_Member.left -> SRM.Boat_in_Regatta>
    <Graph.Relation.Role SRM.Crew_Member.right -> SRM.Sailor>
    <Graph.Relation.Role SRM.Team_has_Boat_in_Regatta.left -> SRM.Team>
    <Graph.Relation.Role SRM.Team_has_Boat_in_Regatta.right -> SRM.Boat_in_Regatta>
    <Graph.Relation.Role SRM.Team.left -> SRM.Regatta_C>
    <Graph.Relation SRM.Regatta_C IS A SRM.Regatta>
    <Graph.Relation.Role SRM.Regatta_C.left -> SRM.Regatta_Event>
    <Graph.Relation.Role SRM.Race_Result.left -> SRM.Boat_in_Regatta>
    <Graph.Relation.Role SRM.Boat.left -> SRM.Boat_Class>
    <Graph.Relation.Attr SRM.Sailor.club -> SRM.Club>
    <Graph.Relation.Role SRM.Sailor.left -> PAP.Person>
    <Graph.Relation PAP.Person IS A PAP.Subject>

    >>> for v in g.nodes () :
    ...     if v.rel_map :
    ...         for a, l in sorted (v.rel_map.iteritems ()) :
    ...             print l.kind, l.source, l.target
    Role <Graph.Link2  SRM.Boat_in_Regatta> <Graph.Link1  SRM.Boat>
    Role <Graph.Link2  SRM.Boat_in_Regatta> <Graph.Link1  SRM.Regatta>
    Attr <Graph.Link2  SRM.Boat_in_Regatta> <Graph.Link1  SRM.Sailor>
    Role <Graph.Link1  SRM.Regatta> <Graph.Object SRM.Regatta_Event>
    Attr <Graph.Object SRM.Regatta_Event> <Graph.Object SRM.Club>
    Role <Graph.Link2  SRM.Crew_Member> <Graph.Link2  SRM.Boat_in_Regatta>
    Role <Graph.Link2  SRM.Crew_Member> <Graph.Link1  SRM.Sailor>
    Role <Graph.Link2  SRM.Team_has_Boat_in_Regatta> <Graph.Link1  SRM.Team>
    Role <Graph.Link2  SRM.Team_has_Boat_in_Regatta> <Graph.Link2  SRM.Boat_in_Regatta>
    Role <Graph.Link1  SRM.Team> <Graph.Link1  SRM.Regatta_C>
    Is_A <Graph.Link1  SRM.Regatta_C> <Graph.Link1  SRM.Regatta>
    Role <Graph.Link1  SRM.Regatta_C> <Graph.Object SRM.Regatta_Event>
    Role <Graph.Link1  SRM.Race_Result> <Graph.Link2  SRM.Boat_in_Regatta>
    Role <Graph.Link1  SRM.Boat> <Graph.Object SRM.Boat_Class>
    Attr <Graph.Link1  SRM.Sailor> <Graph.Object SRM.Club>
    Role <Graph.Link1  SRM.Sailor> <Graph.Object PAP.Person>
    Is_A <Graph.Object PAP.Person> <Graph.Object PAP.Subject>

    >>> for v in g.nodes () :
    ...     print "%%-45s %%-12s %%s" %% (v, v.pos, tuple (v.pos))
    <Graph.Link2  SRM.Boat_in_Regatta>            (0,0)        (0, 0)
    <Graph.Link1  SRM.Regatta>                    E            (1, 0)
    <Graph.Object SRM.Regatta_Event>              E*2          (2, 0)
    <Graph.Object SRM.Club>                       NE*2         (2, 2)
    <Graph.Link2  SRM.Crew_Member>                NE           (1, 1)
    <Graph.Link2  SRM.Team_has_Boat_in_Regatta>   S            (0, -1)
    <Graph.Link1  SRM.Team>                       S*2          (0, -2)
    <Graph.Link1  SRM.Regatta_C>                  E + S*2      (1, -2)
    <Graph.Link1  SRM.Race_Result>                SW           (-1, -1)
    <Graph.Link1  SRM.Boat>                       W            (-1, 0)
    <Graph.Object SRM.Boat_Class>                 W*2          (-2, 0)
    <Graph.Link1  SRM.Sailor>                     N*2          (0, 2)
    <Graph.Object PAP.Person>                     N*3          (0, 3)
    <Graph.Object PAP.Subject>                    E*2 + N*3    (2, 3)

    >>> ar = Ascii_Renderer (g)

    >>> for v in g.nodes () :
    ...     for a, l in sorted (v.rel_map.iteritems ()) :
    ...       if l.source_connector and l.target_connector :
    ...         print "%%-30s %%-30s %%-10s %%-10s %%-10s %%1.1s %%5.3f %%1.1s %%5.3f" %% ((
    ...            l.source.type_name, l.target.type_name, l.source.pos, l.target.pos, l.delta) + l.source_connector + l.target_connector)
    SRM.Boat_in_Regatta            SRM.Boat                       (0,0)      W          E          l 0.500 r 0.500
    SRM.Boat_in_Regatta            SRM.Regatta                    (0,0)      E          W          r 0.500 l 0.500
    SRM.Boat_in_Regatta            SRM.Sailor                     (0,0)      N*2        S*2        t 0.250 b 0.250
    SRM.Regatta                    SRM.Regatta_Event              E          E*2        W          r 0.500 l 0.500
    SRM.Regatta_Event              SRM.Club                       E*2        NE*2       S*2        t 0.500 b 0.500
    SRM.Crew_Member                SRM.Boat_in_Regatta            NE         (0,0)      NE         b 0.500 t 0.750
    SRM.Crew_Member                SRM.Sailor                     NE         N*2        SE         t 0.500 b 0.750
    SRM.Team_has_Boat_in_Regatta   SRM.Team                       S          S*2        N          b 0.500 t 0.500
    SRM.Team_has_Boat_in_Regatta   SRM.Boat_in_Regatta            S          (0,0)      S          t 0.500 b 0.750
    SRM.Team                       SRM.Regatta_C                  S*2        E + S*2    W          r 0.500 l 0.500
    SRM.Regatta_C                  SRM.Regatta                    E + S*2    E          S*2        t 0.250 b 0.500
    SRM.Regatta_C                  SRM.Regatta_Event              E + S*2    E*2        W + S*2    t 0.750 b 0.500
    SRM.Race_Result                SRM.Boat_in_Regatta            SW         (0,0)      SW         t 0.500 b 0.250
    SRM.Boat                       SRM.Boat_Class                 W          W*2        E          l 0.500 r 0.500
    SRM.Sailor                     SRM.Club                       N*2        NE*2       W*2        r 0.500 l 0.500
    SRM.Sailor                     PAP.Person                     N*2        N*3        S          t 0.500 b 0.500
    PAP.Person                     PAP.Subject                    N*3        E*2 + N*3  W*2        r 0.500 l 0.500


    >>> ar.max_x_spec, ar.max_y_spec
    (2, 3)

    >>> ar.grid_size, ar.node_size
    (Point (32, 12), Point (16, 4))

    >>> ar.transform
    Affine (32, 0, 96, 0, -12, 48)

    >>> ar.max_x, ar.max_y
    (208, 88)

    >>> for n in ar.nodes :
    ...     print "%%-45s %%-12s %%s" %% (n.entity, tuple (n.pos), tuple (n.entity.pos))
    <Graph.Link2  SRM.Boat_in_Regatta>            (96, 48)     (0, 0)
    <Graph.Link1  SRM.Regatta>                    (128, 48)    (1, 0)
    <Graph.Object SRM.Regatta_Event>              (160, 48)    (2, 0)
    <Graph.Object SRM.Club>                       (160, 24)    (2, 2)
    <Graph.Link2  SRM.Crew_Member>                (128, 36)    (1, 1)
    <Graph.Link2  SRM.Team_has_Boat_in_Regatta>   (96, 60)     (0, -1)
    <Graph.Link1  SRM.Team>                       (96, 72)     (0, -2)
    <Graph.Link1  SRM.Regatta_C>                  (128, 72)    (1, -2)
    <Graph.Link1  SRM.Race_Result>                (64, 60)     (-1, -1)
    <Graph.Link1  SRM.Boat>                       (64, 48)     (-1, 0)
    <Graph.Object SRM.Boat_Class>                 (32, 48)     (-2, 0)
    <Graph.Link1  SRM.Sailor>                     (96, 24)     (0, 2)
    <Graph.Object PAP.Person>                     (96, 12)     (0, 3)
    <Graph.Object PAP.Subject>                    (160, 12)    (2, 3)

    >>> for n in ar.nodes :
    ...     print "%%-45s %%-12s %%s" %% (n.entity, n.box.top_left, (n.max_x, n.max_y))
    <Graph.Link2  SRM.Boat_in_Regatta>            (96, 48)     (112.0, 52.0)
    <Graph.Link1  SRM.Regatta>                    (128, 48)    (144.0, 52.0)
    <Graph.Object SRM.Regatta_Event>              (160, 48)    (176.0, 52.0)
    <Graph.Object SRM.Club>                       (160, 24)    (176.0, 28.0)
    <Graph.Link2  SRM.Crew_Member>                (128, 36)    (144.0, 40.0)
    <Graph.Link2  SRM.Team_has_Boat_in_Regatta>   (96, 60)     (112.0, 64.0)
    <Graph.Link1  SRM.Team>                       (96, 72)     (112.0, 76.0)
    <Graph.Link1  SRM.Regatta_C>                  (128, 72)    (144.0, 76.0)
    <Graph.Link1  SRM.Race_Result>                (64, 60)     (80.0, 64.0)
    <Graph.Link1  SRM.Boat>                       (64, 48)     (80.0, 52.0)
    <Graph.Object SRM.Boat_Class>                 (32, 48)     (48.0, 52.0)
    <Graph.Link1  SRM.Sailor>                     (96, 24)     (112.0, 28.0)
    <Graph.Object PAP.Person>                     (96, 12)     (112.0, 16.0)
    <Graph.Object PAP.Subject>                    (160, 12)    (176.0, 16.0)

    >>> for n in ar.nodes :
    ...     for k, l in sorted (n.link_map.iteritems ()) :
    ...         print l.relation.kind, k, l.source.entity, l.target.entity
    Role left <Graph.Link2  SRM.Boat_in_Regatta> <Graph.Link1  SRM.Boat>
    Role right <Graph.Link2  SRM.Boat_in_Regatta> <Graph.Link1  SRM.Regatta>
    Attr skipper <Graph.Link2  SRM.Boat_in_Regatta> <Graph.Link1  SRM.Sailor>
    Role left <Graph.Link1  SRM.Regatta> <Graph.Object SRM.Regatta_Event>
    Attr club <Graph.Object SRM.Regatta_Event> <Graph.Object SRM.Club>
    Role left <Graph.Link2  SRM.Crew_Member> <Graph.Link2  SRM.Boat_in_Regatta>
    Role right <Graph.Link2  SRM.Crew_Member> <Graph.Link1  SRM.Sailor>
    Role left <Graph.Link2  SRM.Team_has_Boat_in_Regatta> <Graph.Link1  SRM.Team>
    Role right <Graph.Link2  SRM.Team_has_Boat_in_Regatta> <Graph.Link2  SRM.Boat_in_Regatta>
    Role left <Graph.Link1  SRM.Team> <Graph.Link1  SRM.Regatta_C>
    Is_A IS_A_0 <Graph.Link1  SRM.Regatta_C> <Graph.Link1  SRM.Regatta>
    Role left <Graph.Link1  SRM.Regatta_C> <Graph.Object SRM.Regatta_Event>
    Role left <Graph.Link1  SRM.Race_Result> <Graph.Link2  SRM.Boat_in_Regatta>
    Role left <Graph.Link1  SRM.Boat> <Graph.Object SRM.Boat_Class>
    Attr club <Graph.Link1  SRM.Sailor> <Graph.Object SRM.Club>
    Role left <Graph.Link1  SRM.Sailor> <Graph.Object PAP.Person>
    Is_A IS_A_0 <Graph.Object PAP.Person> <Graph.Object PAP.Subject>

    >>> print clean_rendered (ar.render ())
                                                                                                    +---------------+                                               +---------------+
                                                                                                    | PAP.Person    |                                               | PAP.Subject   |
                                                                                                    |               |                                               |               |
                                                                                                    |               |                                               |               |
                                                                                                    +---------------+                                               +---------------+
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
                                                                                                    +---------------+                                               +---------------+
                                                                                                    | SRM.Sailor    |                                               | SRM.Club      |
                                                                                                    |               |                                               |               |
                                                                                                    |               |                                               |               |
                                                                                                    +---------------+                                               +---------------+
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
                                                                                                                                    +---------------+
                                                                                                                                    | SRM.Crew      |
                                                                                                                                    |  _Member      |
                                                                                                                                    |               |
                                                                                                                                    +---------------+
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
                                    +---------------+               +---------------+               +---------------+               +---------------+               +---------------+
                                    | SRM.Boat      |               | SRM.Boat      |               | _in_          |               | SRM.Regatta   |               | SRM.Regatta   |
                                    |  _Class       |               |               |               |               |               |               |               |  _Event       |
                                    |               |               |               |               |               |               |               |               |               |
                                    +---------------+               +---------------+               +---------------+               +---------------+               +---------------+
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
                                                                    +---------------+               +---------------+
                                                                    | SRM.Race      |               | _has_         |
                                                                    |  _Result      |               |               |
                                                                    |               |               |               |
                                                                    +---------------+               +---------------+
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
                                                                                                    +---------------+               +---------------+
                                                                                                    | SRM.Team      |               | SRM.Regatta_C |
                                                                                                    |               |               |               |
                                                                                                    |               |               |               |
                                                                                                    +---------------+               +---------------+


"""

from _GTW.__test__.model        import *
from _GTW._OMP._SRM.Graph       import graph

from _MOM._Graph.Ascii          import Renderer as Ascii_Renderer

from _TFL.Regexp                import Regexp, Multi_Re_Replacer, Re_Replacer, re

clean_rendered = Multi_Re_Replacer \
    ( Re_Replacer ("^( *\n)+", "")
    , Re_Replacer ("(\n *)+$", "")
    )

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.SRM_Graph