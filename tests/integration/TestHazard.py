#!/usr/bin/env python -O
"""
This is the test class for testing Hazard module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestHazard.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from analyses.hazard.Hazard import Hazard

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2015 Andrew "weibullguy" Rowland'


class TestHazardController(unittest.TestCase):
    """
    Class for testing the Hazard data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Hazard class.
        """

        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Hazard()

    @attr(all=True, integration=True)
    def test_request_hazard(self):
        """
        (TestHazard) request_hazard should return 0 on success
        """

        self.assertEqual(self.DUT.request_hazard(self._dao)[1], 0)

    @attr(all=True, integration=True)
    def test_add_hazard(self):
        """
        (TestHazard) add_hazard should return 0 on success
        """

        self.assertEqual(self.DUT.request_hazard(self._dao)[1], 0)
        self.assertEqual(self.DUT.add_hazard(0)[1], 0)

    @attr(all=True, integration=True)
    def test_delete_hazard(self):
        """
        (TestHazard) delete_hazard should return 0 on success
        """
# TODO: Get last id to delete.
        self.assertEqual(self.DUT.request_hazard(self._dao)[1], 0)
        (_results,
         _error_code) = self.DUT.delete_hazard(0, 1)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_calculate_hazard(self):
        """
        (TestHazard) calculate_hazard should return False on success
        """

        self.assertEqual(self.DUT.request_hazard(self._dao)[1], 0)
        self.assertFalse(self.DUT.calculate_hazard(0, 2))

    @attr(all=True, integration=True)
    def test_save_hazard(self):
        """
        (TestHazard) save_hazard returns (True, 0) on success
        """

        self.assertEqual(self.DUT.request_hazard(self._dao)[1], 0)
        self.assertEqual(self.DUT.save_hazard(0, 2), (True, 0))

    @attr(all=True, integration=True)
    def test_save_all_hazards(self):
        """
        (TestHazard) save_all_hazards returns False on success
        """

        self.assertEqual(self.DUT.request_hazard(self._dao)[1], 0)
        self.assertFalse(self.DUT.save_all_hazards())
