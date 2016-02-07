#!/usr/bin/env python -O
"""
This is the test class for testing the Usage Profile module algorithms and
models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestProfile.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from usage.UsageProfile import UsageProfile

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestUsageProfileController(unittest.TestCase):
    """
    Class for testing the Usage Profile controller class.
    """

    def setUp(self):

        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = UsageProfile()
        self.DUT._dao = self._dao

    @attr(all=True, integration=True)
    def test_request_profile(self):
        """
        Method to test that a Usage Profile can be loaded from a Project
        database.
        """

        self.assertFalse(self.DUT.request_profile())

    @attr(all=True, integration=True)
    def test_add_mission(self):
        """
        Method to test that a mission can be added to the Usage Profile.
        """

        (_results, _error_code, _last_id) = self.DUT.add_mission(0)
        self.assertEqual(_error_code, 0)
        #self.assertTrue(isinstance(self.DUT.dicMissions[_last_id], Mission))

    @attr(all=True, integration=True)
    def test_save_mission(self):
        """
        Method to test that a Mission can be saved to the database.
        """

        self.assertEqual(self.DUT._save_mission(), ([], 0))

    @attr(all=True, integration=True)
    def test_delete_mission(self):
        """
        Method to test that a mission can be deleted from the Usage Profile.
        """

        _n = len(self.DUT.dicMissions)

        self.assertEqual(self.DUT.delete_mission(_n - 1), ([], 0))
        self.assertTrue(self.DUT.delete_mission(_n))

    @attr(all=True, integration=True)
    def test_add_phase(self):
        """
        Method to test that a phase can be added.
        """

        (_results, _error_code, _last_id) = self.DUT.add_phase()
        self.assertEqual(_error_code, 0)
        self.assertTrue(isinstance(self.DUT.dicPhases[_last_id], Phase))

    @attr(all=True, integration=True)
    def test_save_phase(self):
        """
        Method to test that a Phase can be saved to the database.
        """

        self.assertEqual(self.DUT.save(), ([], 0))

    @attr(all=True, integration=True)
    def test_delete_phase(self):
        """
        Method to test that a phase can be deleted.
        """

        _n = len(self.DUT.dicPhases)

        self.assertEqual(self.DUT.delete_phase(_n - 1), ([], 0))
        self.assertTrue(self.DUT.delete_phase(_n))

    @attr(all=True, integration=True)
    def test_add_environment(self):
        """
        Method to test that an Environment can be added.
        """

        (_results, _error_code, _last_id) = self.DUT.add_environment()
        self.assertEqual(_error_code, 0)
        self.assertTrue(isinstance(self.DUT.dicEnvironments[_last_id],
                                   Environment))

    @attr(all=True, integration=True)
    def test_delete_environment(self):
        """
        Method to test that an evironment can be deleted.
        """

        _n = len(self.DUT.dicEnvironments)

        self.assertEqual(self.DUT.delete_environment(_n - 1), ([], 0))
        self.assertTrue(self.DUT.delete_environment(_n))
