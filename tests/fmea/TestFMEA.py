#!/usr/bin/env python -O
"""
This is the test class for testing the FMEA class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       TestFMEA.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao

from analyses.fmea.FMEA import *


class TestFMEAModel(unittest.TestCase):
    """
    Class for testing the FMEA model class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the FMEA model class.
        """

        self.FDUT = Model(None, 0)
        self.HDUT = Model(0, None)

    @attr(all=True, unit=True)
    def test_function_FMEA_create(self):
        """
        (TestFMEA) __init__ should return instance of Function FMEA data model
        """

        DUT = Model(None, 0)

        self.assertTrue(isinstance(DUT, Model))
        self.assertEqual(DUT.dicModes, {})
        self.assertEqual(DUT.assembly_id, None)
        self.assertEqual(DUT.function_id, 0)

    @attr(all=True, unit=True)
    def test_hardware_FMEA_create(self):
        """
        (TestFMEA) __init__ should return instance of Hardware FMEA data model
        """

        DUT = Model(0, None)

        self.assertTrue(isinstance(DUT, Model))
        self.assertEqual(DUT.dicModes, {})
        self.assertEqual(DUT.assembly_id, 0)
        self.assertEqual(DUT.function_id, None)

    @attr(all=True, unit=True)
    def test_FMEA_create_parent_problem(self):
        """
        (TestFMEA) __init__ raises ParentError for None, None or int, int input
        """

        self.assertRaises(ParentError, Model, None, None)
        self.assertRaises(ParentError, Model, 2, 10)

    #@attr(all=True, unit=True)
    #def test_rpn(self):
    #    """
    #    (TestFMEA) calculate always returns a value between 1 - 1000
    #    """

    #    for severity in range(1, 11):
    #        for occurrence in range(1, 11):
    #            for detection in range(1, 11):
    #                self.assertIn(self.DUT.calculate(severity,
    #                                                 occurrence,
    #                                                 detection),
    #                              range(1, 1001))

    #@attr(all=True, unit=True)
    #def test_rpn_out_of_range_inputs(self):
    #    """
    #    (TestFMEA) calculate raises OutOfRangeError for 10 < input < 1
    #    """

    #    self.assertRaises(OutOfRangeError, self.DUT.calculate, 0, 1, 1)
    #    self.assertRaises(OutOfRangeError, self.DUT.calculate, 11, 1, 1)
    #    self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 0, 1)
    #    self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 11, 1)
    #    self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 1, 0)
    #    self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 1, 11)


class TestFMEAController(unittest.TestCase):
    """
    Class for testing the FMEA data controller class.
    """

    def setUp(self):

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = FMEA()
        self.DUT._dao = self._dao

    @attr(all=True, unit=True, integration=True)
    def test_create_controller(self):
        """
        (TestFMEA) __init__ should return instance of FMEA data controller
        """

        self.assertEqual(self.DUT.dicDFMEA, {})
        self.assertEqual(self.DUT.dicFFMEA, {})

    @attr(all=True, integration=True)
    def test_request_function_fmea(self):
        """
        (TestFMEA) request_fmea for a Function should return False on success
        """

        self.assertFalse(self.DUT.request_fmea(self._dao, None, 0))

    @attr(all=True, integration=True)
    def test_request_hardware_fmea(self):
        """
        (TestFMEA) request_fmea for a Hardware should return False on success
        """

        self.assertFalse(self.DUT.request_fmea(self._dao, 0))

    @attr(all=True, integration=True)
    def test_request_fmea_parent_problem(self):
        """
        (TestFMEA) __init__ raises ParentError for None, None or int, int input
        """

        self.assertRaises(ParentError, self.DUT.request_fmea, self._dao,
                          None, None)
        self.assertRaises(ParentError, self.DUT.request_fmea, self._dao, 2, 10)

    @attr(all=True, integration=True)
    def test_add_mode(self):
        """
        (TestFMEA) add_mode returns 0 on successful add
        """

        self.DUT.request_fmea(self._dao, 0)
        (_results, _error_code, _last_id) = self.DUT.add_mode(0)
        self.assertEqual(_error_code, 0)

        self.DUT.request_fmea(self._dao, None, 0)
        (_results, _error_code, _last_id) = self.DUT.add_mode(None, 0)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_delete_mode(self):
        """
        (TestFMEA) delete_mode returns 0 on successful delete
        """

        self.DUT.request_fmea(self._dao, None, 0)
        _n = len(self.DUT.dicFFMEA[0].dicModes)
        _n = self.DUT.dicFFMEA[0].dicModes.keys()[_n - 1]
        _mode_id = self.DUT.dicFFMEA[0].dicModes[_n].mode_id

        self.assertEqual(self.DUT.delete_mode(_mode_id, None, 0), (True, 0))

        self.DUT.request_fmea(self._dao, 0)
        _n = len(self.DUT.dicDFMEA[0].dicModes)
        _n = self.DUT.dicDFMEA[0].dicModes.keys()[_n - 1]
        _mode_id = self.DUT.dicDFMEA[0].dicModes[_n].mode_id

        self.assertEqual(self.DUT.delete_mode(_mode_id, 0), (True, 0))

    @attr(all=True, integration=True)
    def test_delete_non_existant_mode(self):
        """
        (TestFMEA) delete_mode returns 60 when trying to delete non-existant mode
        """

        self.DUT.request_fmea(self._dao, None, 0)
        _n = len(self.DUT.dicFFMEA[0].dicModes)
        try:
            _n = self.DUT.dicFFMEA[0].dicModes.keys()[_n - 1]
        except IndexError:
            return
        _mode_id = self.DUT.dicFFMEA[0].dicModes[_n].mode_id

        self.assertEqual(self.DUT.delete_mode(_mode_id + 1, None, 0),
                         (True, 60))

        self.DUT.request_fmea(self._dao, 0)
        _n = len(self.DUT.dicDFMEA[0].dicModes)
        _n = self.DUT.dicDFMEA[0].dicModes.keys()[_n - 1]
        _mode_id = self.DUT.dicDFMEA[0].dicModes[_n].mode_id

        self.assertEqual(self.DUT.delete_mode(_mode_id + 1, 0),
                         (True, 60))

    @attr(all=True, integration=True)
    def test_save_mode(self):
        """
        (TestFMEA) _save_mode
        """

        self.DUT.request_fmea(self._dao, None, 0)
        _n = len(self.DUT.dicFFMEA[0].dicModes)
        _n = self.DUT.dicFFMEA[0].dicModes.keys()[_n - 1]
        _mode = self.DUT.dicFFMEA[0].dicModes[_n]
        _values = (0, 0, 0, 'Test Mode', 'Mission', 'Mission Phase', 'Local',
                   'Next', 'End', 'Detection Method', 'Other Indications',
                   'Isolation Method', 'Design Provisions', 'Operator Actions',
                   'Severity Class', 'Hazard Rate Source', 'Mode Probability',
                   1.0, 0.0, 0.0, 0.0, 0.0, 10, 10, 0, 0, 'Remarks')
        _mode.set_attributes(_values)

        self.assertFalse(self.DUT._save_mode(_mode))
