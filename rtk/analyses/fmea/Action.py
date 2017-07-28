#!/usr/bin/env python
"""
##################
FMEA Action Module
##################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Action.py is part of The RTK Project
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

# Import other RTK modules.
try:
    import Utilities as _util
except ImportError:                         # pragma: no cover
    import rtk.Utilities as _util

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Action data model contains the attributes and methods of a FMEA
    action.  A Mechanism or a Cause will contain of one or more Actions.
    The attributes of an Action are:

    :ivar int mode_id: the ID of the failure Mode this Action is associated
                       with.
    :ivar int mechanism_id: the ID of the failure Mechanism this Action is
                            associated with.
    :ivar int cause_id: the ID of the failure Cause this Action is associated
                        with.
    :ivar int action_id: the ID of this Action.
    :ivar str action_recommended: the description of the recommended Action.
    :ivar int action_category: the index of the category of this Action.
    :ivar int action_owner: the index of the owner of this Action.
    :ivar int action_due_date: the ordinal due date of this Action.
    :ivar int action_status: the index of the status of this Action.
    :ivar str action_taken: the description of the Action actually taken.
    :ivar int action_approved: indicates whether or not the Action is approved.
    :ivar int action_approved_date: the ordinal date the Action was approved.
    :ivar int action_closed: indicates whether or not the Action is closed.
    :ivar int action_closed_date: the ordinal date the Action was closed.
    """

    def __init__(self):
        """
        Method to initialize an Action data model instance.
        """

        # Set public scalar attribute default values.
        self.mode_id = 0
        self.mechanism_id = 0
        self.cause_id = 0
        self.action_id = 0
        self.action_recommended = ''
        self.action_category = 0
        self.action_owner = 0
        self.action_due_date = 0
        self.action_status = 0
        self.action_taken = ''
        self.action_approved = 0
        self.action_approved_date = 0
        self.action_closed = 0
        self.action_closed_date = 0

    def set_attributes(self, values):
        """
        Method to set the Actopm data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.mode_id = int(values[0])
            self.mechanism_id = int(values[1])
            self.cause_id = int(values[2])
            self.action_id = int(values[3])
            self.action_recommended = str(values[4])
            self.action_category = int(values[5])
            self.action_owner = int(values[6])
            self.action_due_date = int(values[7])
            self.action_status = int(values[8])
            self.action_taken = str(values[9])
            self.action_approved = int(values[10])
            self.action_approved_date = int(values[11])
            self.action_closed = int(values[12])
            self.action_closed_date = int(values[13])
        except IndexError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."
        except ValueError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Wrong input data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Action data model
        attributes.

        :return: (mode_id, mechanism_id, cause_id, action_id,
                  action_recommended, action_category, action_owner,
                  action_due_date, action_status, action_taken,
                  action_approved, action_approved_date, action_closed,
                  action_closed_date)
        :rtype: tuple
        """

        return(self.mode_id, self.mechanism_id, self.cause_id, self.action_id,
               self.action_recommended, self.action_category,
               self.action_owner, self.action_due_date, self.action_status,
               self.action_taken, self.action_approved,
               self.action_approved_date, self.action_closed,
               self.action_closed_date)


class Action(object):
    """
    The Action data controller provides an interface between the Action data
    model and an RTK view model.  A single Action controller can control one
    or more Action data models.  Currently the Action controller is unused.
    """

    def __init__(self):
        """
        Method to initialize an Action data controller instance.
        """

        pass
