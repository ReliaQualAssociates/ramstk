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

    def set_attributes(self, values):
        """
        Method to set the dataset Record data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''
# TODO: Change the assembly_id to type int.
        try:
            self.survival_id = int(values[0])
            self.assembly_name = str(values[1])
            self.failure_date = int(values[2])
            self.left_interval = float(values[3])
            self.right_interval = float(values[4])
            self.status = int(values[5])
            self.n_failures = int(values[6])
            self.interarrival_time = float(values[7])
            self.mode_type = int(values[8])
            self.nevada_chart = int(values[9])
            self.ship_date = int(values[10])
            self.return_date = int(values[11])
            self.user_float_1 = float(values[12])
            self.user_float_2 = float(values[13])
            self.user_float_3 = float(values[14])
            self.user_integer_1 = int(values[15])
            self.user_integer_2 = int(values[16])
            self.user_integer_3 = int(values[17])
            self.user_string_1 = str(values[18])
            self.user_string_2 = str(values[19])
            self.user_string_3 = str(values[20])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Verificaiton data model
        attributes.

        :return: (survival_id, assembly_name, failure_date, left_interval,
                  right_interval, status, n_failures, interarrival_time,
                  mode_type, nevada_chart, ship_date, return_date,
                  user_float_1, user_float_2, user_float_3, user_integer_1,
                  user_integer_2, user_integer_3, user_string_1, user_string_2,
                  user_string_3)
        :rtype: tuple
        """

        _values = (self.survival_id, self.assembly_name, self.failure_date,
                   self.left_interval, self.right_interval, self.status,
                   self.n_failures, self.interarrival_time, self.mode_type,
                   self.nevada_chart, self.ship_date, self.return_date,
                   self.user_float_1, self.user_float_2, self.user_float_3,
                   self.user_integer_1, self.user_integer_2,
                   self.user_integer_3, self.user_string_1, self.user_string_2,
                   self.user_string_3)

        return _values


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
