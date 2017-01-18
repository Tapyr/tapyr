// Copyright (C) 2016-2017 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/nav_off_canvas.js
//
// Purpose
//    Vanilla javascript function supporting off-canvas navigation
//
// Revision Dates
//    15-Jan-2016 (CT) Creation
//    24-Jan-2016 (CT) Use `$.$$`
//    13-Jan-2017 (CT) Remove calls of `$.prevent_default`
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.nav_off_canvas = $.merge
        ( function nav_off_canvas (opts) {
            var O = $.merge ({}, nav_off_canvas.defaults, opts);
            var S = $.merge ({}, nav_off_canvas.selectors, O ["selectors"]);
            var hide_els$   = $.$$     (S.hide);
            var main_el     = $.query1 (S.main);
            var nav_el      = $.query1 (S.nav);
            var toggle_els$ = $.$$     (S.toggle);
            var main_id     = "#" + main_el.id;
            var mcl         = main_el.classList;
            var off_cls     = O.off_class;
            var on_cls      = O.on_class;
            var hide_cb     = function hide_cb (ev) {
                mcl.add    (off_cls);
                mcl.remove (on_cls);
                if ($.is_in_viewport (main_el, 0.6, 0.4)) {
                    // avoid automatic scrolling to the anchor
                    // if it is already visible
                    $V5a.history_push (main_id);
                } else {
                    // the `toggle` alwyas points to `nav_el`
                    // --> don't follow the link
                    // --> set window.location manually to `main_el`
                    window.location  = main_id;
                };
                $.prevent_default (ev);
            };
            var toggle_cb   = function toggle_cb (ev) {
                // for narrow screens, nav_el might be hidden although
                // `off_cls` isn't set
                // --> don't test for `off_cls` directly
                var nav_off = nav_el.clientHeight === 0
                           || nav_el.clientWidth  === 0;
                if (nav_off) {
                    mcl.remove (off_cls);
                    mcl.add    (on_cls);
                    if ($.is_in_viewport (nav_el, 0.75, 0.9)) {
                        // avoid automatic scrolling to the anchor
                        // if it is already visible
                        $.prevent_default (ev);
                        $V5a.history_push ("#" + nav_el.id);
                    };
                } else {
                    hide_cb (ev);
                };
             };
            hide_els$.bind   ("click", hide_cb);
            toggle_els$.bind ("click", toggle_cb);
          }
        , { defaults :
              { off_class      : "nav-off-canvas"
              , on_class       : "nav-on-canvas"
              , toggle_display : "inline-block"
              }
          , selectors :
              { hide           : "a.main-nav-hide"
              , main           : "[id=main]"
              , nav            : "[id=navigate]"
              , toggle         : "a.main-nav-link"
              }
          }
        );
  } ($V5a)
);

// __END__ V5a/nav_off_canvas.js
