//-*- coding: iso-8859-1 -*-
// Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW
//
// Purpose
//    Provide a javascript class based on ideas of
//        http://dean.edwards.name/weblog/2006/03/base/
//    and
//        http://ejohn.org/blog/simple-javascript-inheritance/
//
// Revision Dates
//    25-Jan-2011 (CT) Creation
//    26-Jan-2011 (CT) `update_proto` factored, `update` added
//    27-Jan-2011 (CT) `Module` added and used for `$GTW`
//    27-Jan-2011 (CT) Argument `meta` added to `extend`
//    ��revision-date�����
//--

var $GTW;

( function () {
    var making_proto = false;
    var super_re     = /\bthis\._super\b/;
    var super_test   =
        ( super_re.test ((function () { this._super (); }))
        ? function (v) { return super_re.test (v); }
        : function (v) { return true; }
        );
    var update_proto = function (dict, proto, base) {
        var name;
        if (dict !== undefined) {
            for (name in dict) {
                if (dict.hasOwnProperty (name)) {
                    var d_val = dict [name];
                    var b_val = base [name];
                    var super_caller =
                        (  (typeof d_val === "function")
                        && (typeof b_val === "function")
                        && super_test (d_val)
                        );
                    proto [name] =
                        ( super_caller
                        ? ( function (d_val, b_val) { // freeze closure values
                                return function () {
                                    var result, saved_super = this._super;
                                    try {
                                        this._super = b_val;
                                        result = d_val.apply (this, arguments);
                                    } finally {
                                        this._super = saved_super;
                                    }
                                    return result;
                                };
                            }
                          ) (d_val, b_val)
                        : d_val
                        );
                }
            }
        }
    };
    var Class    = function Class () {};
    var Module   = function (dict) {
        return new Class ().update (dict);
    };
    Class.extend = function (dict, meta) {
        var base = this.prototype;
        var proto, result;
        // don't run `init` in constructor called by `new this ()`
        making_proto = true;
        try {
            proto = new this ();
        }  finally {
            making_proto = false;
        }
        result = proto.constructor = function () {
            if (! making_proto && this ["init"]) {
                this.init.apply (this, arguments);
            }
            this.update = proto.update;
        };
        proto.update = function (dict) {
            update_proto.call (this, dict, this, proto);
            return this;
        };
        result.prototype = proto;
        result.extend    = this.extend;
        result.update    = this.update;
        update_proto.call (this, dict, proto, base);
        result.update     (meta);
        return result;
    };
    Class.update = function (dict) {
        update_proto.call (this, dict, this, this.prototype);
        return this;
    };
    Class  = Class.extend ({}); // add `proto.constructor` to `Class`
    $GTW = Module (
        { Class       : Class
        , Module      : Module
        , author      : "christian.tanzer@swing.co.at"
        , copyright   : "Copyright (C) 2011 Christian Tanzer"
        , license     : "Dual licensed under the MIT or AGPLv3 licenses."
        , license_url : "http://www.c-tanzer.at/license/mit_or_agpl.html"
        , version     : "1.0"
        }
    );
  }
) ();

/*

Field = $GTW.Class.extend
  ( { init : function (name, title) { this.name = name; this.title = title; }, show : function () { return (this.name + ": " + this.title); } }
  , { name : "Field"}
  );
P_Field = Field.extend ({ show : function () { return this._super () + " but more powerful!"; } });
P_Field.prototype instanceof Field
f = new Field ("a", "b")
pf = new P_Field ("gqu", "foo")
!(f instanceof P_Field) && ( f instanceof Field) && ( f instanceof Object)
(pf instanceof P_Field) && (pf instanceof Field) && (pf instanceof Object)

*/

// __END__ GTW.js
