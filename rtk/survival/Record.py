#!/usr/bin/env python
"""
###############################################
Survival Package Dataset Record Data Sub-Module
###############################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.survival.Record.py is part of The RTK Project
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

try:
    import Utilities
except ImportError:
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'


class Model(object):
    """
    The Record data model contains the attributes and methods for a dataset
    Record. The attributes of a Record model are:

    :ivar int survival_id: default value: 0
    :ivar int assembly_id: default value: 0
    :ivar str assembly_name: the noun name of the affected Hardware assembly.
    :ivar int failure_date: default value: 719163
    :ivar float left_interval: default value: 0.0
    :ivar float right_interval: default value: 0.0
    :ivar int status: default value: 0
    :ivar int n_failures: default value: 0
    :ivar float interarrival_time: default value: 0.0
    :ivar int mode_type: default value: 0
    :ivar int nevada_chart: default value: 0
    :ivar int ship_date: default value: 719163
    :ivar int return_date: default value: 719163
    :ivar float user_float_1: default value: 0.0
    :ivar float user_float_2: default value: 0.0
    :ivar float user_float_3: default value: 0.0
    :ivar int user_integer_1: default value: 0
    :ivar int user_integer_2: default value: 0
    :ivar int user_integer_3: default value: 0
    :ivar str user_string_1: default value: ''
    :ivar str user_string_2: default value: ''
    :ivar str user_string_3: default value: ''
    """

    def __init__(self):
        """
        Method to initialize a dataset Record data model instance.
        """

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dict attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.survival_id = 0
        self.assembly_id = 0
        self.assembly_name = ''
        self.failure_date = 719163
        self.left_interval = 0.0
        self.right_interval = 0.0
        self.status = 0                     # 1 = Event
                                            # 2 = Right Censored
                                            # 3 = Left Censored
                                            # 4 = Interval Censored
        self.n_failures = 0
        self.interarrival_time = 0.0
        self.mode_type = 0
        self.nevada_chart = 0
        self.ship_date = 719163
        self.return_date = 719163
        self.user_float_1 = 0.0
        self.user_float_2 = 0.0
        self.user_float_3 = 0.0
        self.user_integer_1 = 0
        self.user_integer_2 = 0
        self.user_integer_3 = 0
        self.user_string_1 = ''
        self.user_string_2 = ''
        self.user_string_3 = ''


class Record(object):
    """
    The dataset Record data controller provides an interface between the
    dataset Record data model and an RTK view model.  A single dataset Record
    controller can manage one or more dataset Record data models.  The
    attributes of a dataset Record data controller are:

    :ivar _dao: the :py:class:`rtk.dao.DAO` to use when communicating with the
                RTK Project database.
    :ivar int _last_id: the last dataset Record ID used.
    :ivar dict dicRecords: Dictionary of the dataset Record data models
                           managed.  Key is the dataset Record ID; value is a
                           pointer to the dataset Record data model instance.
    """

    def __init__(self):
        """
        Method to initialize a dataset Record data controller instance.
        """

        pass
