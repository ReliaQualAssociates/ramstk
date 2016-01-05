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

    :ivar dicEnvironments: Dictionary of the Environments associated with the
    Phase.  Key is the Environment ID, value is a pointer to the instance of
    the Environment data model.

    :ivar revision_id: default value: 0
    :ivar mission_id: default value: 0
    :ivar phase_id: default value: 0
    :ivar start_time: default value: 0.0
    :ivar end_time: default value: 0.0
    :ivar code: default value: ''
    :ivar description: default value: ''
    """

    def __init__(self):
        """
        Method to initialize a Phase data model instance.
        """

        # Set public dict attribute default values.
        self.dicEnvironments = {}

        # Set public scalar attribute default values.
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
