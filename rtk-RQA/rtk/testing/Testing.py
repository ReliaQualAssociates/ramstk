#!/usr/bin/env python
"""
###########################
Testing Package Data Module
###########################
"""

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
    import Configuration
    import Utilities as Utilities
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Testing data model contains the attributes and methods of a test. The
    attributes of a Testing model are:

    :ivar int _int_mission_id:
    :ivar int revision_id:
    :ivar int assembly_id:
    :ivar int test_id:
    :ivar str name:
    :ivar str description:
    :ivar str attachment:
    :ivar int test_type:
    :ivar float cum_time:
    :ivar float cum_failures:
    :ivar float confidence:
    :ivar float consumer_risk:
    :ivar float producer_risk:
    """

    def __init__(self):
        """
        Method to initialize a Testing data model instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._int_mission_id = -1

        # Initialize public dictionary attributes.

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
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Testing data model
        attributes.

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
        Method to initialize a Testing data controller instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicTests = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_tests(self, dao, revision_id):
        """
        Method to read the RTK Project database and load all the tests
        associated with the selected Revision.  For each tests returned:

        #. Retrieve the inputs from the RTK Project database.
        #. Create a Testing data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Testings being managed
           by this controller.

        :param dao: the :py:class:`rtk.DAO.DAO` to use for communicating with
                    the RTK Project database.
        :param int revision_id: the Revision ID to select the Tests for.
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
