#!/usr/bin/env python
"""
##############
Mission Module
##############
"""

# -*- coding: utf-8 -*-
#
#       rtk.usage.Mission.py is part of The RTK Project
#
# All rights reserved.

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Mission data model contains the attributes and methods of a mission.
    A Usage Profile will consist of one or more missions.  The attributes of a
    Mission are:

    :ivar dict dicPhases: Dictionary of the Phases associated with the Mission.
                          Key is the Phase ID; value is a pointer to the
                          instance of the Phase data model.
    :ivar int revision_id: the ID of the Revision this Mission is associated
                           with.
    :ivar int mission_id: the ID of the Mission.
    :ivar float time: the total length of the Mission.
    :ivar str time_units: the time units for the Mission time.
    :ivar str description: the description of the Mission.
    """

    def __init__(self):
        """
        Method to initialize a Mission data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicPhases = {}

        # Define public list attributes.

        # Define public scalar attributes.
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
