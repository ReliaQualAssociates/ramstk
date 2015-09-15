#!/usr/bin/env python
"""
###########################
Testing Package Data Module
###########################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.testing.Testing.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Function to convert string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        _error_code = 1000                  # pragma: no cover

    return _error_code


class Model(object):
    """
    The Testing data model contains the attributes and methods of a test. The
    attributes of a Testing model are:

    :ivar int _int_mission_id: default value: -1
    :ivar float _flt_test_termination_time: default value: 0.0
    :ivar int revision_id: default value: None
    :ivar int assembly_id: default value: None
    :ivar int test_id: default value: 0
    :ivar str name: default value: ''
    :ivar str description: default value: ''
    :ivar str attachment: default value: ''
    :ivar int test_type: default value: 0
    :ivar float cum_time: default value: 0.0
    :ivar float cum_failures: default value: 0.0
    :ivar float confidence: default value: 0.75
    :ivar float consumer_risk: default value: 0.0
    :ivar float producer_risk: default value: 0.0
    """

    def __init__(self):
        """
        Method to initialize a Testing data model instance.
        """

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._int_mission_id = -1

        # Initialize public dict attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.revision_id = None
        self.assembly_id = None
        self.test_id = 0
        self.name = ''
        self.description = ''
        self.attachment = ''
        self.test_type = 0
        self.cum_time = 0.0
        self.cum_failures = 0
        self.confidence = 0.75
        self.consumer_risk = 0.0
        self.producer_risk = 0.0
        self.test_termination_time = 0.0

    def set_attributes(self, values):
        """
        Method to set the Testing data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.revision_id = int(values[0])
            self.assembly_id = int(values[1])
            self.test_id = int(values[2])
            self.name = str(values[3])
            self.description = str(values[4])
            self.test_type = int(values[5])
            self.attachment = str(values[6])
            self.cum_time = float(values[7])
            self.cum_failures = int(values[8])
            self.confidence = float(values[9])
            self.consumer_risk = float(values[10])
            self.producer_risk = float(values[11])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Testing data model attributes.

        :return: (revision_id, assembly_id, test_id, name, description,
                  attachment, test_type, cum_time, cum_failures, confidence,
                  consumer_risk, producer_risk)
        :rtype: tuple
        """

        _values = (self.revision_id, self.assembly_id, self.test_id,
                   self.name, self.description, self.test_type,
                   self.attachment, self.cum_time, self.cum_failures,
                   self.confidence, self.consumer_risk, self.producer_risk)

        return _values


class Testing(object):
    """
    The Testing data controller provides an interface between the Testing data
    model and an RTK view model.  A single Testing controller can manage one or
    more Testing data models.  The attributes of a Testing data controller are:

    :ivar _dao: the :class:`rtk.dao.DAO` to use when communicating with the RTK
                Project database.
    :ivar _last_id: the last Testing ID used.
    :ivar dicTests: Dictionary of the Testing data models managed.  Key is the
                    Test ID; value is a pointer to the Testing data model
                    instance.
    """

    def __init__(self):
        """
        Initializes a Testing data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicTests = {}

    def request_tests(self, dao, revision_id):
        """
        Reads the RTK Project database and loads all the stakeholder inputs
        associated with the selected Revision.  For each stakeholder input
        returned:

        #. Retrieve the inputs from the RTK Project database.
        #. Create a Testing data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Testings being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :param int revision_id: the Revision ID to select the stakeholders for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self._last_id = self._dao.get_last_id('rtk_tests')[0]

        _query = "SELECT * FROM rtk_tests \
                  WHERE fld_revision_id={0:d}".format(revision_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_tests = len(_results)
        except TypeError:
            _n_tests = 0

        for i in range(_n_tests):
            _test = Model()
            _test.set_attributes(_results[i])
            self.dicTests[_test.test_id] = _test

        return(_results, _error_code)
