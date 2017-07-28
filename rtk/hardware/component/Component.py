#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.Component.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors 
#    may be used to endorse or promote products derived from this software 
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER 
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
#################################
Hardware Package Component Module
#################################
"""

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
    import Utilities
    from hardware.Hardware import Model as Hardware
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.Hardware import Model as Hardware

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(Hardware):                        # pylint: disable=R0902
    """
    The Component data model contains the attributes and methods of a hardware
    Component item.  The attributes of an Component are:

    :ivar int category_id: the ID of the component category.
    :ivar int subcategory_id: the ID of the component sub-category.
    :ivar float junction_temperature: the operating temperature of the
                                      component's junction.
    :ivar float knee_temperature: the temperature at which the component must
                                  begin being derated.
    :ivar float thermal_resistance: the junction-case or junction-ambient
                                    resistance to thermal transfer.
    :ivar float reference_temperature: the reference temperature for the
                                       component.
    """

    def __init__(self):
        """
        Method to initialize a Component data model instance.
        """

        super(Model, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.category_id = 0
        self.subcategory_id = 0
        self.junction_temperature = 0.0
        self.knee_temperature = 30.0
        self.thermal_resistance = 0.0
        self.reference_temperature = 30.0

    def set_attributes(self, values):
        """
        Method to set the Component data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Hardware.set_attributes(self, values[:121])

        if _code == 0:
            try:
                self.category_id = int(values[121])
                self.subcategory_id = int(values[122])
                self.junction_temperature = float(values[123])
                self.knee_temperature = float(values[124])
                self.thermal_resistance = float(values[125])
                self.reference_temperature = float(values[126])
            except IndexError as _err:
                _code = Utilities.error_handler(_err.args)
                _msg = _(u"ERROR: Insufficient input values.")
            except TypeError as _err:
                _code = Utilities.error_handler(_err.args)
                _msg = _(u"ERROR: Converting one or more inputs to correct "
                         u"data type.")

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Component data model
        attributes.

        :return: (category_id, subcategory_id, junction_temperature,
                  knee_temperature, thermal_resistance, reference_temperature)
        :rtype: tuple
        """

        _values = Hardware.get_attributes(self)

        _values = _values + (self.category_id, self.subcategory_id,
                             self.junction_temperature,
                             self.knee_temperature, self.thermal_resistance,
                             self.reference_temperature)

        return _values


class Component(object):
    """
    The Component data controller provides an interface between the Component
    data model and an RTK view model.  A single Component controller can manage
    one or more Component data models.  The Component data controller is
    currently unused.
    """

    def __init__(self):
        """
        Method to initialize a Component data controller instance.
        """

        pass
