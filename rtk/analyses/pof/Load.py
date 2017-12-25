#!/usr/bin/env python
"""
#########################
PoF Operating Load Module
#########################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.pof.Load.py is part of The RTK Project
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
except ImportError:  # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:  # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Load data model contains the attributes and methods of a Physics of
    Failure operating load.  A PoF will consist of one or more Loads per
    failure mechanism.  The attributes of a Load are:

    :ivar dict dicStresses: Dictionary of the operating stresses associated
                            with the operating load.  Key is the Stress ID;
                            value is a pointer to the instance of the operating
                            Stress data model.
    :ivar int mechanism_id: the PoF Mechanism ID the Load is associated with.
    :ivar int load_id: the PoF Load ID.
    :ivar str description: the description of the PoF Load.
    :ivar int damage_model: the index of the damage (methematical) model.
    :ivar int priority: the priority of the PoF Load.
    """

    def __init__(self, mechanism_id=None):
        """
        Method to initialize a Load data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicStresses = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.mechanism_id = mechanism_id
        self.load_id = None
        self.description = ''
        self.damage_model = 0
        self.priority = 0


class Load(object):
    """
    The Load data controller provides an interface between the Load data model
    and an RTK view model.  A single Load data controller can control one or
    more Load data models.  Currently the Load data controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Load data controller instance.
        """

        pass
