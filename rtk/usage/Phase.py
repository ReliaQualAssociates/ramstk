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
