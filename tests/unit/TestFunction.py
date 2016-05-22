#!/usr/bin/env python -O
"""
This is the test class for testing Function module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestFunction.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from function.Function import Model, Function   # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestFunctionModel(unittest.TestCase):
    """
    Class for testing the Function model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Function class.
        """

        self.DUT = Model()

        self._reliability_inputs = (0.005013, 0.004013)
        self._availability_inputs = (1.5, 2.25, 3.18, 2.16)
        self._cost_inputs = (118.92)
        self._mission_time = 10.0

    @attr(all=True, unit=True)
    def test01_function_create(self):
        """
        (TestFunction) Test the creation of a Function class instance and check default values
        for public attributes are correct.
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.function_id, 0)
        self.assertEqual(self.DUT.availability, 1.0)
        self.assertEqual(self.DUT.mission_availability, 1.0)
        self.assertEqual(self.DUT.code, '')
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.mission_hazard_rate, 0.0)
        self.assertEqual(self.DUT.hazard_rate, 0.0)
        self.assertEqual(self.DUT.mmt, 0.0)
        self.assertEqual(self.DUT.mcmt, 0.0)
        self.assertEqual(self.DUT.mpmt, 0.0)
        self.assertEqual(self.DUT.mission_mtbf, 0.0)
        self.assertEqual(self.DUT.mtbf, 0.0)
        self.assertEqual(self.DUT.mttr, 0.0)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.n_modes, 0)
        self.assertEqual(self.DUT.n_parts, 0)
        self.assertEqual(self.DUT.type, 0)
        self.assertEqual(self.DUT.parent_id, -1)
        self.assertEqual(self.DUT.level, 0)
        self.assertEqual(self.DUT.safety_critical, 1)

    @attr(all=True, unit=True)
    def test02_function_set_attributes(self):
        """
        (TestFunction) set_attributes should return a 0 error code on success
        """

        _values = (0, 0, 1.0, 1.0, 'New Code', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 'New Name', 'New Remarks', 0, 0, 0, 4, 0, 1)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test02a_function_set_attributes_missing_index(self):
        """
        (TestFunction) set_attributes should return a 40 error code passed a wrong data type
        """

        _values = (0, 0, 1.0, 1.0, 'New Code', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 'New Name', 'New Remarks', 0, 0, 0, 4, 0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test02b_function_set_attributes_wrong_type(self):
        """
        (TestFunction) set_attributes should return a 10 error code when too few items are passed
        """

        _values = (0, 0, 1.0, 1.0, 'New Code', 0.0, 0.0, 0.0, 0.0, None, 0.0,
                   0.0, 0.0, 0.0, 'New Name', 'New Remarks', 0, 0, 0, 4, 0, 1)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test03_function_get_attributes(self):
        """
        (TestFunction) the creation of a Function class instance and check default values
        for public attributes are correct.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0, 1.0, 1.0, '', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, '', '', 0, 0, 0, -1, 0, 1))

    @attr(all=True, unit=True)
    def test04_calculate_reliability(self):
        """
        (TestFunction) Test of Revision reliability calculations.
        """

        # Check that everything is OK with good inputs.
        (_error_code,
         _error_msg) = self.DUT.calculate_reliability(self._reliability_inputs)
        self.assertEqual(_error_code, 0)
        self.assertAlmostEqual(self.DUT.hazard_rate, 0.005013)
        self.assertAlmostEqual(self.DUT.mission_hazard_rate, 0.004013)
        self.assertAlmostEqual(self.DUT.mtbf, 199.4813485)
        self.assertAlmostEqual(self.DUT.mission_mtbf, 249.1901321)

        # Check the TypeError conditions.
        self._reliability_inputs = (None, 0.004013)
        (_error_code,
         _error_msg) = self.DUT.calculate_reliability(self._reliability_inputs)
        self.assertEqual(_error_code, 10)

        self._reliability_inputs = (0.005013, None)
        (_error_code,
         _error_msg) = self.DUT.calculate_reliability(self._reliability_inputs)
        self.assertEqual(_error_code, 10)

        # Check the ZeroDivisionError conditions.
        self._reliability_inputs = (0.0, 0.004013)
        (_error_code,
         _error_msg) = self.DUT.calculate_reliability(self._reliability_inputs)
        self.assertEqual(_error_code, 20)

        self._reliability_inputs = (0.005013, 0.0)
        (_error_code,
         _error_msg) = self.DUT.calculate_reliability(self._reliability_inputs)
        self.assertEqual(_error_code, 20)

    @attr(all=True, unit=True)
    def test05_calculate_availability(self):
        """
        (TestFunction) Test of Revision availability calculations.
        """

        self.DUT.mtbf = 199.4813485
        self.DUT.mission_mtbf = 249.1901321

        # Check that everything is OK with good inputs.
        (_error_code,
         _error_msg) = self.DUT.calculate_availability((1.5, 2.25, 3.18, 2.16))
        self.assertEqual(_error_code, 0)
        self.assertAlmostEqual(self.DUT.availability, 0.9843088)
        self.assertAlmostEqual(self.DUT.mission_availability, 0.9873995)

        # Check the TypeError conditions.
        (_error_code,
         _error_msg) = self.DUT.calculate_availability((None, 2.25, 3.18, 2.16))
        self.assertEqual(_error_code, 10)

        (_error_code,
         _error_msg) = self.DUT.calculate_availability((1.5, None, 3.18, 2.16))
        self.assertEqual(_error_code, 10)

        (_error_code,
         _error_msg) = self.DUT.calculate_availability((1.5, 2.25, None, 2.16))
        self.assertEqual(_error_code, 10)

        (_error_code,
         _error_msg) = self.DUT.calculate_availability((1.5, 2.25, 3.18, None))
        self.assertEqual(_error_code, 10)

        # Check the ZeroDivisionError conditions.
        self.DUT.mtbf = 0.0

        (_error_code,
         _error_msg) = self.DUT.calculate_availability((1.5, 2.25, 0.0, 2.16))
        self.assertEqual(_error_code, 20)

        self.DUT.mtbf = 199.4813485
        self.DUT.mission_mtbf = 0.0

        (_error_code,
         _error_msg) = self.DUT.calculate_availability((1.5, 2.25, 0.0, 2.16))
        self.assertEqual(_error_code, 20)

    @attr(all=True, unit=True)
    def test06_calculate_costs(self):
        """
        (TestFunction) Test of Revision cost calculations.
        """

        self.DUT.hazard_rate = 0.005013

        (_error_code,
         _error_msg) = self.DUT.calculate_costs(self._cost_inputs,
                                                self._mission_time)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.cost, 118.92)
        #self.assertAlmostEqual(self.DUT.cost_per_failure, 0.5013)
        #self.assertAlmostEqual(self.DUT.cost_per_hour, 10.0)

        # Check TypeError conditions.
        (_error_code,
         _error_msg) = self.DUT.calculate_costs(None,
                                                self._mission_time)
        self.assertEqual(_error_code, 10)

        # Check ZeroDivisionError conditions.
        (_error_code,
         _error_msg) = self.DUT.calculate_costs(self._cost_inputs,
                                                0.0)
        self.assertEqual(_error_code, 20)


class TestFunctionController(unittest.TestCase):
    """
    Class for testing the Function data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Function class.
        """

        self.DUT = Function()

    @attr(all=True, unit=True)
    def test01_controller_create(self):
        """
        (TestFunction) Test that Function data controller was created.
        """

        self.assertTrue(isinstance(self.DUT, Function))
        self.assertEqual(self.DUT._dao, None)       # pylint: disable=W0212
        self.assertEqual(self.DUT._last_id, None)   # pylint: disable=W0212
        self.assertEqual(self.DUT.dicFunctions, {})
