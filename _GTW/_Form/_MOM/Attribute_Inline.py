# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.MOM.Attribute_Inline
#
# Purpose
#    Handle the creation/modification of an object inside of a other form.
#    The attribute inline will be treated like a `Field` of a form and not
#    like a inline group
#
# Revision Dates
#    15-Apr-2010 (MG) Creation
#    ��revision-date�����
#--

from   _TFL                                 import TFL
import _TFL._Meta.Once_Property
from   _TFL.predicate                       import all_true
from   _GTW                                 import GTW
import _GTW._Form.Field
import _GTW._Form.Widget_Spec
import _GTW._Form._MOM
import _GTW._Form._MOM.Inline_Instance

class _Attribute_Inline_ (TFL.Meta.Object) :
    """The `field` instance for attribute inline editing."""

    electric = False

    def __init__ (self, name, form_cls, inline_description, form = None) :
        self.name               = self.html_name = name
        self.form_cls           = form_cls
        self.inline_description = inline_description
        self.form               = form
    # end def __init__

    def create_object (self, form) :
        if self.needs_processing :
            self.form.recursively_run \
                ("create_object", self.form, reverse = True)
        if (    not self.form.error_count
           and (   self.form.instance
               or (self.form.is_link_role and self.form.raw_attr_dict)
               )
           ) :
            ### the instance has been created/updated successfully -> update
            ### the raw_attr_dict of the parent
            form.raw_attr_dict [self.name] = self.form.get_object_raw (form)
        ### not not move the caching up because the `get_object_raw` could
        ### create additional errors
        ec = self.form.error_count
        if ec or not self.form.instance :
            ### an error was detected or the instance has not been
            ### created -> delete the values for this attribute from
            ### parent's raw_attr_dict
            form.raw_attr_dict.pop (self.name, None)
        form.inline_errors += ec
    # end def create_object

    def clone (self, form) :
        instance = getattr (form.instance, self.name, None)
        return self.__class__ \
            ( self.name, self.form_cls, self.inline_description
            , self.form_cls
                ( instance
                , parent = form
                , prefix = "__".join ((form.prefix, self.name))
                )
            )
    # end def clone

    def get_raw (self, form, defaults) :
        return self.form.get_object_raw (defaults)
    # end def get_raw

    @TFL.Meta.Once_Property
    def Media (self) :
        self._setup_javascript ()
        return self.widget.Media
    # end def Media

    def prepare_request_data (self, form, request_data) :
        self.form.recursively_run \
            ("prepare_request_data", self.form, request_data)
    # end def prepare_request_data

    def _setup_javascript (self) :
        pass
    # end def _setup_javascript

    def setup_raw_attr_dict (self, form) :
        self.form.recursively_run ("setup_raw_attr_dict", self.form)
    # end def setup_raw_attr_dict

    def update_object (self, form) :
        self.form.recursively_run ("update_object", self.form)
    # end def setup_raw_attr_dict

    def update_raw_attr_dict (self, form) :
        self.form.recursively_run ("update_raw_attr_dict", self.form)
    # end def setup_raw_attr_dict

    def __getattr__ (self, name) :
        try :
            return getattr (self.inline_description, name)
        except AttributeError :
            raise AttributeError (name)
    # end def __getattr__

# end class _Attribute_Inline_

class An_Attribute_Inline (_Attribute_Inline_) :
    """Inline of an An_Entity."""


    Form_Class       = GTW.Form.MOM.An_Attribute_Inline_Instance
    needs_processing = True

# end class An_Attribute_Inline

class Id_Attribute_Inline (_Attribute_Inline_) :
    """Inline for a ID_Entity."""

    Form_Class = GTW.Form.MOM.Id_Attribute_Inline_Instance

    @TFL.Meta.Once_Property
    def needs_processing (self) :
        state = self.form.state
        if state == "U" :
            ### this from handles an instance which should be unlinked
            ### because we handle an attribute inline we cannot destroy the
            ### object but just unlink it from the many object
            self.form.instance = None
            return False
        if state == "L" :
            ### the client side provided information which object should be
            ### linked -> let's get this object by it's lid and set it in the
            ### form
            et_man             = self.form.et_man
            pid                = et_man.pid_from_lid  (self.form.lid)
            self.form.instance = et_man.pid_query     (pid)
            self.form._create_update_executed = True
            return False
        return True
    # end def needs_processing

    def _setup_javascript (self) :
        if self.form_cls.completer :
            self.form_cls.completer.attach (self.form_cls, self.link_name)
    # end def _setup_javascript

# end class Id_Attribute_Inline

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*", "_Attribute_Inline_")
### __END__ GTW.Form.MOM.Attribute_Inline
