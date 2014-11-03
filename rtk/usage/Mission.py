#!/usr/bin/env python
"""
##############
Mission Module
##############
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       Mission.py is part of The RTK Project
#
# All rights reserved.


class Model(object):
    """
    The Mission data model contains the attributes and methods of a mission.
    A Usage Profile will consist of one or more missions.  The attributes of a
    Mission are:

    :ivar dicPhases: Dictionary of the Phases associated with the Mission.
    Key is the Phase ID; value is a pointer to the instance of the Phase data
    model.

    :ivar revision_id: default value: 0
    :ivar mission_id: default value: 0
    :ivar time: default value: 0.0
    :ivar time_units: default value: ''
    :ivar description: default value: ''
    """

    def __init__(self):
        """
        Method to initialize a Mission data model instance.
        """

        # Set public dict attribute default values.
        self.dicPhases = {}

        # Set public scalar attribute default values.
        self.revision_id = 0
        self.mission_id = 0
        self.time = 0.0
        self.time_units = ''
        self.description = ''

    def set_attributes(self, values):
        """
        Method to set the Mission data model attributes.

        :param tuple values: values to assign to the attributes.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error = False

        try:
            self.revision_id = int(values[0])
            self.mission_id = int(values[1])
            self.time = float(values[2])
            self.time_units = str(values[3])
            self.description = str(values[4])
        except(IndexError, ValueError, TypeError):
            _error = True

        return _error

    def get_attributes(self):
        """
        Method to retrieve the current values of the Mission data model
        attributes.

        :return: values; the values of the attributes.
        :rtype: tuple
        """

        return(self.mission_id, self.time, self.time_units, self.description)


class Mission(object):
    """
    The Mission controller provides an interface between the Mission data model
    and an RTK view model.  A single Mission controller can control one or more
    Mission data models.  Currently the Mission controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Mission controller instance.
        """

        pass
