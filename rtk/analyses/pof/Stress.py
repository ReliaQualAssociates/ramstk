#!/usr/bin/env python
"""
###########################
PoF Operating Stress Module
###########################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.pof.Stress.py is part of The RTK Project
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
    The Stress data model contains the attributes and methods of a Physics of
    Failure operating stress.  A PoF will consist of one or more Stress per
    operating load.  The attributes of a Stress are:

    :ivar dict dicMethods: Dictionary of the test methods associated with the
                           operating stress.  Key is the Method ID; value is a
                           pointer to the instance of the test method data
                           model.
    :ivar int load_id: the PoF Load ID the Stress is associated with.
    :ivar int stress_id: the ID of the PoF Stress.
    :ivar str description: the description of the PoF Stress.
    :ivar int measurable_parameter: the index of the parameter that can be
                                    measured and correlated with the PoF
                                    Stress.
    :ivar int load_history: the index of the load history method for the
                            PoF Stress.
    :ivar str remarks: any remarks associated with the PoF Stress.
    """

    def __init__(self, load_id=None):
        """
        Method to initialize a Stress data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicMethods = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.load_id = load_id
        self.stress_id = None
        self.description = ''
        self.measurable_parameter = 0
        self.load_history = 0
        self.remarks = ''


class Stress(object):
    """
    The Stress data controller provides an interface between the Stress data
    model and an RTK view model.  A single Stress data controller can control
    one or more Stress data models.  Currently the Stress data controller is
    unused.

    """

    def __init__(self):
        """
        Method to initialize a Stress data controller instance.
        """

        pass
