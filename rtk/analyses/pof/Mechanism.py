#!/usr/bin/env python
"""
####################
PoF Mechanism Module
####################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.pof.Mechanism.py is part of The RTK Project
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

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
    import Utilities
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Mechanism data model contains the attributes and methods of a Physics
    of Failure failure mechanism.  A PoF will consist of one or more failure
    mechanism.  The attributes of a Mechanism are:

    :ivar dict dicLoads: Dictionary of the operating loads associated with the
                         failure mechanism.  Key is the Load ID; value is a
                         pointer to the instance of the operating Load data
                         model.
    :ivar int assembly_id: the Hardware ID the PoF Mechanism is associated
                           with.
    :ivar int mechanism_id: the PoF Mechanism ID.
    :ivar str description: the description of the PoF Mechanism.
    """

    def __init__(self):
        """
        Method to initialize a Mechanism data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicLoads = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.assembly_id = None
        self.mechanism_id = None
        self.description = ''

    def set_attributes(self, values):
        """
        Method to set the Mechanism data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.assembly_id = int(values[0])
            self.mechanism_id = int(values[1])
            self.description = str(values[2])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."
        except ValueError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Wrong input data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Mechanism data model
        attributes.

        :return: (assembly_id, mechanism_id, description)
        :rtype: tuple
        """

        return(self.assembly_id, self.mechanism_id, self.description)


class Mechanism(object):
    """
    The Mechanism data controller provides an interface between the Mechanism
    data model and an RTK view model.  A single Mechanism data controller can
    control one or more Mechanism data models.  Currently the Mechanism data
    controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Mechanism data controller instance.
        """

        pass
