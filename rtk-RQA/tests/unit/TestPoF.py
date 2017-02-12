#!/usr/bin/env python -O
"""
This is the test class for testing the Physics of Failure (PoF) class.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestPoF.py is part of The RTK Project

#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from analyses.pof.PhysicsOfFailure import Model, PoF, ParentError


__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestPoFModel(unittest.TestCase):
    """
    Class for testing the Physics of Failure model class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the PoF model class.
        """

        self.DUT = Model(0)

    @attr(all=True, unit=True)
    def test_pof_create(self):

        """
        (TestPoF) __init__ should return instance of PoF data model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT.dicMechanisms, {})
        self.assertEqual(self.DUT.assembly_id, 0)

    @attr(all=True, unit=True)
    def test_pof_create_parent_problem(self):

        """
        (TestPoF) __init__ raises ParentError for None input
        """

        self.assertRaises(ParentError, Model, None)


class TestPoFController(unittest.TestCase):
    """
    Class for testing the PoF data controller class.
    """

    def setUp(self):

        self.DUT = PoF()

    @attr(all=True, unit=True)
    def test_create_controller(self):
        """
        (TestPoF) __init__ should return instance of PoF data controller
        """

        self.assertEqual(self.DUT.dicPoF, {})
