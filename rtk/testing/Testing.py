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
