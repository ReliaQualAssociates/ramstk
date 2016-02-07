#!/usr/bin/env python -O
"""
This is the test class for testing Growth Testing module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.testing.TestGrowth.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr
import numpy as np

import dao.DAO as _dao
from testing.growth.Growth import Growth

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

        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
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
        (TestGrowth) request_test_data should return a tuple on success
        """

        _test = (0, 7, 1, u'Test Plan', u'Description', 4, u'Attachment', 0.0,
                 0, 0.75, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 1, 0.0, 0.3, 0.0, 0.7,
                 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        self.DUT._dao = self._dao

        self.DUT.request_tests(self._dao, _test)
        _test_id = min(self.DUT.dicTests.keys())

        self.assertEqual(self.DUT._request_test_data(_test_id), ([], 0))

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
