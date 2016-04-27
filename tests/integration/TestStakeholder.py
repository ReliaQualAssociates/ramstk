#!/usr/bin/env python -O
"""
This is the test class for testing Stakeholder module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestStakeholder.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from stakeholder.Stakeholder import Model, Stakeholder

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestStakeholderController(unittest.TestCase):
    """
    Class for testing the Stakeholder data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Stakeholder class.
        """

        _database = '/tmp/tempdb.rtk'

        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Stakeholder()

    @attr(all=True, integration=True)
    def test00_request_inputs(self):
        """
        (TestStakeholder) request_inputs should return 0 on success
        """

        self.assertEqual(self.DUT.request_inputs(self._dao, 0)[1], 0)
# TODO: Test that method fails when no Stakeholder inputs exist in database.
    @attr(all=True, integration=True)
    def test01_add_input(self):
        """
        (TestStakeholder) add_input returns 0 on success and new Stakeholder data model added to dictionary
        """

        self.assertEqual(self.DUT.request_inputs(self._dao, 0)[1], 0)
        (_results,
         _error_code) = self.DUT.add_input(0)

        self.assertTrue(isinstance(self.DUT.dicStakeholders[self.DUT._last_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test02_delete_input(self):
        """
        (TestStakeholder) delete_input returns 0 on success
        """

        self.assertEqual(self.DUT.request_inputs(self._dao, 0)[1], 0)
        (_results,
         _error_code) = self.DUT.delete_input(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test03_save_input(self):
        """
        (TestStakeholder) save_input returns (True, 0) on success
        """

        self.DUT.request_inputs(self._dao, 0)
        self.assertEqual(self.DUT.save_input(1), (True, 0))

    @attr(all=True, integration=True)
    def test04_save_all_inputs(self):
        """
        (TestStakeholder) save_all_inputs returns False on success
        """

        self.DUT.request_inputs(self._dao, 0)
        self.assertFalse(self.DUT.save_all_inputs())

    @attr(all=True, integration=True)
    def test05_calculate_stakeholder(self):
        """
        (TestStakeholder) calculate_stakeholder returns 0 on success
        """

        self.DUT.request_inputs(self._dao, 0)
        self.assertEqual(self.DUT.calculate_stakeholder(1), (0.8, 0.8))
