#!/usr/bin/env python -O
"""
This is the test class for testing the Environment class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       TestEnvironment.py is part of The RTK Project
#
# All rights reserved.

import unittest

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from usage.Environment import Model


class TestEnvironmentModel(unittest.TestCase):
    """
    Class for testing the Environment model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Environment model class.
        """

        self.DUT = Model()

        self.good_values = (0, 0, 0, 0, 1, 'Test Environment', 'units',
                            0.0, 0.0, 0.0, 0.0)
        self.bad_values = (0, 0, 0, 0, 'units', 'Test Environment', 1, 50.0,
                           0.0, 0.0, 0.0)

    def test_environment_create(self):
        """
        Method to test the creation of an Environment class instance and
        default values for public attributes are correct.
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.mission_id, 0)
        self.assertEqual(self.DUT.phase_id, 0)
        self.assertEqual(self.DUT.test_id, 0)
        self.assertEqual(self.DUT.environment_id, 0)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.units, '')
        self.assertEqual(self.DUT.minimum, 0.0)
        self.assertEqual(self.DUT.maximum, 0.0)
        self.assertEqual(self.DUT.mean, 0.0)
        self.assertEqual(self.DUT.variance, 0.0)

    def test_set_attributes(self):
        """
        Test that Environment instance attributes can be set.
        """

        self.assertFalse(self.DUT.set_attributes(self.good_values))
        self.assertTrue(self.DUT.set_attributes(self.bad_values))

    def test_get_attributes(self):
        """
        Test that attributes can be retrieved.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0, 0, 0, 0, '', '', 0.0, 0.0, 0.0, 0.0))
