#!/usr/bin/env python -O
"""
This is the test class for testing Allocation module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.allocation.TestAllocation.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

<<<<<<< HEAD
import dao.DAO as _dao
=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
from analyses.allocation.Allocation import Model, Allocation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestAllocationModel(unittest.TestCase):
    """
    Class for testing the Allocation data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Allocation class.
        """

<<<<<<< HEAD
        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestAllocation) __init__ should return a Allocation model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.hardware_id, None)
        self.assertEqual(self.DUT.reliability_goal, 1.0)
        self.assertEqual(self.DUT.hazard_rate_goal, 0.0)
        self.assertEqual(self.DUT.mtbf_goal, 0.0)
        self.assertEqual(self.DUT.included, 1)
        self.assertEqual(self.DUT.n_sub_systems, 1)
        self.assertEqual(self.DUT.n_sub_elements, 1)
        self.assertEqual(self.DUT.weight_factor, 1.0)
        self.assertEqual(self.DUT.percent_wt_factor, 1.0)
        self.assertEqual(self.DUT.int_factor, 1)
        self.assertEqual(self.DUT.soa_factor, 1)
        self.assertEqual(self.DUT.op_time_factor, 1)
        self.assertEqual(self.DUT.env_factor, 1)
        self.assertEqual(self.DUT.availability_alloc, 0.0)
        self.assertEqual(self.DUT.reliability_alloc, 0.0)
        self.assertEqual(self.DUT.hazard_rate_alloc, 0.0)
        self.assertEqual(self.DUT.mtbf_alloc, 0.0)
        self.assertEqual(self.DUT.parent_id, -1)
        self.assertEqual(self.DUT.method, 0)
        self.assertEqual(self.DUT.goal_measure, 0)
        self.assertEqual(self.DUT.duty_cycle, 100.0)
        self.assertEqual(self.DUT.hazard_rate, 0.0)
        self.assertEqual(self.DUT.mission_time, 10.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestAllocation) set_attributes should return a 0 error code on success
        """

        _values = (32, 0.95, 1, 0.005, 200.0, 2, 2, 8, 5, 9, 6, 0.8, 0.2,
                   0.975, 0.982, 0.05, 200.0, 0, 50.0, 0.005, 25.0, 1, 2)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_base_attributes_wrong_type(self):
        """
        (TestAllocation) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (32, 0.95, 1, 1, 2, 2, 8, 5, 9, 6, 0.8, 0.2, 0.975, None,
                   0.05, 200.0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestAllocation) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (32, 0.95, 1, 1, 2, 2, 8, 9, 6, 0.8, 0.2, 0.975, 0.982, 0.05,
                   200.0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestAllocation) get_attributes should return a tuple of attribute values
        """

        _values = (None, 1.0, 0.0, 0.0, 1, 1, 1, 1.0, 1.0, 1, 1, 1, 1,
                   0.0, 0.0, 0.0, 0.0, -1, 0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestAllocation) get_attributes(set_attributes(values)) == values
        """

        _values = (32, 0.95, 1, 0.005, 200.0, 2, 2, 8.0, 5.0, 9, 6, 8, 2,
                   0.975, 0.982, 0.05, 200.0, 0, 1, 2)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)

    def test_equal_apportionment(self):
        """
        (TestAllocation) equal_apportionment should return False on success
        """

        self.assertFalse(self.DUT.equal_apportionment(5, 0.95))

        self.assertAlmostEqual(self.DUT.reliability_alloc, 0.98979378)
        self.assertAlmostEqual(self.DUT.hazard_rate_alloc, 0.00102587)
        self.assertAlmostEqual(self.DUT.mtbf_alloc, 974.7862873)

    @attr(all=True, unit=True)
    def test_equal_apportionment_zero_children(self):
        """
        (TestAllocation) equal_apportionment should return True when there are zero children
        """

        self.assertTrue(self.DUT.equal_apportionment(0, 0.95))

    @attr(all=True, unit=True)
    def test_equal_apportionment_zero_goal(self):
        """
        (TestAllocation) equal_apportionment should return True when the reliability goal is zero
        """

        self.assertTrue(self.DUT.equal_apportionment(5, 0.0))

    @attr(all=True, unit=True)
    def test_equal_apportionment_zero_mission_time(self):
        """
        (TestAllocation) equal_apportionment should return True when the mission time is zero
        """

        self.DUT.mission_time = 0.0
        self.assertTrue(self.DUT.equal_apportionment(5, 0.95))

    @attr(all=True, unit=True)
    def test_agree_apportionment(self):
        """
        (TestAllocation) agree_apportionment should return False on success
        """

        self.assertFalse(self.DUT.agree_apportionment(5, 0.95))

        self.assertAlmostEqual(self.DUT.reliability_alloc, 0.98979378)
        self.assertAlmostEqual(self.DUT.hazard_rate_alloc, 0.00102587)
        self.assertAlmostEqual(self.DUT.mtbf_alloc, 974.78628731)

    @attr(all=True, unit=True)
    def test_agree_apportionment_zero_children(self):
        """
        (TestAllocation) agree_apportionment should return True when passed zero children
        """

        self.assertTrue(self.DUT.agree_apportionment(0, 0.95))

    @attr(all=True, unit=True)
    def test_agree_apportionment_zero_goal(self):
        """
        (TestAllocation) agree_apportionment should return True when passed a zero goal reliability
        """

        self.assertTrue(self.DUT.agree_apportionment(5, 0.0))

    @attr(all=True, unit=True)
    def test_agree_apportionment_zero_duty_cycle(self):
        """
        (TestAllocation) agree_apportionment should return True when the duty cycle is zero
        """

        self.DUT.duty_cycle = 0.0
        self.assertTrue(self.DUT.agree_apportionment(5, 0.0))

    @attr(all=True, unit=True)
    def test_agree_apportionment_zero_mission_time(self):
        """
        (TestAllocation) agree_apportionment should return True when the mission time is zero
        """

        self.DUT.mission_time = 0.0
        self.assertTrue(self.DUT.agree_apportionment(5, 0.0))

    @attr(all=True, unit=True)
    def test_arinc_apportionment(self):
        """
        (TestAllocation) arinc_apportionment should return False on success
        """

        self.DUT.hazard_rate = 0.0001
        self.assertFalse(self.DUT.arinc_apportionment(0.0005, 0.0004))

        self.assertAlmostEqual(self.DUT.reliability_alloc, 0.99920031)
        self.assertAlmostEqual(self.DUT.hazard_rate_alloc, 8E-05)
        self.assertAlmostEqual(self.DUT.mtbf_alloc, 12499.99999999)

    @attr(all=True, unit=True)
    def test_arinc_apportionment_zero_current_hr(self):
        """
        (TestAllocation) arinc_apportionment should return True when passed a zero current hazard rate
        """

        self.DUT.hazard_rate = 0.0
        self.assertTrue(self.DUT.arinc_apportionment(0.0005, 0.0004))

    @attr(all=True, unit=True)
    def test_arinc_apportionment_zero_system_hr(self):
        """
        (TestAllocation) arinc_apportionment should return True when passed a zero system hazard rate
        """

        self.DUT.hazard_rate = 0.0001
        self.assertTrue(self.DUT.arinc_apportionment(0.0, 0.0004))

    @attr(all=True, unit=True)
    def test_arinc_apportionment_zero_goal_hr(self):
        """
        (TestAllocation) arinc_apportionment should return True when passed a zero goal hazard rate
        """

        self.DUT.hazard_rate = 0.0001
        self.assertTrue(self.DUT.arinc_apportionment(0.0005, 0.0))

    @attr(all=True, unit=True)
    def test_arinc_apportionment_zero_mission_time(self):
        """
        (TestAllocation) arinc_apportionment should return False with a mission time of zero
        """

        self.DUT.hazard_rate = 0.0001
        self.DUT.mission_time = 0.0
        self.assertFalse(self.DUT.arinc_apportionment(0.0005, 0.0004))

    @attr(all=True, unit=True)
    def test_foo_apportionment(self):
        """
        (TestAllocation) foo_apportionment should return False on success
        """

        self.DUT.hazard_rate = 0.0001
        self.DUT.int_factor = 3
        self.DUT.soa_factor = 7
        self.DUT.op_time_factor = 10
        self.DUT.env_factor = 4
        self.assertFalse(self.DUT.foo_apportionment(5, 0.0004))

        self.assertAlmostEqual(self.DUT.reliability_alloc, 0.51068618)
        self.assertAlmostEqual(self.DUT.hazard_rate_alloc, 0.06720000)
        self.assertAlmostEqual(self.DUT.mtbf_alloc, 14.88095238)

    @attr(all=True, unit=True)
    def test_foo_apportionment_zero_cum_weight(self):
        """
        (TestAllocation) foo_apportionment should return True when the cumulative weight is zero
        """

        self.DUT.hazard_rate = 0.0001
        self.DUT.int_factor = 3
        self.DUT.soa_factor = 7
        self.DUT.op_time_factor = 10
        self.DUT.env_factor = 4
        self.assertTrue(self.DUT.foo_apportionment(0, 0.0004))

    @attr(all=True, unit=True)
    def test_foo_apportionment_zero_hazard_rate(self):
        """
        (TestAllocation) foo_apportionment should return True when the goal hazard rate is zero
        """

        self.DUT.hazard_rate = 0.0001
        self.DUT.int_factor = 3
        self.DUT.soa_factor = 7
        self.DUT.op_time_factor = 10
        self.DUT.env_factor = 4
        self.assertTrue(self.DUT.foo_apportionment(5, 0.0))

    @attr(all=True, unit=True)
    def test_foo_apportionment_zero_goal(self):
        """
        (TestAllocation) foo_apportionment should return True when the goal is zero
        """

        self.DUT.int_factor = 3
        self.DUT.soa_factor = 7
        self.DUT.op_time_factor = 10
        self.DUT.env_factor = 4
        self.assertTrue(self.DUT.foo_apportionment(5, 0.0))

    @attr(all=True, unit=True)
    def test_set_goals_rt_input(self):
        """
        (TestAllocation) _calculate_goals should return False on success passing reliability goal
        """

        self.DUT.mission_time = 10.0
        self.DUT.reliability_goal = 0.975
        self.DUT.goal_measure = 1

        self.assertFalse(self.DUT.calculate_goals())
        self.assertAlmostEqual(self.DUT.hazard_rate_goal, 0.00253178)
        self.assertAlmostEqual(self.DUT.mtbf_goal, 394.97890205)

    @attr(all=True, unit=True)
    def test_set_goals_rt_zero_input(self):
        """
        (TestAllocation) _calculate_goals should return True when passing reliability goal of zero
        """

        self.DUT.mission_time = 10.0
        self.DUT.reliability_goal = 0.0
        self.DUT.goal_measure = 1

        self.assertTrue(self.DUT.calculate_goals())

    @attr(all=True, unit=True)
    def test_set_goals_mtbf_input(self):
        """
        (TestAllocation) _calculate_goals should return False on success passing MTBF goal
        """

        self.DUT.mission_time = 10.0
        self.DUT.mtbf_goal = 400.0
        self.DUT.goal_measure = 3

        self.assertFalse(self.DUT.calculate_goals())
        self.assertAlmostEqual(self.DUT.reliability_goal, 0.9753099)
        self.assertAlmostEqual(self.DUT.hazard_rate_goal, 0.00250000)

    @attr(all=True, unit=True)
    def test_set_goals_mtbf_zero_input(self):
        """
        (TestAllocation) _calculate_goals should return True when passing MTBF goal of zero
        """

        self.DUT.mission_time = 10.0
        self.DUT.mtbf_goal = 0.0
        self.DUT.goal_measure = 3

        self.assertTrue(self.DUT.calculate_goals())

    @attr(all=True, unit=True)
    def test_set_goals_ht_input(self):
        """
        (TestAllocation) _calculate_goals should return False on success passing hazard rate goal
        """

        self.DUT.mission_time = 10.0
        self.DUT.hazard_rate_goal = 0.00015
        self.DUT.goal_measure = 2

        self.assertFalse(self.DUT.calculate_goals())
        self.assertAlmostEqual(self.DUT.reliability_goal, 0.99850112)
        self.assertAlmostEqual(self.DUT.mtbf_goal, 6666.66666666)

    @attr(all=True, unit=True)
<<<<<<< HEAD
    def test_set_goals_ht_input(self):
=======
    def test_set_goals_ht_input_zero(self):
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """
        (TestAllocation) _calculate_goals should return True when passing hazard rate goal of zero
        """

        self.DUT.mission_time = 10.0
        self.DUT.hazard_rate_goal = 0.0
        self.DUT.goal_measure = 2

        self.assertTrue(self.DUT.calculate_goals())


class TestAllocationController(unittest.TestCase):
    """
    Class for testing the Allocation data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Allocation class.
        """

<<<<<<< HEAD
        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = Allocation()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestAllocation) __init__ should create an Allocation data controller
        """

        self.assertTrue(isinstance(self.DUT, Allocation))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT.dicAllocation, {})
<<<<<<< HEAD

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
