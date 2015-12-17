#!/usr/bin/env python -O
"""
This is the test class for testing the Control class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.tests.fmea.TestControl.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao

from analyses.fmea.Control import Model


class TestControlModel(unittest.TestCase):
    """
    Class for testing the Control model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Control model class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_control_create(self):
        """
        (TestControl) __init__ should return instance of Control data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.mode_id, 0)
        self.assertEqual(self.DUT.mechanism_id, 0)
        self.assertEqual(self.DUT.cause_id, 0)
        self.assertEqual(self.DUT.control_id, 0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.control_type, 0)

    @attr(all=True, unit=True)
    def test_set_good_attributes(self):
        """
        (TestControl) set_attributes should return 0 with good inputs
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, 1, 2, 3, 'Test Control', 1))
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestControl) set_attributes should return 40 with missing input(s)
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, 1, 2))
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestControl) set_attributes should return 10 with wrong data type
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, 1, None, 'Test Cause'))
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_value(self):
        """
        (TestControl) set_attributes should return 10 with bad value
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, 1, 'Test Cause', 2))
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestControl) get_attributes should return good values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0, 0, 0, '', 0))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestControl) get_attributes(set_attributes(values)) == values
        """

        values = (4, 10, 246, 187, 'Test Cause', 1)

        self.DUT.set_attributes(values)
        result = self.DUT.get_attributes()
        self.assertEqual(result, values)
