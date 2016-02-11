#!/usr/bin/env python -O
"""
This is the test class for testing the Usage Profile module algorithms and
models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestProfile.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from usage.UsageProfile import Model, UsageProfile

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestUsageProfileModel(unittest.TestCase):
    """
    Class for testing the Usage Profile model class.
    """

    def setUp(self):

        self.DUT = Model(0)

    @attr(all=True, unit=True)
    def test_profile_create(self):
        """
        Method to test the creation of a Usage Profile class instance and
        default values for public attributes are correct.
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, 0)


class TestUsageProfileController(unittest.TestCase):
    """
    Class for testing the Usage Profile controller class.
    """

    def setUp(self):

        self.DUT = UsageProfile()

    @attr(all=True, unit=True)
    def test_create_controller(self):
        """
        Method to test the creation of a Usage Profile controller instance.
        """

        self.assertEqual(self.DUT.dicProfiles, {})
