#!/usr/bin/env python -O
"""
This is the test class for testing the FMEA class.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.fmea.TestFMEA.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao

from analyses.fmea.FMEA import Model, FMEA, ParentError

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


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

        self.DUT = FMEA()

    @attr(all=True, unit=True)
    def test_create_controller(self):
        """
        (TestFMEA) __init__ should return instance of FMEA data controller
        """

        self.assertEqual(self.DUT.dicDFMEA, {})
        self.assertEqual(self.DUT.dicFFMEA, {})
