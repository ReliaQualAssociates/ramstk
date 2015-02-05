#!/usr/bin/env python -O
"""
This is the test class for testing BoM module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.hardware.TestBoM.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from hardware.BoM import *


class TestBoMController(unittest.TestCase):
    """
    Class for testing the BoM data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the BoM class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = BoM()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestBoM) __init__ should create a BoM data controller
        """

        self.assertTrue(isinstance(self.DUT, BoM))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicHardware, {})

    @attr(all=True, integration=True)
    def test_request_bom(self):
        """
        (TestBoM) request_bom should return 0 on success
        """

        self.assertEqual(self.DUT.request_bom(self._dao, 0)[1], 0)

    @attr(all=True, integration=True)
    def test_add_hardware_assembly(self):
        """
        (TestBoM) add_hardware should return 0 on success
        """

        self.assertEqual(self.DUT.request_bom(self._dao, 0)[1], 0)
        self.assertEqual(self.DUT.add_hardware(0, 0, 0)[1], 0)

    @attr(all=True, integration=True)
    def test_delete_hardware(self):
        """
        (TestBoM) delete_hardware returns 0 on success
        """

        self.assertEqual(self.DUT.request_bom(self._dao, 0)[1], 0)
        (_results,
         _error_code) = self.DUT.delete_hardware(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_hardware_item(self):
        """
        (TestBoM) save_hardware_item returns (True, 0) on success
        """

        self.DUT.request_bom(self._dao, 0)
        self.assertEqual(self.DUT.save_hardware_item(2), (True, 0))

    @attr(all=True, integration=True)
    def test_save_bom(self):
        """
        (TestBoM) save_bom returns False on success
        """

        self.DUT.request_bom(self._dao, 0)
        self.assertFalse(self.DUT.save_bom())
