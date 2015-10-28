#!/usr/bin/env python -O
"""
This is the test class for testing Growth Testing module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.testing.TestGrowth.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr
import numpy as np

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from testing.growth.Growth import Model, Growth


class TestGrowthModel(unittest.TestCase):
    """
    Class for testing the Reliability Growth data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Reliability Growth class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestGrowth) __init__ should return a Reliability Growth model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.lst_p_growth_rate, [0.0])
        self.assertEqual(self.DUT.lst_p_ms, [0.0])
        self.assertEqual(self.DUT.lst_p_fef, [0.0])
        self.assertEqual(self.DUT.lst_p_prob, [0.0])
        self.assertEqual(self.DUT.lst_p_mtbfi, [0.0])
        self.assertEqual(self.DUT.lst_p_mtbff, [0.0])
        self.assertEqual(self.DUT.lst_p_mtbfa, [0.0])
        self.assertEqual(self.DUT.lst_p_test_time, [0.0])
        self.assertEqual(self.DUT.lst_p_n_failures, [0.0])
        self.assertEqual(self.DUT.lst_p_start_date, [0.0])
        self.assertEqual(self.DUT.lst_p_end_date, [0.0])
        self.assertEqual(self.DUT.lst_p_weeks, [0.0])
        self.assertEqual(self.DUT.lst_p_n_test_units, [0.0])
        self.assertEqual(self.DUT.lst_p_tpu, [0.0])
        self.assertEqual(self.DUT.lst_p_tpupw, [0.0])
        self.assertEqual(self.DUT.lst_o_growth_rate, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.lst_o_ms, [0.0])
        self.assertEqual(self.DUT.lst_o_fef, [0.0])
        self.assertEqual(self.DUT.lst_o_mtbfi, [0.0])
        self.assertEqual(self.DUT.lst_o_mtbff, [0.0])
        self.assertEqual(self.DUT.lst_o_mtbfa, [0.0])
        self.assertEqual(self.DUT.lst_o_test_time, [0.0])
        self.assertEqual(self.DUT.alpha_hat, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.beta_hat, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.cum_mean, [[0.0, 0.0, 0.0]])
        self.assertEqual(self.DUT.instantaneous_mean, [[0.0, 0.0, 0.0]])

        self.assertEqual(self.DUT.rg_plan_model, 0)
        self.assertEqual(self.DUT.rg_assess_model, 0)
        self.assertEqual(self.DUT.tr, 0.0)
        self.assertEqual(self.DUT.mtbfg, 0.0)
        self.assertEqual(self.DUT.mtbfgp, 0.0)
        self.assertEqual(self.DUT.n_phases, 1)
        self.assertEqual(self.DUT.ttt, 0.0)
        self.assertEqual(self.DUT.avg_growth, 0.0)
        self.assertEqual(self.DUT.avg_ms, 0.75)
        self.assertEqual(self.DUT.avg_fef, 0.7)
        self.assertEqual(self.DUT.probability, 0.75)
        self.assertEqual(self.DUT.ttff, 0.0)
        self.assertEqual(self.DUT.grouped, 0)
        self.assertEqual(self.DUT.group_interval, 0.0)
        self.assertEqual(self.DUT.se_scale, 0.0)
        self.assertEqual(self.DUT.se_shape, 0.0)
        self.assertEqual(self.DUT.se_cum_mean, 0.0)
        self.assertEqual(self.DUT.se_inst_mean, 0.0)
        self.assertEqual(self.DUT.cramer_vonmises, 0.0)
        self.assertEqual(self.DUT.chi_square, 0.0)

        self.assertEqual(self.DUT.cvm_critical_value, 0.0)
        self.assertEqual(self.DUT.chi2_critical_value, [0.0, 0.0])

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestGrowth) set_attributes should return a 0 error code on success
        """

        _values = (0, 0, 1, 'Testing', 'Description', 2, 'Attachment', 40.2,
                   2.0, 0.6, 0.8, 0.9, 0, 0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.75,
                   0.7, 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestGrowth) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 0, 1, 'Testing', 'Description', 2, 'Attachment', 40.2,
                   2.0, 0.6, 0.8, 0.9, 0, 0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.75,
                   0.7, 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, None, 0.0, 0.0, 0.0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestGrowth) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 0, 1, 'Testing', 'Description', 2, 'Attachment', 40.2,
                   2.0, 0.6, 0.8, 0.9, 0, 0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.7,
                   0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_phase_attributes(self):
        """
        (TestGrowth) set_phase_attributes should return a 0 error code on success
        """

        _values = (1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 719163,
                   719163, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   6.0, 7.0, 8.0, 9.0, 10.0, 11.0)
        (_error_code,
         _error_msg) = self.DUT.set_phase_attributes(_values, 0)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_phase_attributes_wrong_type(self):
        """
        (TestGrowth) set_phase_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 719163,
                   719163, 0.0, 0, 0.0, 0.0, None, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0, 0.0)
        (_error_code,
         _error_msg) = self.DUT.set_phase_attributes(_values, 0)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_phase_attributes_missing_index(self):
        """
        (TestGrowth) set_phase_attributes should return a 40 error code when too few items are passed
        """

        _values = (1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 719163,
                   719163, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        (_error_code,
         _error_msg) = self.DUT.set_phase_attributes(_values, 0)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestGrowth) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (None, None, 0, '', '', 0, '', 0.0, 0, 0.75, 0.0,
                          0.0, 0, 0, 0.0, 0.0, 0, 1, 0.0, 0.0, 0.75, 0.7,
                          0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0))

    @attr(all=True, unit=True)
    def test_get_phase_attributes(self):
        """
        (TestGrowth) get_phase_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_phase_attributes(),
                         ([0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0],
                          [0.0], [0], [0], [0], [0.0], [0.0], [0.0], [0.0],
                          [0.0, 0.0, 0.0], [0.0], [0.0], [0.0], [0.0], [0.0],
                          [0.0], [[0.0, 0.0, 0.0]], [[0.0, 0.0, 0.0]]))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestGrowth) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 0, 1, 'Testing', 'Description', 2, 'Attachment', 40.2,
                   2.0, 0.6, 0.8, 0.9, 0, 0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.75,
                   0.7, 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1.0, 2.0, 3.0, 4.0, 5.0)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)

    @attr(all=True, unit=True)
    def test_calculate_initial_mtbf_program(self):
        """
        (TestGrowth) calculate_initial_mtbf should return False when calculating the planned initial MTBF for the overall program
        """

        self.DUT.lst_p_mtbfi = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [0.0, 0.0, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.n_phases = 5

        self.assertFalse(self.DUT.calculate_initial_mtbf())
        self.assertAlmostEqual(self.DUT.lst_p_mtbfi[0], 35.8)

    @attr(all=True, unit=True)
    def test_calculate_initial_mtbf_phase(self):
        """
        (TestGrowth) calculate_initial_mtbf should return False when calculating initial MTBF for a test phase
        """

        self.DUT.lst_p_mtbfi = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [47.7333333, 0.0, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.n_phases = 5

        self.assertFalse(self.DUT.calculate_initial_mtbf(0))
        self.assertAlmostEqual(self.DUT.lst_p_mtbfi[0], 35.8000000)

    @attr(all=True, unit=True)
    def test_calculate_initial_mtbf_phase_zero_division(self):
        """
        (TestGrowth) calculate_initial_mtbf should return True when a zero division error occurs when calculting initial MTBF for a test phase
        """

        self.DUT.lst_p_mtbfi = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [47.7333333, 0.0, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_test_time = [0.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.n_phases = 5

        self.assertTrue(self.DUT.calculate_initial_mtbf())
        self.assertEqual(self.DUT.lst_p_mtbfi[0], 0.0)

    @attr(all=True, unit=True)
    def test_calculate_final_mtbf_program(self):
        """
        (TestGrowth) calculate_final_mtbf should return False when calculating the final MTBF for the overall program
        """

        self.DUT.lst_p_mtbfi = [35.8, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.n_phases = 5

        self.assertFalse(self.DUT.calculate_final_mtbf())
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[4], 78.9573023)

    @attr(all=True, unit=True)
    def test_calculate_final_mtbf_program_zero_division(self):
        """
        (TestGrowth) calculate_final_mtbf should return True when a zero division error occurs when calculting final MTBF for a test program
        """

        self.DUT.lst_p_mtbfi = [35.8, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [0.0, 0.0, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_test_time = [0.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.n_phases = 5

        self.assertTrue(self.DUT.calculate_final_mtbf())
        self.assertEqual(self.DUT.lst_p_mtbff[4], 0.0)

    @attr(all=True, unit=True)
    def test_calculate_final_mtbf_phase(self):
        """
        (TestGrowth) _calculate_final_mtbf should return False when calculating the final MTBF for a test phase
        """

        self.DUT.lst_p_mtbfi = [35.8, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [0.0, 0.0, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.n_phases = 5

        self.assertFalse(self.DUT.calculate_final_mtbf(0))
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[0], 46.4935065)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfi[1], 46.4935065)
        self.assertFalse(self.DUT.calculate_final_mtbf(1))
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[1], 57.4008738)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfi[2], 57.4008738)
        self.assertFalse(self.DUT.calculate_final_mtbf(2))
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[2], 67.3217509)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfi[3], 67.3217509)
        self.assertFalse(self.DUT.calculate_final_mtbf(3))
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[3], 72.7385854)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfi[4], 72.7385854)
        self.assertFalse(self.DUT.calculate_final_mtbf(4))
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[4], 78.9573023)

    @attr(all=True, unit=True)
    def test_calculate_final_mtbf_phase_zero_division(self):
        """
        (TestGrowth) calculate_final_mtbf should return True when a zero division error occurs when calculting final MTBF for a test phase
        """

        self.DUT.lst_p_mtbfi = [35.8, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [0.0, 0.0, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_test_time = [0.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.n_phases = 5

        self.assertTrue(self.DUT.calculate_final_mtbf())
        self.assertEqual(self.DUT.lst_p_mtbff[0], 0.0)

    @attr(all=True, unit=True)
    def test_calculate_average_mtbf(self):
        """
        (TestGrowth) calculate_average_mtbf should return False
        """

        self.DUT.lst_p_mtbfi = [35.8, 46.4935065, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [46.4935065, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]
        self.DUT.lst_p_n_failures = [27.9329609, 0, 0, 0]
        self.DUT.lst_p_mtbfa = [35.8, 0.0, 0.0, 0.0]

        self.assertFalse(self.DUT.calculate_average_mtbf(1))
        self.assertAlmostEqual(self.DUT.lst_p_n_failures[1], 28.6298235)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfa[1], 52.3929182)

    @attr(all=True, unit=True)
    def test_calculate_total_time_program(self):
        """
        (TestGrowth) calculate_total_time should return False when calculating the total test time for the overall test program
        """

        self.DUT.lst_p_mtbfi = [35.8, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [0.0, 0.0, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.assertFalse(self.DUT.calculate_total_time())
        self.assertAlmostEqual(self.DUT.ttt, 10000.000009203484)

    @attr(all=True, unit=True)
    def test_calculate_total_time_same_mtbf(self):
        """
        (TestGrowth) calculate_total_time should return False when the final MTBF and initial MTBF are the same
        """

        self.DUT.lst_p_mtbfi = [35.8, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [0.0, 0.0, 0.0, 0.0, 35.8]

        self.assertFalse(self.DUT.calculate_total_time())
        self.assertAlmostEqual(self.DUT.ttt, 0.0)

    @attr(all=True, unit=True)
    def test_calculate_total_time_phase(self):
        """
        (TestGrowth) calculate_total_time should return False when calculating the test time required for a single phase
        """

        self.DUT.lst_p_mtbfi = [35.8, 46.4935065, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [46.4935065, 57.4008738, 0.0, 0.0, 0.0]
        self.DUT.lst_p_test_time = [1000.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]
        self.DUT.lst_p_n_failures = [27.9329609, 15.6203831, 0, 0]
        self.DUT.lst_p_mtbfa = [35.8, 57.4008738, 0.0, 0.0]

        self.assertFalse(self.DUT.calculate_total_time(1))
        self.assertAlmostEqual(self.DUT.lst_p_test_time[1], 1500.0000036)

    @attr(all=True, unit=True)
    def test_calculate_growth_rate_program(self):
        """
        (TestGrowth) calculate_growth_rate should return False when calculating the average growth rate for the overall program
        """

        self.DUT.lst_p_mtbfi = [35.8, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [0.0, 0.0, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]

        self.assertFalse(self.DUT.calculate_growth_rate())
        self.assertAlmostEqual(self.DUT.avg_growth, 0.231391)

    @attr(all=True, unit=True)
    def test_calculate_growth_rate_phase(self):
        """
        (TestGrowth) calculate_growth_rate should return False when calculating the average growth rate for a test phase
        """

        self.DUT.lst_p_mtbfi = [35.8, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [46.4935065, 0.0, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.assertFalse(self.DUT.calculate_growth_rate(0))
        self.assertAlmostEqual(self.DUT.lst_p_growth_rate[0], 0.2339893)

    @attr(all=True, unit=True)
    def test_calculate_minimum_first_phase_time(self):
        """
        (TestGrowth) calculate_minimum_first_phase_time should return False
        """

        self.DUT.lst_p_mtbfi = [35.8, 46.4935065, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [46.4935065, 57.4008738, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_test_time = [1000.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]
        self.DUT.lst_p_n_failures = [27.9329609, 15.6203831, 0, 0]
        self.DUT.lst_p_mtbfa = [35.8, 57.4008738, 0.0, 0.0]

        self.DUT.ttt = 10000.0
        self.DUT.avg_growth = 0.23

        self.assertFalse(self.DUT.calculate_minimum_first_phase_time())
        self.assertAlmostEqual(self.DUT.lst_p_test_time[0], 999.9999991)

    @attr(all=True, unit=True)
    def test_calculate_minimum_first_phase_time_zero_division(self):
        """
        (TestGrowth) _calculate_minimum_first_phase_time should return True when there is a zero division error
        """

        self.DUT.lst_p_mtbfi = [0.0, 46.4935065, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [46.4935065, 57.4008738, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_test_time = [1000.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]
        self.DUT.lst_p_n_failures = [27.9329609, 15.6203831, 0, 0]
        self.DUT.lst_p_mtbfa = [35.8, 57.4008738, 0.0, 0.0]

        self.assertTrue(self.DUT.calculate_minimum_first_phase_time())
        self.assertAlmostEqual(self.DUT.lst_p_test_time[0], 0.0)

    @attr(all=True, unit=True)
    def test_calculate_management_strategy_program(self):
        """
        (TestGrowth) calculate_management_strategy should return False when calculating the average management strategy for the overall program
        """

        self.DUT.lst_p_mtbfi = [35.8, 46.4935065, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [46.4935065, 57.4008738, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_test_time = [1000.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]
        self.DUT.lst_p_n_failures = [27.9329609, 15.6203831, 0, 0]
        self.DUT.lst_p_mtbfa = [35.8, 57.4008738, 0.0, 0.0]

        self.DUT.mtbfgp = 86.26506
        self.DUT.avg_fef = 0.65

        self.assertFalse(self.DUT.calculate_management_strategy())
        self.assertAlmostEqual(self.DUT.avg_ms, 0.9)

    @attr(all=True, unit=True)
    def test_calculate_management_strategy_phase(self):
        """
        (TestGrowth) calculate_management_strategy should return False when calculating the average management strategy for a test phase
        """

        self.DUT.lst_p_mtbfi = [35.8, 46.4935065, 0.0, 0.0, 0.0]
        self.DUT.lst_p_fef = [0.65, 0.7, 0.6, 0.65, 0.55]
        self.DUT.lst_p_ms = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.DUT.mtbfgp = 86.26506

        self.assertFalse(self.DUT.calculate_management_strategy(1))
        self.assertAlmostEqual(self.DUT.lst_p_ms[1], 0.6586271)

    @attr(all=True, unit=True)
    def test_calculate_management_strategy_program_zero_division(self):
        """
        (TestGrowth) calculate_management_strategy should return True when there is a zero division error when calculating the average management strategy for the overall program
        """

        self.DUT.lst_p_mtbfi = [35.8, 46.4935065, 0.0, 0.0, 0.0]

        self.DUT.mtbfgp = 86.26506
        self.DUT.avg_fef = 0.0

        self.assertTrue(self.DUT.calculate_management_strategy())
        self.assertAlmostEqual(self.DUT.avg_ms, 100.0)

    @attr(all=True, unit=True)
    def test_calculate_management_strategy_phase_zero_division(self):
        """
        (TestGrowth) calculate_management_strategy should return True when there is a zero division error when calculating the average management strategy for a test phase
        """

        self.DUT.lst_p_mtbfi = [35.8, 46.4935065, 0.0, 0.0, 0.0]
        self.DUT.lst_p_fef = [0.65, 0.0, 0.6, 0.65, 0.55]
        self.DUT.lst_p_ms = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.DUT.mtbfgp = 0.0

        self.assertTrue(self.DUT.calculate_management_strategy(1))
        self.assertAlmostEqual(self.DUT.lst_p_ms[1], 100.0)

    @attr(all=True, unit=True)
    def test_calculate_probability(self):
        """
        (TestGrowth) calculate_probability should return False
        """

        self.DUT.lst_p_mtbfi = [35.8, 46.4935065, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [46.4935065, 57.4008738, 0.0, 0.0, 78.9573023]
        self.DUT.lst_p_mtbfa = [35.8, 57.4008738, 0.0, 0.0]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]
        self.DUT.lst_p_n_failures = [27.9329609, 15.6203831, 0, 0]
        self.DUT.lst_p_fef = [0.65, 0.7, 0.6, 0.65, 0.55]
        self.DUT.lst_p_ms = [0.9, 0.6586271, 0.0, 0.0, 0.0]
        self.DUT.lst_p_prob = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.assertFalse(self.DUT.calculate_probability(0))
        self.assertAlmostEqual(self.DUT.lst_p_prob[0], 0.9999999999879223)

    @attr(all=True, unit=True)
    def test_calculate_probability_zero_division(self):
        """
        (TestGrowth) calculate_probability should return True when there is a zero division error
        """

        self.DUT.lst_p_mtbfi = [0.0, 46.4935065, 0.0, 0.0, 0.0]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_fef = [0.65, 0.7, 0.6, 0.65, 0.55]
        self.DUT.lst_p_ms = [0.9, 0.6586271, 0.0, 0.0, 0.0]
        self.DUT.lst_p_prob = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.assertTrue(self.DUT.calculate_probability())
        self.assertEqual(self.DUT.lst_p_prob[0], 0.0)

    @attr(all=True, unit=True)
    def test_calculate_growth_potential(self):
        """
        (TestGrowth) calculate_growth_potential should return False
        """

        self.DUT.lst_p_mtbfi = [35.8, 46.4935065, 0.0, 0.0, 0.0]
        self.DUT.avg_ms = 0.9
        self.DUT.avg_fef = 0.65

        self.assertFalse(self.DUT.calculate_growth_potential())
        self.assertAlmostEqual(self.DUT.mtbfgp, 86.2650602)

    @attr(all=True, unit=True)
    def test_calculate_growth_potential_zero_fef_zero_ms(self):
        """
        (TestGrowth) calculate_growth_potential should return True when the FEF and/or MS are zero
        """

        self.DUT.lst_p_mtbfi = [35.8, 46.4935065, 0.0, 0.0, 0.0]
        self.DUT.avg_ms = 0.0
        self.DUT.avg_fef = 0.0

        self.assertTrue(self.DUT.calculate_growth_potential())
        self.assertEqual(self.DUT.mtbfgp, 35.8)

    @attr(all=True, unit=True)
    def test_calculate_growth_potential_zero_division_error(self):
        """
        (TestGrowth) calculate_growth_potential should return True when the FEF and MS are both equal to one
        """

        self.DUT.lst_p_mtbfi = [35.8, 46.4935065, 0.0, 0.0, 0.0]
        self.DUT.avg_ms = 1.0
        self.DUT.avg_fef = 1.0

        self.assertTrue(self.DUT.calculate_growth_potential())
        self.assertEqual(self.DUT.mtbfgp, 35.8)

    @attr(all=True, unit=True)
    def test_calculate_idealized_values_mtbf(self):
        """
        (TestGrowth) calculate_idealized_values should return a list of idealized values using MTBF
        """

        self.DUT.lst_p_mtbfi = [68.0]
        self.DUT.lst_p_mtbff = [130.0]
        self.DUT.lst_p_test_time = [5.0]

        self.DUT.ttt = 28.0
        self.DUT.avg_growth = 0.23

        _ideal = self.DUT.calculate_idealized_growth_curve()
        self.assertEqual(_ideal, [68.0, 68.0, 68.0, 68.0, 68.0, np.nan,
                                  91.662900231750001, 94.924655460703661,
                                  97.843786611326578, 100.49306637325681,
                                  102.92365442293124, 105.17299361680951,
                                  107.26937634837147, 109.23474261071321,
                                  111.08647626912771, 112.83860328607791,
                                  114.50261712016706, 116.08806307019879,
                                  117.60296183014364, 119.05412286565567,
                                  120.44738049450172, 121.78777460303299,
                                  123.07969097031288, 124.32697163319288,
                                  125.53300269876129, 126.70078495028643,
                                  127.83299116437281, 128.93201305008046])

    @attr(all=True, unit=True)
    def test_calculate_idealized_values_failure_intensity(self):
        """
        (TestGrowth) calculate_idealized_values should return a list of idealized values using failure intensity
        """

        self.DUT.lst_p_mtbfi = [68.0]
        self.DUT.lst_p_mtbff = [130.0]
        self.DUT.lst_p_test_time = [5.0]

        self.DUT.ttt = 28.0
        self.DUT.avg_growth = 0.23

        _ideal = self.DUT.calculate_idealized_growth_curve(False)
        self.assertEqual(_ideal, [0.014705882352941176, 0.014705882352941176,
                                  0.014705882352941176, 0.014705882352941176,
                                  0.014705882352941176, np.nan,
                                  0.010909539164391639, 0.010534670841275521,
                                  0.01022037305212223, 0.0099509352842886249,
                                  0.0097159395049346547, 0.0095081443021716242,
                                  0.0093223251037870113, 0.0091545965697357248,
                                  0.0090019958647109613, 0.0088622153312613774,
                                  0.0087334248347400653, 0.0086141500990958662,
                                  0.0085031872024134945, 0.0083995411156691374,
                                  0.0083023806403631079, 0.0082110047848357372,
                                  0.0081248172798971553, 0.0080433069901384088,
                                  0.0079660326647302254, 0.007892610928909161,
                                  0.007822706727672199, 0.0077560256474982266])

    @attr(all=True, unit=True)
    def test_calculate_planned_growth_curve(self):
        """
        (TestGrowth) calculate_planned_growth_curve should return False
        """

        # These inputs are from MIL-HDBK-189, section 5.2.6.2.2, Case 2.
        self.DUT.lst_p_n_failures = [0, 0, 0, 0, 0]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]
        self.DUT.lst_p_mtbfi = [35.8, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbfa = [35.8, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.DUT.n_phases = 5
        self.DUT.ttt = 10000.0

        self.assertFalse(self.DUT.calculate_planned_growth_curve())
        self.assertAlmostEqual(self.DUT.lst_p_n_failures[0], 27.9329609)
        self.assertAlmostEqual(self.DUT.lst_p_n_failures[1], 28.6298235)
        self.assertAlmostEqual(self.DUT.lst_p_n_failures[2], 39.8920227)
        self.assertAlmostEqual(self.DUT.lst_p_n_failures[3], 28.5257523)
        self.assertAlmostEqual(self.DUT.lst_p_n_failures[4], 39.5009086)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfa[0], 41.1467532)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfa[1], 52.3929182)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfa[2], 62.6691712)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfa[3], 70.1120860)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfa[4], 75.9476201)
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[0], 46.4935065)
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[1], 57.4008738)
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[2], 67.3217509)
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[3], 72.7385854)
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[4], 78.9573023)

    @attr(all=True, unit=True)
    def test_create_planned_values_mtbf(self):
        """
        (TestGrowth) create_planned_values should return a list of MTBF values to plot
        """

        self.DUT.lst_p_test_time = [5.0]
        self.DUT.lst_p_mtbfa = [50.0]

        _plan = self.DUT.create_planned_values(0)
        self.assertEqual(_plan, [50.0, 50.0, 50.0, 50.0, np.nan])

    @attr(all=True, unit=True)
    def test_create_planned_values_failure_intensity(self):
        """
        (TestGrowth) create_planned_values should return a list of failure intensity values to plot
        """

        self.DUT.lst_p_test_time = [5.0]
        self.DUT.lst_p_mtbfa = [50.0]

        _plan = self.DUT.create_planned_values(0, False)
        self.assertEqual(_plan, [0.02, 0.02, 0.02, 0.02, np.nan])

    @attr(all=True, unit=True)
    def test_assess_plan_feasibility(self):
        """
        (TestGrowth) assess_plan_feasibility should return False
        """

        self.DUT.lst_p_start_date = [735599, 735689, 735764, 735856, 735964]
        self.DUT.lst_p_end_date = [735672, 735749, 735841, 735917, 736084]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_n_test_units = [5, 5, 4, 4, 3]

        self.DUT.lst_p_tpu = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_tpupw = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.DUT.n_phases = 5

        self.assertEqual(self.DUT.assess_plan_feasibility(),
                         [False, False, 0, 0])
        self.assertEqual(self.DUT.lst_p_tpu,
                         [200.0, 300.0, 625.0, 500.0, 1000.0])
        self.assertEqual(self.DUT.lst_p_tpupw,
                         [19.17808219178082, 35.0, 56.81818181818182,
                          57.37704918032787, 58.333333333333336])

    @attr(all=True, unit=True)
    def test_estimate_crow_amsaa_exact(self):
        """
        (TestGrowth) estimate_crow_amsaa should return False using exact failure times
        """

        # For example data, see http://www.reliawiki.org/index.php/Crow-AMSAA_%28NHPP%29#Example_-_Parameter_Estimation
        self.DUT.dic_test_data = {0: [719163, 0.0, 2.7, 1],
                                  1: [719163, 0.0, 10.3, 1],
                                  2: [719163, 0.0, 12.5, 1],
                                  3: [719163, 0.0, 30.6, 1],
                                  4: [719163, 0.0, 57.0, 1],
                                  5: [719163, 0.0, 61.3, 1],
                                  6: [719163, 0.0, 80.0, 1],
                                  7: [719163, 0.0, 109.5, 1],
                                  8: [719163, 0.0, 125.0, 1],
                                  9: [719163, 0.0, 128.6, 1],
                                  10: [719163, 0.0, 143.8, 1],
                                  11: [719163, 0.0, 167.9, 1],
                                  12: [719163, 0.0, 229.2, 1],
                                  13: [719163, 0.0, 296.7, 1],
                                  14: [719163, 0.0, 320.6, 1],
                                  15: [719163, 0.0, 328.2, 1],
                                  16: [719163, 0.0, 366.2, 1],
                                  17: [719163, 0.0, 396.7, 1],
                                  18: [719163, 0.0, 421.1, 1],
                                  19: [719163, 0.0, 438.2, 1],
                                  20: [719163, 0.0, 501.2, 1],
                                  21: [719163, 0.0, 620.0, 1]}

        self.DUT.grouped = False

        self.assertFalse(self.DUT.estimate_crow_amsaa())
        self.assertEqual(self.DUT.alpha_hat, [0.32279203293521613,
                                              0.42394221488057504,
                                              0.52924893703956533])
        self.assertEqual(self.DUT.beta_hat, [0.51077399351295227,
                                             0.6142103999317297,
                                             0.8474287960726461])

    @attr(all=True, unit=True)
    def test_estimate_crow_amsaa_grouped(self):
        """
        (TestGrowth) estimate_crow_amsaa should return False using grouped failure times
        """

        # For example data, see http://www.reliawiki.org/index.php/Crow-AMSAA_%28NHPP%29#Example_-_Parameter_Estimation
        self.DUT.dic_test_data = {0: [719163, 0.0, 62.0, 12],
                                  1: [719163, 0.0, 100.0, 6],
                                  2: [719163, 62.0, 187.0, 15],
                                  3: [719163, 187.0, 210.0, 3],
                                  4: [719163, 210.0, 350.0, 18],
                                  5: [719163, 350.0, 500.0, 16]}

        self.DUT.grouped = True

        self.assertFalse(self.DUT.estimate_crow_amsaa())
        self.assertEqual(self.DUT.alpha_hat, [0.38537715881590562,
                                              0.44585433767531873,
                                              0.50770467031237509])
        self.assertEqual(self.DUT.beta_hat, [0.7231246075396317,
                                             0.81360853965677293,
                                             0.95456866230721715])

    @attr(all=True, unit=True)
    def test_calculate_crow_amsaa_mean(self):
        """
        (TestGrowth) calculate_crow_amsaa_mean should return False on success
        """

        self.DUT.dic_test_data = {0: [719163, 0.0, 2.7, 1],
                                  1: [719163, 0.0, 10.3, 1],
                                  2: [719163, 0.0, 12.5, 1],
                                  3: [719163, 0.0, 30.6, 1],
                                  4: [719163, 0.0, 57.0, 1],
                                  5: [719163, 0.0, 61.3, 1],
                                  6: [719163, 0.0, 80.0, 1],
                                  7: [719163, 0.0, 109.5, 1],
                                  8: [719163, 0.0, 125.0, 1],
                                  9: [719163, 0.0, 128.6, 1],
                                  10: [719163, 0.0, 143.8, 1],
                                  11: [719163, 0.0, 167.9, 1],
                                  12: [719163, 0.0, 229.2, 1],
                                  13: [719163, 0.0, 296.7, 1],
                                  14: [719163, 0.0, 320.6, 1],
                                  15: [719163, 0.0, 328.2, 1],
                                  16: [719163, 0.0, 366.2, 1],
                                  17: [719163, 0.0, 396.7, 1],
                                  18: [719163, 0.0, 421.1, 1],
                                  19: [719163, 0.0, 438.2, 1],
                                  20: [719163, 0.0, 501.2, 1],
                                  21: [719163, 0.0, 620.0, 1]}

        self.DUT.alpha_hat = [0.32279203293521613,
                              0.42394221488057504,
                              0.52924893703956533]
        self.DUT.beta_hat = [0.51077399351295227,
                             0.6142103999317297,
                             0.8474287960726461]

        self.assertFalse(self.DUT.calculate_crow_amsaa_mean())
        self.assertEqual(self.DUT.cum_mean[0], [1.2984255368000672,
                                                3.4602620492308573,
                                                20.219964361430275])
        self.assertAlmostEqual(self.DUT.instantaneous_mean[0][1], 5.6336754)

    @attr(all=True, unit=True)
    def test_calculate_cramer_vonmises_typei(self):
        """
        (TestGrowth) calculate_cramer_vonmises should return False on success with Type I (time terminated) data
        """

        self.DUT.dic_test_data = {0: [719163, 0.0, 2.7, 1],
                                  1: [719163, 0.0, 10.3, 1],
                                  2: [719163, 0.0, 12.5, 1],
                                  3: [719163, 0.0, 30.6, 1],
                                  4: [719163, 0.0, 57.0, 1],
                                  5: [719163, 0.0, 61.3, 1],
                                  6: [719163, 0.0, 80.0, 1],
                                  7: [719163, 0.0, 109.5, 1],
                                  8: [719163, 0.0, 125.0, 1],
                                  9: [719163, 0.0, 128.6, 1],
                                  10: [719163, 0.0, 143.8, 1],
                                  11: [719163, 0.0, 167.9, 1],
                                  12: [719163, 0.0, 229.2, 1],
                                  13: [719163, 0.0, 296.7, 1],
                                  14: [719163, 0.0, 320.6, 1],
                                  15: [719163, 0.0, 328.2, 1],
                                  16: [719163, 0.0, 366.2, 1],
                                  17: [719163, 0.0, 396.7, 1],
                                  18: [719163, 0.0, 421.1, 1],
                                  19: [719163, 0.0, 438.2, 1],
                                  20: [719163, 0.0, 501.2, 1],
                                  21: [719163, 0.0, 620.0, 1]}

        self.DUT.beta_hat = [0.51077399351295227,
                             0.6142103999317297,
                             0.8474287960726461]

        self.assertFalse(self.DUT.calculate_cramer_vonmises(t_star=650.0,
                                                            type2=False))
        self.assertAlmostEqual(self.DUT.cramer_vonmises, 0.03383013)

    @attr(all=True, unit=True)
    def test_calculate_cramer_vonmises_typeii(self):
        """
        (TestGrowth) calculate_cramer_vonmises should return False on success with Type II (failure terminated) data
        """

        self.DUT.dic_test_data = {0: [719163, 0.0, 2.7, 1],
                                  1: [719163, 0.0, 10.3, 1],
                                  2: [719163, 0.0, 12.5, 1],
                                  3: [719163, 0.0, 30.6, 1],
                                  4: [719163, 0.0, 57.0, 1],
                                  5: [719163, 0.0, 61.3, 1],
                                  6: [719163, 0.0, 80.0, 1],
                                  7: [719163, 0.0, 109.5, 1],
                                  8: [719163, 0.0, 125.0, 1],
                                  9: [719163, 0.0, 128.6, 1],
                                  10: [719163, 0.0, 143.8, 1],
                                  11: [719163, 0.0, 167.9, 1],
                                  12: [719163, 0.0, 229.2, 1],
                                  13: [719163, 0.0, 296.7, 1],
                                  14: [719163, 0.0, 320.6, 1],
                                  15: [719163, 0.0, 328.2, 1],
                                  16: [719163, 0.0, 366.2, 1],
                                  17: [719163, 0.0, 396.7, 1],
                                  18: [719163, 0.0, 421.1, 1],
                                  19: [719163, 0.0, 438.2, 1],
                                  20: [719163, 0.0, 501.2, 1],
                                  21: [719163, 0.0, 620.0, 1]}

        self.DUT.beta_hat = [0.51077399351295227,
                             0.6142103999317297,
                             0.8474287960726461]

        self.assertFalse(self.DUT.calculate_cramer_vonmises())
        self.assertAlmostEqual(self.DUT.cramer_vonmises, 0.04488069)

    @attr(all=True, unit=True)
    def test_calculate_chi_square_exact(self):
        """
        (TestGrowth) calculate_chi_square should return False on success with exact data
        """

        self.DUT.dic_test_data = {0: [719163, 0.0, 2.7, 1],
                                  1: [719163, 0.0, 10.3, 1],
                                  2: [719163, 0.0, 12.5, 1],
                                  3: [719163, 0.0, 30.6, 1],
                                  4: [719163, 0.0, 57.0, 1],
                                  5: [719163, 0.0, 61.3, 1],
                                  6: [719163, 0.0, 80.0, 1],
                                  7: [719163, 0.0, 109.5, 1],
                                  8: [719163, 0.0, 125.0, 1],
                                  9: [719163, 0.0, 128.6, 1],
                                  10: [719163, 0.0, 143.8, 1],
                                  11: [719163, 0.0, 167.9, 1],
                                  12: [719163, 0.0, 229.2, 1],
                                  13: [719163, 0.0, 296.7, 1],
                                  14: [719163, 0.0, 320.6, 1],
                                  15: [719163, 0.0, 328.2, 1],
                                  16: [719163, 0.0, 366.2, 1],
                                  17: [719163, 0.0, 396.7, 1],
                                  18: [719163, 0.0, 421.1, 1],
                                  19: [719163, 0.0, 438.2, 1],
                                  20: [719163, 0.0, 501.2, 1],
                                  21: [719163, 0.0, 620.0, 1]}

        self.DUT.ttt = 620.0
        self.DUT.beta_hat = [0.51077399351295227,
                             0.6142103999317297,
                             0.8474287960726461]
        self.DUT.grouped = False
        self.DUT.confidence = 0.90

        self.assertFalse(self.DUT.calculate_chi_square())
        self.assertAlmostEqual(self.DUT.chi_square, 71.6366900)
        self.assertAlmostEqual(self.DUT.chi2_critical_value[0], 29.7874771)
        self.assertAlmostEqual(self.DUT.chi2_critical_value[1], 60.4808866)

    @attr(all=True, unit=True)
    def test_calculate_chi_square_grouped(self):
        """
        (TestGrowth) calculate_chi_square should return False on success with grouped data
        """

        self.DUT.dic_test_data = {0: [719163, 0.0, 62.0, 12],
                                  1: [719163, 0.0, 100.0, 6],
                                  2: [719163, 62.0, 187.0, 15],
                                  3: [719163, 187.0, 210.0, 3],
                                  4: [719163, 210.0, 350.0, 18],
                                  5: [719163, 350.0, 500.0, 16]}

        self.DUT.ttt = 500.0
        self.DUT.beta_hat = [0.7231246075396317,
                             0.81360853965677293,
                             0.95456866230721715]
        self.DUT.grouped = True

        self.assertFalse(self.DUT.calculate_chi_square())
        self.assertAlmostEqual(self.DUT.chi_square, 69.1068657)

    @attr(all=True, unit=True)
    def test_assess_growth_rate(self):
        """
        (TestGrowth) assess_growth_rate should return False on success
        """

        self.DUT.dic_test_data = {0: [719163, 0.0, 2.7, 1],
                                  1: [719163, 0.0, 10.3, 1],
                                  2: [719163, 0.0, 12.5, 1],
                                  3: [719163, 0.0, 30.6, 1],
                                  4: [719163, 0.0, 57.0, 1],
                                  5: [719163, 0.0, 61.3, 1],
                                  6: [719163, 0.0, 80.0, 1],
                                  7: [719163, 0.0, 109.5, 1],
                                  8: [719163, 0.0, 125.0, 1],
                                  9: [719163, 0.0, 128.6, 1],
                                  10: [719163, 0.0, 143.8, 1],
                                  11: [719163, 0.0, 167.9, 1],
                                  12: [719163, 0.0, 229.2, 1],
                                  13: [719163, 0.0, 296.7, 1],
                                  14: [719163, 0.0, 320.6, 1],
                                  15: [719163, 0.0, 328.2, 1],
                                  16: [719163, 0.0, 366.2, 1],
                                  17: [719163, 0.0, 396.7, 1],
                                  18: [719163, 0.0, 421.1, 1],
                                  19: [719163, 0.0, 438.2, 1],
                                  20: [719163, 0.0, 501.2, 1],
                                  21: [719163, 0.0, 620.0, 1]}

        self.DUT.estimate_crow_amsaa()
        self.assertFalse(self.DUT.assess_growth_rate())
        self.assertAlmostEqual(self.DUT.lst_o_growth_rate[1], 0.3857896)


class TestGrowthController(unittest.TestCase):
    """
    Class for testing the Growth data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Growth class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Growth()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestGrowth) __init__ should create a Growth data controller
        """

        self.assertTrue(isinstance(self.DUT, Growth))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicTests, {})

    @attr(all=True, integration=True)
    def test_request_tests(self):
        """
        (TestGrowth) request_tests should return 0 on success
        """

        _test = (0, 7, 1, u'Test Plan', u'Description', 4, u'Attachment', 0.0,
                 0, 0.75, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 1, 0.0, 0.3, 0.0, 0.7,
                 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.assertEqual(self.DUT.request_tests(self._dao, _test)[1], 0)

    @attr(all=True, integration=True)
    def test_request_test_data(self):
        """
        (TestGrowth) request_test_data should return a tuple on success
        """

        self.DUT._dao = self._dao

        self.assertEqual(self.DUT.request_test_data(1), ([], 0))

# TODO: Test that method fails when no Testing inputs exist in database.
    @attr(all=True, integration=True)
    def test_add_test(self):
        """
        (TestGrowth) add_test returns 0 on success and new Testing data model added to dictionary
        """

        _test = (0, 7, 1, u'Test Plan', u'Description', 4, u'Attachment', 0.0,
                 0, 0.75, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 1, 0.0, 0.3, 0.0, 0.7,
                 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.assertEqual(self.DUT.request_tests(self._dao, _test)[1], 0)
        (_results, _error_code) = self.DUT.add_test(0, 7)

        self.assertTrue(isinstance(self.DUT.dicGrowth[self.DUT._last_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=False)
    def test_delete_test(self):
        """
        (TestGrowth) delete_test returns 0 on success
        """

        _test = (0, 7, 1, u'Test Plan', u'Description', 4, u'Attachment', 0.0,
                 0, 0.75, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 1, 0.0, 0.3, 0.0, 0.7,
                 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.assertEqual(self.DUT.request_tests(self._dao, _test)[1], 0)
        (_results,
         _error_code) = self.DUT.delete_test(self.DUT._last_id - 1)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_test(self):
        """
        (TestGrowth) save_test returns (True, 0) on success
        """

        _test = (0, 7, 1, u'Test Plan', u'Description', 4, u'Attachment', 0.0,
                 0, 0.75, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 1, 0.0, 0.3, 0.0, 0.7,
                 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.DUT.request_tests(self._dao, _test)
        self.assertEqual(self.DUT.save_test(1), (True, 0))

    @attr(all=True, integration=True)
    def test_save_all_tests(self):
        """
        (TestGrowth) save_all_tests returns False on success
        """

        _test = (0, 7, 1, u'Test Plan', u'Description', 4, u'Attachment', 0.0,
                 0, 0.75, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 1, 0.0, 0.3, 0.0, 0.7,
                 0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.DUT.request_tests(self._dao, _test)
        self.assertFalse(self.DUT.save_all_tests())
