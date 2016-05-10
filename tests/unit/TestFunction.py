#!/usr/bin/env python -O
"""
This is the test class for testing Function module algorithms and models.
"""

<<<<<<< HEAD
__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       TestFunction.py is part of The RTK Project
#
# All rights reserved.
=======
# -*- coding: utf-8 -*-
#
#       tests.unit.TestFunction.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

import unittest
from nose.plugins.attrib import attr

<<<<<<< HEAD
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from function.Function import Model, Function
=======
from function.Function import Model, Function   # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e


class TestFunctionModel(unittest.TestCase):
    """
    Class for testing the Function model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Function class.
        """

<<<<<<< HEAD
        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = Model()

        self._reliability_inputs = (0.005013, 0.004013)
        self._availability_inputs = (1.5, 2.25, 3.18, 2.16)
        self._cost_inputs = (118.92)
        self._mission_time = 10.0

    @attr(all=True, unit=True)
    def test_function_create(self):
        """
        Test the creation of a Function class instance and check default values
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
    def test_function_set_attributes(self):
        """
        (TestRequirement) set_attributes should return a 0 error code on success
        """

        _values = (0, 0, 1.0, 1.0, 'New Code', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 'New Name', 'New Remarks', 0, 0, 0, 4, 0, 1)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_function_set_attributes_missing_index(self):
        """
        (TestRequirement) set_attributes should return a 40 error code passed a wrong data type
        """

        _values = (0, 0, 1.0, 1.0, 'New Code', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 'New Name', 'New Remarks', 0, 0, 0, 4, 0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_function_set_attributes_wrong_type(self):
        """
        (TestRequirement) set_attributes should return a 10 error code when too few items are passed
        """

        _values = (0, 0, 1.0, 1.0, 'New Code', 0.0, 0.0, 0.0, 0.0, None, 0.0,
                   0.0, 0.0, 0.0, 'New Name', 'New Remarks', 0, 0, 0, 4, 0, 1)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_function_get_attributes(self):
        """
        Test the creation of a Function class instance and check default values
        for public attributes are correct.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0, 1.0, 1.0, '', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, '', '', 0, 0, 0, -1, 0, 1))

    @attr(all=True, unit=True)
    def test_calculate_reliability(self):
        """
        Test of Revision reliability calculations.
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
    def test_calculate_availability(self):
        """
        Test of Revision availability calculations.
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
    def test_calculate_costs(self):
        """
        Test of Revision cost calculations.
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

<<<<<<< HEAD
        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = Function()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        Test that Function data controller was created.
        """

        self.assertTrue(isinstance(self.DUT, Function))
<<<<<<< HEAD
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicFunctions, {})

    @attr(all=True, integration=True)
    def test_request_functions(self):
        """
        (TestFunction) request_functions should return 0 on success
        """

        self.assertEqual(self.DUT.request_functions(self._dao)[1], 0)
# TODO: Test that method fails when no Functions exist in database.
    @attr(all=True, integration=True)
    def test_add_function(self):
        """
        (TestFunction) add_function returns 0 on success and new Function data model added to dictionary
        """

        self.assertEqual(self.DUT.request_functions(self._dao)[1], 0)
        (_results,
         _error_code) = self.DUT.add_function(0, 0, 'F-T', 'Test Function',
                                              'This is a test function')

        self.assertTrue(isinstance(self.DUT.dicFunctions[self.DUT._last_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_add_function_no_parent(self):
        """
        (TestFunction) add_function uses default parent ID when none is passed
        """

        self.assertEqual(self.DUT.request_functions(self._dao)[1], 0)
        (_results,
         _error_code) = self.DUT.add_function(0, None, 'F-T', 'New Function',
                                              'This is a test function')
        self.assertEqual(self.DUT.dicFunctions[self.DUT._last_id].parent_id,
                         -1)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_add_function_no_code(self):
        """
        (TestFunction) add_function uses default code when none is passed
        """
# TODO: This test requires the configuration values to be set.
        #self.assertEqual(self.DUT.request_functions(self._dao)[1], 0)
        #(_results,
        # _error_code) = self.DUT.add_function(0, 0, None, 'New Function',
        #                                      'This is a test function')
        #self.assertEqual(self.DUT.dicFunctions[self.DUT._last_id].name,
        #                 'New Function')
        #self.assertTrue(_results)
        #self.assertEqual(_error_code, 0)

        pass

    @attr(all=True, integration=True)
    def test_add_function_no_name(self):
        """
        (TestFunction) add_function uses default name when none is passed
        """

        self.assertEqual(self.DUT.request_functions(self._dao)[1], 0)
        (_results,
         _error_code) = self.DUT.add_function(0, 0, 'F-T', None,
                                              'This is a test function')
        self.assertEqual(self.DUT.dicFunctions[self.DUT._last_id].name,
                         'New Function')
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_add_function_no_remarks(self):
        """
        (TestFunction) add_function uses default remarks when none is passed
        """

        self.assertEqual(self.DUT.request_functions(self._dao)[1], 0)
        (_results,
         _error_code) = self.DUT.add_function(0, 0, 'F-T', 'New Function',
                                              '')
        self.assertEqual(self.DUT.dicFunctions[self.DUT._last_id].remarks,
                         '')
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_delete_function(self):
        """
        Test the ability to delete a function from the RTK Project database.
        """

        self.assertEqual(self.DUT.request_functions(self._dao)[1], 0)
        (_results,
         _error_code) = self.DUT.delete_function(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_function(self):
        """
        Test the ability to save a function to the RTK Project database.
        """

        self.DUT.request_functions(self._dao)
        (_results,
         _error_code) = self.DUT.save_function(0)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_all_functions(self):
        """
        Test the ability to save all functions to the RTK Project database.
        """

        self.DUT.request_functions(self._dao)
        self.assertFalse(self.DUT.save_all_functions())
=======
        self.assertEqual(self.DUT._dao, None)       # pylint: disable=W0212
        self.assertEqual(self.DUT._last_id, None)   # pylint: disable=W0212
        self.assertEqual(self.DUT.dicFunctions, {})
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
