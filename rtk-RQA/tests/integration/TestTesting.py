#!/usr/bin/env python -O
"""
This is the test class for testing Testing module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestTesting.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from testing.Testing import Testing

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestTestingController(unittest.TestCase):
    """
    Class for testing the Testing data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Testing class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Testing()

    @attr(all=True, integration=True)
    def test00_request_tests(self):
        """
        (TestTesting) request_inputs should return 0 on success
        """

        self.assertEqual(self.DUT.request_tests(self._dao, 0)[1], 0)
