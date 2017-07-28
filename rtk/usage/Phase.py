#!/usr/bin/env python
"""
####################
Mission Phase Module
####################
"""

# -*- coding: utf-8 -*-
#
#       rtk.usage.Phase.py is part of The RTK Project
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

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Phase data model contains the attributes and methods of a mission
    phase.  A Mission will consist of one or more mission phases.  The
    attributes of a Phase are:

    :ivar dict dicEnvironments: Dictionary of the Environments associated with
                                the Phase.  Key is the Environment ID, value is
                                a pointer to the instance of the Environment
                                data model.
    :ivar int revision_id: the ID of the Revision this Phase is associated
                           with.
    :ivar int mission_id: the ID of the Mission this Phase belongs to.
    :ivar int phase_id: the ID of the Phase.
    :ivar float start_time: the Mission time the Phase begins.
    :ivar float end_time: the Mission time the Phase ends.
    :ivar str code: the Phase code.
    :ivar str description: the description of the Mission Phase.
    """

    def __init__(self):
        """
        Method to initialize a Phase data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicEnvironments = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.revision_id = 0
        self.mission_id = 0
        self.phase_id = 0
        self.start_time = 0.0
        self.end_time = 0.0
        self.code = ''
        self.description = ''

    def set_attributes(self, values):
        """
        Method to set the Phase data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error = False

        try:
            self.revision_id = int(values[0])
            self.mission_id = int(values[1])
            self.phase_id = int(values[2])
            self.start_time = float(values[3])
            self.end_time = float(values[4])
            self.code = str(values[5])
            self.description = str(values[6])
        except(IndexError, ValueError, TypeError):
            _error = True

        return _error

    def get_attributes(self):
        """
        Method to retrieve the current values of the Phase data model
        attributes.

        :return: value of instance attributes
        :rtype: tuple
        """

        return(self.revision_id, self.mission_id, self.phase_id,
               self.start_time, self.end_time, self.code, self.description)


class Phase(object):
    """
    The Phase controller provides an interface between the Phase data model
    and an RTK view model.  A single Phase controller can control one or more
    Phase data models.  Currently the Phase controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Phase controller instance.
        """

        pass
