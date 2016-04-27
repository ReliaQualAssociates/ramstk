#!/usr/bin/env python
"""
##################
Environment Module
##################
"""

# -*- coding: utf-8 -*-
#
#       rtk.usage.Environment.py is part of The RTK Project
#
# All rights reserved.

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Environment data model contains the attributes and methods of a mission
    phase environment.  A Phase will consist of zero or more environments.  The
    attributes of an Environment are:

    :ivar int revision_id: the ID of the Revision the Environment is associated
                           with.
    :ivar int mission_id: the ID of the Mission the Environment is associated
                          with.
    :ivar int phase_id: the ID of the Phase the Environment is associated with.
    :ivar int test_id:
    :ivar int environment_id: the ID of the Environment.
    :ivar str name: the name of the Environment parameter.
    :ivar str units: the measurement units for the Environment parameter.
    :ivar float minimum: the expected maximum value of the Envionment
                         parameter.
    :ivar float maximum: the expected minimum value of the Envionment
                         parameter.
    :ivar float mean: the expected average of the Environment parameter.
    :ivar float variance: the expected variance on the Environment parameter.
    """

    def __init__(self):
        """
        Method to initialize an Environment data model instance.
        """

        self.revision_id = 0
        self.mission_id = 0
        self.phase_id = 0
        self.test_id = 0
        self.environment_id = 0
        self.name = ''
        self.units = ''
        self.minimum = 0.0
        self.maximum = 0.0
        self.mean = 0.0
        self.variance = 0.0

    def set_attributes(self, values):
        """
        Method to set the Environment data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error = False

        try:
            self.revision_id = int(values[0])
            self.mission_id = int(values[1])
            self.phase_id = int(values[2])
            self.test_id = int(values[3])
            self.environment_id = int(values[4])
            self.name = str(values[5])
            self.units = str(values[6])
            self.minimum = float(values[7])
            self.maximum = float(values[8])
            self.mean = float(values[9])
            self.variance = float(values[10])
        except(IndexError, ValueError):
            _error = True

        return _error

    def get_attributes(self):
        """
        Method to retrieve the current values of the Environment data model
        attributes.

        :return: (revision_id, mission_id, phase_id, test_id, environment_id,
                  name, units, minimum, maximum, mean, variance)
        :rtype: tuple
        """

        return(self.revision_id, self.mission_id, self.phase_id, self.test_id,
               self.environment_id, self.name, self.units, self.minimum,
               self.maximum, self.mean, self.variance)


class Environment(object):
    """
    The Environment controller provides an interface between the Environment
    data model and an RTK view model.  A single Environment controller can
    control one or more Environment data models.  Currently the Environment
    controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Environment controller instance.
        """

        pass
