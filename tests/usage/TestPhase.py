#!/usr/bin/env python -O
"""
This is the test class for testing the Phase class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       TestPhase.py is part of The RTK Project
#
# All rights reserved.

import unittest

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao

from usage.Phase import Model
from usage.Environment import Model as Environment


class TestPhaseModel(unittest.TestCase):
    """
    Class for testing the Phase model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Phase model class.
        """

        self.DUT = Model()

        self.good_values = (0, 1, 1, 0.0, 50.0, 'TP1', 'Test Phase')
        self.bad_values = (0, 1, 'TP1', 'Test Mission', 1, 0.0, 50.0)

    def test_phase_create(self):
        """
        Method to test the creation of a Phase class instance and default
        values for public attributes are correct.
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.mission_id, 0)
        self.assertEqual(self.DUT.phase_id, 0)
        self.assertEqual(self.DUT.start_time, 0.0)
        self.assertEqual(self.DUT.end_time, 0.0)
        self.assertEqual(self.DUT.code, '')
        self.assertEqual(self.DUT.description, '')

    def test_set_attributes(self):
        """
        Test that attributes can be set.
        """

        self.assertFalse(self.DUT.set_attributes(self.good_values))
        self.assertTrue(self.DUT.set_attributes(self.bad_values))

    def test_get_attributes(self):
        """
        Test that attributes can be retrieved.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0, 0, 0.0, 0.0, '', ''))
