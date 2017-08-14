#!/usr/bin/env python -O
"""
This is the test class for testing Growth Testing module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.testing.TestGrowth.py is part of The RTK Project
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
import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from testing.growth.Growth import Model, Growth

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestGrowthController(unittest.TestCase):
    """
    Class for testing the Growth data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Growth class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Growth()

    @attr(all=True, integration=True)
    def test_request_tests(self):
        """
        (TestGrowth) request_tests should return 0 on success
        """

        _test = (0, 7, 1, u'Test Plan', u'Description', 4, u'Attachment', 0.0,
                 0, 0.75, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 1, 0.0, 0.3, 0.0, 0.7,
                 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.assertEqual(self.DUT.request_tests(self._dao, _test)[1], 0)

    @attr(all=True, integration=True)
    def test_request_test_data(self):
        """
        (TestGrowth) _request_test_data should return a tuple on success
        """

        _test = (0, 7, 1, u'Test Plan', u'Description', 4, u'Attachment', 0.0,
                 0, 0.75, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 1, 0.0, 0.3, 0.0, 0.7,
                 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        self.DUT._dao = self._dao

        self.DUT.request_tests(self._dao, _test)
        _test_id = min(self.DUT.dicTests.keys())

        self.assertEqual(self.DUT._request_test_data(_test_id),
                         ([(1, 719163, 0.0, 2.7, 1), (2, 719163, 0.0, 10.3, 1), (3, 719163, 0.0, 30.6, 1), (4, 719163, 0.0, 57.0, 1), (5, 719163, 0.0, 61.3, 1), (6, 719163, 0.0, 80.0, 1), (7, 719163, 0.0, 109.5, 1), (8, 719163, 0.0, 125.0, 1), (9, 719163, 0.0, 128.6, 1), (10, 719163, 0.0, 143.8, 1), (11, 719163, 0.0, 167.9, 1), (12, 719163, 0.0, 229.2, 1), (13, 719163, 0.0, 269.7, 1), (14, 719163, 0.0, 320.6, 1), (15, 719163, 0.0, 328.2, 1), (16, 719163, 0.0, 366.2, 1), (17, 719163, 0.0, 396.7, 1), (18, 719163, 0.0, 421.1, 1), (19, 719163, 0.0, 438.2, 1), (20, 719163, 0.0, 501.2, 1), (21, 719163, 0.0, 620.0, 1)], 0))

# TODO: Test that method fails when no Testing inputs exist in database.
    @attr(all=True, integration=True)
    def test_add_test(self):
        """
        (TestGrowth) add_test returns 0 on success and new Testing data model added to dictionary
        """

        _test = (0, 7, 1, u'Test Plan', u'Description', 4, u'Attachment', 0.0,
                 0, 0.75, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 1, 0.0, 0.3, 0.0, 0.7,
                 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.assertEqual(self.DUT.request_tests(self._dao, _test)[1], 0)
        (_results, _error_code) = self.DUT.add_test(0, 7)

        self.assertTrue(isinstance(self.DUT.dicTests[self.DUT._last_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=False)
    def test_delete_test(self):
        """
        (TestGrowth) delete_test returns 0 on success
        """

        _test = (0, 7, 1, u'Test Plan', u'Description', 4, u'Attachment', 0.0,
                 0, 0.75, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 1, 0.0, 0.3, 0.0, 0.7,
                 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.assertEqual(self.DUT.request_tests(self._dao, _test)[1], 0)
        (_results,
         _error_code) = self.DUT.delete_test(self.DUT._last_id - 1)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_test(self):
        """
        (TestGrowth) save_test returns (True, 0) on success
        """

        _test = (0, 7, 1, u'Test Plan', u'Description', 4, u'Attachment', 0.0,
                 0, 0.75, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 1, 0.0, 0.3, 0.0, 0.7,
                 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.DUT.request_tests(self._dao, _test)
        self.assertEqual(self.DUT.save_test(1), (True, 0))

    @attr(all=True, integration=True)
    def test_save_all_tests(self):
        """
        (TestGrowth) save_all_tests returns False on success
        """

        _test = (0, 7, 1, u'Test Plan', u'Description', 4, u'Attachment', 0.0,
                 0, 0.75, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 1, 0.0, 0.3, 0.0, 0.7,
                 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.DUT.request_tests(self._dao, _test)
        self.assertFalse(self.DUT.save_all_tests())
