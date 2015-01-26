#!/usr/bin/env python -O
"""
This is the test class for testing Mission module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       TestMission.py is part of The RTK Project
#
# All rights reserved.

import unittest

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao

from usage.Mission import Model
from usage.Phase import Model as Phase


class TestMissionModel(unittest.TestCase):
    """
    Class for testing the Mission model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Mission class.
        """

        self.DUT = Model()

        self.good_values = (0, 1, 50.0, 'days', 'Test Mission')
        self.bad_values = (0, 'days', 'Test Mission', 1, 50.0)

    @attr(all=True, unit=True)
    def test_mission_create(self):
        """
        Method to test the creation of a Mission class instance and default
        values for public attributes are correct.
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.mission_id, 0)
        self.assertEqual(self.DUT.time, 0.0)
        self.assertEqual(self.DUT.time_units, '')
        self.assertEqual(self.DUT.description, '')

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        Test that attributes can be set.
        """

        self.assertFalse(self.DUT.set_attributes(self.good_values))
        self.assertTrue(self.DUT.set_attributes(self.bad_values))

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        Test that attributes can be retrieved.
        """

        self.assertEqual(self.DUT.get_attributes(), (0, 0.0, '', ''))
