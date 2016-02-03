#!/usr/bin/env python
"""
###################################
Dataset Package Dataset Sub-Module
###################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.survival.Dataset.py is part of The RTK Project
#
# All rights reserved.

try:
    import Utilities as _util
    from analyses.statistics.Distributions import time_between_failures
except ImportError:
    import rtk.Utilities as _util
    from rtk.analyses.statistics.Distributions import time_between_failures

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'


class Model(object):                       # pylint: disable=R0902, R0904
    """
    The Dataset data model contains the attributes and methods for a
    The Dataset data model contains the attributes and methods for a
    Dataset. The attributes of an Dataset model are:

    :ivar self.dicRecords: default value: {}
    :ivar survival_id: default value: None
    :ivar dataset_id: default value: None
    """

    def __init__(self):
        """
        Method to initialize a Dataset data model instance.
        """

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dict attributes.
        self.dicRecords = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.survival_id = None
        self.dataset_id = None

    def set_attributes(self, values):
        """
        Method to set the Dataset data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.survival_id = int(values[0])
            self.dataset_id = int(values[1])
        except IndexError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def load_records(self, records):
        """
        Method to populate the Records dictionary.

        :param tuple records: the records to populate the dictionare with.
        :return:
        :rtype:
        """

        for _record in records:
            self.dicRecords[_record[0]] = list(_record[1:])

        return

    def get_attributes(self):
        """
        Retrieves the current values of the Verificaiton data model attributes.

        :return: (survival_id, dataset_id, dicRecords)
        :rtype: tuple
        """

        _values = (self.survival_id, self.dataset_id, self.dicRecords)

        return _values

    def calculate_tbf(self, previous_id, current_id):
        """
        Method to calculate the time between failure of subsequent failures in
        a dataset.

        :param int previous_id: the Record ID of the previous failure or
                                suspension.
        :param int current_id: the Record ID of the current failure or
                               suspension.
        :return: False on success or True if an error is encountered.
        :rtype: boolean
        """

        _p_record = self.dicRecords[previous_id]
        _c_record = self.dicRecords[current_id]

        _previous = [previous_id, _p_record[0], _p_record[2], _p_record[3],
                     _p_record[5], _p_record[4]]
        _current = [current_id, _c_record[0], _c_record[2], _c_record[3],
                    _c_record[5], _c_record[4]]

        _c_record[6] = time_between_failures(_previous, _current)

        return False


class Dataset(object):
    """
    The Dataset data controller provides an interface between the Dataset
    data model and an RTK view model.  A single Dataset controller can
    manage one or more Dataset data models.  The attributes of a
    Dataset data controller are:

    :ivar _dao: the :class:`rtk.dao.DAO` to use when communicating with the RTK
                Project database.
    :ivar int _last_id: the last Dataset ID used.
    :ivar dict dicDatasets: Dictionary of the Dataset data models managed.
                             Key is the Dataset ID; value is a pointer to the
                             Dataset data model instance.
    """

    def __init__(self):
        """
        Initializes a Dataset data controller instance.
        """

        pass
