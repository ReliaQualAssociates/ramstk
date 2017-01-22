#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestBoM.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing Hardware BoM module algorithms and models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.BoM import BoM

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestBoMController(unittest.TestCase):
    """
    Class for testing the BoM data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the BoM class.
        """

        self.DUT = BoM()

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestBoM) __init__ should create a BoM data controller
        """

        self.assertTrue(isinstance(self.DUT, BoM))
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicHardware, {})
        self.assertEqual(self.DUT.dao, None)
