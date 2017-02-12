#!/usr/bin/env python -O
"""
This is the test class for testing Growth Testing module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.testing.TestGrowth.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr
import numpy as np

from testing.growth.Growth import Model, Growth

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestGrowthModel(unittest.TestCase):
    """
    Class for testing the Reliability Growth data model class.  We use the
    example test plan in the original revision of MIL-HDBK-189:

    self.DUT.lst_p_mtbfa = [50.0, 73.0, 87.0, 98.0, 106.0]
    self.DUT.lst_p_mtbfi = [45.0, 64.9350649, 80.1688181, 94.0247917,
                            101.5902031]
    self.DUT.lst_p_mtbff = [55.0, 80.1688181, 94.0247917, 101.5902031, 110.0]

    self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
    self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]
    self.DUT.lst_p_n_failures = [20.0, 20.5, 28.6, 20.4, 28.3]

    self.DUT.avg_growth = 0.23
    self.DUT.ttt = 10000.0
    self.DUT.mtbfg = 110.0

    self.DUT.n_phases = 5
    """

    def setUp(self):
        """
        Setup the test fixture for the Reliability Growth class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test00_create(self):
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
    def test01_set_attributes(self):
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
    def test02_set_attributes_wrong_type(self):
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
    def test03_set_attributes_missing_index(self):
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
    def test04_set_phase_attributes(self):
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
    def test05_set_phase_attributes_wrong_type(self):
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
    def test06_set_phase_attributes_missing_index(self):
        """
        (TestGrowth) set_phase_attributes should return a 40 error code when too few items are passed
        """

        _values = (1, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 719163,
                   719163, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        (_error_code,
         _error_msg) = self.DUT.set_phase_attributes(_values, 0)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test07_get_attributes(self):
        """
        (TestGrowth) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (None, None, 0, '', '', 0, '', 0.0, 0, 0.75, 0.0,
                          0.0, 0, 0, 0.0, 0.0, 0, 1, 0.0, 0.0, 0.75, 0.7,
                          0.75, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0))

    @attr(all=True, unit=True)
    def test08_get_phase_attributes(self):
        """
        (TestGrowth) get_phase_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_phase_attributes(),
                         ([0.0], [0.0], [0.0], [0], [0.0], [0.0], [0.0], [0.0],
                          [0.0], [0.0], [0.0], [0.0], [0], [0], [0], [0.0],
                          [0.0], [0.0], [0.0], [0.0, 0.0, 0.0], [0.0], [0.0],
                          [0.0], [0.0], [0.0], [0.0], [[0.0, 0.0, 0.0]],
                          [[0.0, 0.0, 0.0]]))

    @attr(all=True, unit=True)
    def test09_sanity(self):
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
    def test13_calculate_idealized_values_mtbf(self):
        """
        (TestGrowth) calculate_idealized_values should return a list of idealized values using MTBF
        """

        self.DUT.lst_i_mtbfa = [50.0, 73.0, 87.0, 98.0, 106.0]
        self.DUT.lst_i_mtbfi = [45.0, 64.9350649, 80.1688181, 94.0247917,
                                101.5902031]
        self.DUT.lst_i_mtbff = [55.0, 80.1688181, 94.0247917, 101.5902031,
                                110.0]
        self.DUT.lst_i_n_failures = [20.0, 20.5, 28.6, 20.4, 28.3]

        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.avg_growth = 0.23
        self.DUT.ttt = 10000.0
        self.DUT.mtbfg = 110.0

        self.DUT.n_phases = 5

        _ideal = self.DUT.calculate_idealized_growth_curve()
        self.assertEqual(_ideal[0], 50.0)
        np.testing.assert_equal(_ideal[1000], np.nan)
        self.assertAlmostEqual(_ideal[1001], 64.9499943)
        self.assertAlmostEqual(_ideal[2500], 80.1688181)
        self.assertAlmostEqual(_ideal[5000], 94.0247917)
        self.assertAlmostEqual(_ideal[7000], 101.5902031)
        self.assertAlmostEqual(_ideal[9999], 110.2730254)

    @attr(all=True, unit=True)
    def test13a_calculate_idealized_values_mtbf_no_growth(self):
        """
        (TestGrowth) calculate_idealized_values should return a list of idealized values using MTBF and no growth rate specified
        """

        self.DUT.lst_i_mtbfa = [50.0, 73.0, 87.0, 98.0, 106.0]
        self.DUT.lst_i_mtbfi = [45.0, 64.9350649, 80.1688181, 94.0247917,
                                101.5902031]
        self.DUT.lst_i_mtbff = [55.0, 80.1688181, 94.0247917, 101.5902031,
                                110.0]
        self.DUT.lst_i_n_failures = [20.0, 20.5, 28.6, 20.4, 28.3]

        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.DUT.avg_growth = 0.0
        self.DUT.ttt = 10000.0
        self.DUT.mtbfg = 110.0

        self.DUT.n_phases = 5

        _ideal = self.DUT.calculate_idealized_growth_curve()
        self.assertAlmostEqual(self.DUT.avg_growth, 0.2306829)
        self.assertEqual(_ideal[0], 50.0)
        np.testing.assert_equal(_ideal[1000], np.nan)
        self.assertAlmostEqual(_ideal[1001], 65.0076965)
        self.assertAlmostEqual(_ideal[2500], 80.2902140)
        self.assertAlmostEqual(_ideal[5000], 94.2117565)
        self.assertAlmostEqual(_ideal[7000], 101.8156050)
        self.assertAlmostEqual(_ideal[9999], 110.5446089)

    @attr(all=True, unit=True)
    def test13b_calculate_idealized_values_mtbf_no_mtbfa(self):
        """
        (TestGrowth) calculate_idealized_values should return a list of idealized values when program initial MTBF equals zero
        """

        self.DUT.lst_i_mtbfa = [0.0, 73.0, 87.0, 98.0, 106.0]
        self.DUT.lst_i_mtbfi = [45.0, 64.9350649, 80.1688181, 94.0247917,
                                101.5902031]
        self.DUT.lst_i_mtbff = [55.0, 80.1688181, 94.0247917, 101.5902031,
                                110.0]
        self.DUT.lst_i_n_failures = [20.0, 20.5, 28.6, 20.4, 28.3]

        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.avg_growth = 0.23
        self.DUT.ttt = 10000.0
        self.DUT.mtbfg = 110.0

        self.DUT.n_phases = 5

        _ideal = self.DUT.calculate_idealized_growth_curve()
        self.assertAlmostEqual(self.DUT.lst_i_mtbfa[0], 49.8750576)
        self.assertAlmostEqual(_ideal[0], 49.8750576)
        np.testing.assert_equal(_ideal[1000], np.nan)
        self.assertAlmostEqual(_ideal[1001], 64.7876941)
        self.assertAlmostEqual(_ideal[2500], 79.9684885)
        self.assertAlmostEqual(_ideal[5000], 93.7898381)
        self.assertAlmostEqual(_ideal[7000], 101.3363446)
        self.assertAlmostEqual(_ideal[9999], 109.9974699)

    @attr(all=True, unit=True)
    def test13c_calculate_idealized_values_mtbf_no_mtbfg(self):
        """
        (TestGrowth) calculate_idealized_values should return a list of idealized values when the final MTBF is zero
        """

        self.DUT.lst_i_mtbfa = [50.0, 73.0, 87.0, 98.0, 106.0]
        self.DUT.lst_i_mtbfi = [45.0, 64.9350649, 80.1688181, 94.0247917,
                                101.5902031]
        self.DUT.lst_i_mtbff = [55.0, 80.1688181, 94.0247917, 101.5902031,
                                110.0]
        self.DUT.lst_i_n_failures = [20.0, 20.5, 28.6, 20.4, 28.3]

        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.avg_growth = 0.23
        self.DUT.ttt = 10000.0
        self.DUT.mtbfg = 0.0

        self.DUT.n_phases = 5

        _ideal = self.DUT.calculate_idealized_growth_curve()
        self.assertAlmostEqual(self.DUT.mtbfg, 110.2755618)
        self.assertEqual(_ideal[0], 50.0)
        np.testing.assert_equal(_ideal[1000], np.nan)
        self.assertAlmostEqual(_ideal[1001], 64.9499943)
        self.assertAlmostEqual(_ideal[2500], 80.1688181)
        self.assertAlmostEqual(_ideal[5000], 94.0247917)
        self.assertAlmostEqual(_ideal[7000], 101.5902031)
        self.assertAlmostEqual(_ideal[9999], 110.2730254)

    @attr(all=True, unit=True)
    def test13d_calculate_idealized_values_mtbf_no_ttt(self):
        """
        (TestGrowth) calculate_idealized_values should return a list of idealized values when the total time on test is zero
        """

        self.DUT.lst_i_mtbfa = [50.0, 73.0, 87.0, 98.0, 106.0]
        self.DUT.lst_i_mtbfi = [45.0, 64.9350649, 80.1688181, 94.0247917,
                                101.5902031]
        self.DUT.lst_i_mtbff = [55.0, 80.1688181, 94.0247917, 101.5902031,
                                110.0]
        self.DUT.lst_i_n_failures = [20.0, 20.5, 28.6, 20.4, 28.3]

        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.avg_growth = 0.23
        self.DUT.ttt = 0.0
        self.DUT.mtbfg = 110.0

        self.DUT.n_phases = 5

        _ideal = self.DUT.calculate_idealized_growth_curve()
        self.assertAlmostEqual(self.DUT.ttt, 9892)
        self.assertEqual(_ideal[0], 50.0)
        np.testing.assert_equal(_ideal[1000], np.nan)
        self.assertAlmostEqual(_ideal[1001], 64.9499943)
        self.assertAlmostEqual(_ideal[2500], 80.1688181)
        self.assertAlmostEqual(_ideal[5000], 94.0247917)
        self.assertAlmostEqual(_ideal[7000], 101.5902031)
        self.assertAlmostEqual(_ideal[8890], 107.3313728)

    @attr(all=True, unit=True)
    def test13e_calculate_idealized_values_mtbf_no_t1(self):
        """
        (TestGrowth) calculate_idealized_values should return a list of idealized values when the first phase test time is zero
        """

        self.DUT.lst_i_mtbfa = [50.0, 73.0, 87.0, 98.0, 106.0]
        self.DUT.lst_i_mtbfi = [45.0, 64.9350649, 80.1688181, 94.0247917,
                                101.5902031]
        self.DUT.lst_i_mtbff = [55.0, 80.1688181, 94.0247917, 101.5902031,
                                110.0]
        self.DUT.lst_i_n_failures = [20.0, 20.5, 28.6, 20.4, 28.3]

        self.DUT.lst_p_test_time = [0.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.avg_growth = 0.23
        self.DUT.ttt = 10000.0
        self.DUT.mtbfg = 110.0

        self.DUT.n_phases = 5

        _ideal = self.DUT.calculate_idealized_growth_curve()
        self.assertAlmostEqual(self.DUT.lst_p_test_time[0], 1011)
        self.assertEqual(_ideal[0], 50.0)
        np.testing.assert_equal(_ideal[1011], np.nan)
        self.assertAlmostEqual(_ideal[1012], 64.9498319)
        self.assertAlmostEqual(_ideal[2510], 80.0408090)
        self.assertAlmostEqual(_ideal[5010], 93.8316148)
        self.assertAlmostEqual(_ideal[7010], 101.3681820)
        self.assertAlmostEqual(_ideal[9999], 109.9959067)

    @attr(all=True, unit=True)
    def test13f_calculate_idealized_values_failure_intensity(self):
        """
        (TestGrowth) calculate_idealized_values should return a list of idealized values using failure intensity
        """

        self.DUT.lst_i_mtbfa = [50.0, 73.0, 87.0, 98.0, 106.0]
        self.DUT.lst_i_mtbfi = [45.0, 64.9350649, 80.1688181, 94.0247917,
                                101.5902031]
        self.DUT.lst_i_mtbff = [55.0, 80.1688181, 94.0247917, 101.5902031,
                                110.0]
        self.DUT.lst_i_n_failures = [20.0, 20.5, 28.6, 20.4, 28.3]

        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.avg_growth = 0.23
        self.DUT.ttt = 10000.0
        self.DUT.mtbfg = 110.0

        self.DUT.n_phases = 5

        _ideal = self.DUT.calculate_idealized_growth_curve(mtbf=False)
        self.assertEqual(_ideal[0], 0.02)
        np.testing.assert_equal(_ideal[1000], np.nan)
        self.assertAlmostEqual(_ideal[1001], 0.01539646)
        self.assertAlmostEqual(_ideal[2500], 0.01247368)
        self.assertAlmostEqual(_ideal[5000], 0.01063549)
        self.assertAlmostEqual(_ideal[7000], 0.009843469)
        self.assertAlmostEqual(_ideal[9999], 0.009068401)

    @attr(all=True, unit=True)
    def test14_calculate_planned_growth_curve_no_mtbfa(self):
        """
        (TestGrowth) calculate_planned_growth_curve should return False on success with average phase MTBF's equal to zero
        """

        # These inputs are from MIL-HDBK-189, section 5.2.6.2.2, Case 2.
        self.DUT.lst_i_n_failures = [0, 0, 0, 0, 0]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_mtbfa = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbfi = [45.0, 60.0, 78.0, 90.0, 105.0]
        self.DUT.lst_p_mtbff = [55.0, 72.0, 85.0, 100.0, 110.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.n_phases = 5
        self.DUT.ttt = 10000.0

        self.assertFalse(self.DUT.calculate_planned_growth_curve())
        self.assertEqual(self.DUT.lst_p_mtbfa[0], 50.0)
        self.assertEqual(self.DUT.lst_p_mtbfa[1], 66.0)
        self.assertEqual(self.DUT.lst_p_mtbfa[2], 81.5)
        self.assertEqual(self.DUT.lst_p_mtbfa[3], 95.0)
        self.assertEqual(self.DUT.lst_p_mtbfa[4], 107.5)

    @attr(all=True, unit=True)
    def test14a_calculate_planned_growth_curve_no_mtbfi(self):
        """
        (TestGrowth) calculate_planned_growth_curve should return False on success with final phase MTBF's equal to zero
        """

        # These inputs are from MIL-HDBK-189, section 5.2.6.2.2, Case 2.
        self.DUT.lst_i_n_failures = [0, 0, 0, 0, 0]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_mtbfa = [50.0, 66.0, 81.5, 95.0, 107.5]
        self.DUT.lst_p_mtbfi = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_mtbff = [55.0, 72.0, 85.0, 100.0, 110.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.n_phases = 5
        self.DUT.ttt = 10000.0

        self.assertFalse(self.DUT.calculate_planned_growth_curve())
        self.assertAlmostEqual(self.DUT.lst_p_mtbfi[0], 45.0)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfi[1], 60.0)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfi[2], 78.0)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfi[3], 90.0)
        self.assertAlmostEqual(self.DUT.lst_p_mtbfi[4], 105.0)

    @attr(all=True, unit=True)
    def test14b_calculate_planned_growth_curve_no_mtbff(self):
        """
        (TestGrowth) calculate_planned_growth_curve should return False on success with initial phase MTBF's equal to zero
        """

        # These inputs are from MIL-HDBK-189, section 5.2.6.2.2, Case 2.
        self.DUT.lst_i_n_failures = [0, 0, 0, 0, 0]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_mtbfa = [50.0, 66.0, 81.5, 95.0, 107.5]
        self.DUT.lst_p_mtbfi = [45.0, 60.0, 78.0, 90.0, 105.0]
        self.DUT.lst_p_mtbff = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_growth_rate = [0.23, 0.23, 0.23, 0.23, 0.23]

        self.DUT.n_phases = 5
        self.DUT.ttt = 10000.0

        self.assertFalse(self.DUT.calculate_planned_growth_curve())
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[0], 64.9350649)
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[1], 80.1688181)
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[2], 94.0247917)
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[3], 101.5902031)
        self.assertAlmostEqual(self.DUT.lst_p_mtbff[4], 110.2755618)

    @attr(all=True, unit=True)
    def test14c_calculate_planned_growth_curve_no_growth(self):
        """
        (TestGrowth) calculate_planned_growth_curve should return False on success with phase growth rate's equal to zero
        """

        # These inputs are from MIL-HDBK-189, section 5.2.6.2.2, Case 2.
        self.DUT.lst_i_n_failures = [0, 0, 0, 0, 0]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_mtbfa = [50.0, 66.0, 81.5, 95.0, 107.5]
        self.DUT.lst_p_mtbfi = [45.0, 60.0, 78.0, 90.0, 105.0]
        self.DUT.lst_p_mtbff = [55.0, 72.0, 85.0, 100.0, 110.0]
        self.DUT.lst_p_growth_rate = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.DUT.n_phases = 5
        self.DUT.ttt = 10000.0

        self.assertFalse(self.DUT.calculate_planned_growth_curve())
        self.assertAlmostEqual(self.DUT.lst_p_growth_rate[0], 0.1837827)
        self.assertAlmostEqual(self.DUT.lst_p_growth_rate[1], 0.1242327)
        self.assertAlmostEqual(self.DUT.lst_p_growth_rate[2], 0.0443355)
        self.assertAlmostEqual(self.DUT.lst_p_growth_rate[3], 0.0611243)
        self.assertAlmostEqual(self.DUT.lst_p_growth_rate[4], 0.0220512)

    @attr(all=True, unit=True)
    def test15_create_planned_values_mtbf(self):
        """
        (TestGrowth) create_planned_values should return a list of MTBF values to plot
        """

        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_mtbfa = [50.0, 66.0, 81.5, 95.0, 107.5]
        self.DUT.lst_p_mtbfi = [45.0, 60.0, 78.0, 90.0, 105.0]
        self.DUT.lst_p_mtbff = [55.0, 72.0, 85.0, 100.0, 110.0]

        self.DUT.n_phases = 5

        _plan = self.DUT.create_planned_values()
        self.assertEqual(_plan[0], 50.0)
        np.testing.assert_equal(_plan[999], np.nan)
        self.assertEqual(_plan[1000], 66.0)
        np.testing.assert_equal(_plan[2499], np.nan)
        self.assertEqual(_plan[2500], 81.5)
        np.testing.assert_equal(_plan[4999], np.nan)
        self.assertEqual(_plan[5000], 95.0)
        np.testing.assert_equal(_plan[6999], np.nan)
        self.assertEqual(_plan[7000], 107.5)
        np.testing.assert_equal(_plan[9999], np.nan)

    @attr(all=True, unit=True)
    def test15a_create_planned_values_failure_intensity(self):
        """
        (TestGrowth) create_planned_values should return a list of failure intensity values to plot
        """

        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_mtbfa = [50.0, 66.0, 81.5, 95.0, 107.5]
        self.DUT.lst_p_mtbfi = [45.0, 60.0, 78.0, 90.0, 105.0]
        self.DUT.lst_p_mtbff = [55.0, 72.0, 85.0, 100.0, 110.0]

        self.DUT.n_phases = 5

        _plan = self.DUT.create_planned_values(False)
        self.assertEqual(_plan[0], 0.02)
        np.testing.assert_equal(_plan[999], np.nan)
        self.assertAlmostEqual(_plan[1000], 0.01515151)
        np.testing.assert_equal(_plan[2499], np.nan)
        self.assertAlmostEqual(_plan[2500], 0.01226994)
        np.testing.assert_equal(_plan[4999], np.nan)
        self.assertAlmostEqual(_plan[5000], 0.01052632)
        np.testing.assert_equal(_plan[6999], np.nan)
        self.assertAlmostEqual(_plan[7000], 0.009302326)
        np.testing.assert_equal(_plan[9999], np.nan)

    @attr(all=True, unit=True)
    def test16_assess_plan_feasibility(self):
        """
        (TestGrowth) assess_plan_feasibility should return a list of integers with the last two equal to -1 on success
        """

        self.DUT.lst_p_ms = [0.95, 0.9, 0.90, 0.8, 0.75]
        self.DUT.lst_p_fef = [0.7, 0.7, 0.7, 0.7, 0.7]
        self.DUT.lst_p_prob = [0.95, 0.975, 0.975, 0.99, 0.99]

        self.DUT.lst_p_mtbfa = [50.0, 66.0, 81.5, 95.0, 107.5]
        self.DUT.lst_p_mtbfi = [45.0, 60.0, 78.0, 90.0, 105.0]
        self.DUT.lst_p_start_date = [735599, 735689, 735764, 735856, 735964]
        self.DUT.lst_p_end_date = [735672, 735749, 735841, 735917, 736084]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_n_test_units = [5, 5, 4, 4, 3]

        self.DUT.lst_p_tpu = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_tpupw = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.DUT.mtbfg = 110.0
        self.DUT.mtbfgp = 150.0
        self.DUT.avg_growth = 0.23
        self.DUT.avg_fef = 0.7

        self.DUT.n_phases = 5

        self.assertEqual(self.DUT.assess_plan_feasibility(),
                         [0.4090909090909091, 0.7333333333333333, -1, -1])
        self.assertEqual(self.DUT.lst_p_tpu,
                         [200.0, 300.0, 625.0, 500.0, 1000.0])
        self.assertEqual(self.DUT.lst_p_tpupw,
                         [19.17808219178082, 35.0, 56.81818181818182,
                          57.37704918032787, 58.333333333333336])

    @attr(all=True, unit=True)
    def test16a_assess_plan_feasibility_no_mtbfg(self):
        """
        (TestGrowth) assess_plan_feasibility should return a list of integers with the first position equal to -1 when the goal MTBF is equal to zero
        """

        self.DUT.lst_p_ms = [0.95, 0.9, 0.90, 0.8, 0.75]
        self.DUT.lst_p_fef = [0.7, 0.7, 0.7, 0.7, 0.7]
        self.DUT.lst_p_prob = [0.95, 0.975, 0.975, 0.99, 0.99]

        self.DUT.lst_p_mtbfa = [50.0, 66.0, 81.5, 95.0, 107.5]
        self.DUT.lst_p_mtbfi = [45.0, 60.0, 78.0, 90.0, 105.0]
        self.DUT.lst_p_start_date = [735599, 735689, 735764, 735856, 735964]
        self.DUT.lst_p_end_date = [735672, 735749, 735841, 735917, 736084]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_n_test_units = [5, 5, 4, 4, 3]

        self.DUT.lst_p_tpu = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_tpupw = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.DUT.mtbfg = 0.0
        self.DUT.mtbfgp = 150.0
        self.DUT.avg_growth = 0.23
        self.DUT.avg_fef = 0.7

        self.DUT.n_phases = 5

        self.assertEqual(self.DUT.assess_plan_feasibility(),
                         [0.0, 0.0, -1, -1])
        self.assertEqual(self.DUT.lst_p_tpu,
                         [200.0, 300.0, 625.0, 500.0, 1000.0])
        self.assertEqual(self.DUT.lst_p_tpupw,
                         [19.17808219178082, 35.0, 56.81818181818182,
                          57.37704918032787, 58.333333333333336])

    @attr(all=True, unit=True)
    def test16b_assess_plan_feasibility_no_mtbfgp(self):
        """
        (TestGrowth) assess_plan_feasibility should return a list of integers with the second position equal to -1 when the growth potential MTBF is equal to zero
        """

        self.DUT.lst_p_ms = [0.95, 0.9, 0.90, 0.8, 0.75]
        self.DUT.lst_p_fef = [0.7, 0.7, 0.7, 0.7, 0.7]
        self.DUT.lst_p_prob = [0.95, 0.975, 0.975, 0.99, 0.99]

        self.DUT.lst_p_mtbfa = [50.0, 66.0, 81.5, 95.0, 107.5]
        self.DUT.lst_p_mtbfi = [45.0, 60.0, 78.0, 90.0, 105.0]
        self.DUT.lst_p_start_date = [735599, 735689, 735764, 735856, 735964]
        self.DUT.lst_p_end_date = [735672, 735749, 735841, 735917, 736084]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_n_test_units = [5, 5, 4, 4, 3]

        self.DUT.lst_p_tpu = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_tpupw = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.DUT.mtbfg = 110.0
        self.DUT.mtbfgp = 0.0
        self.DUT.avg_growth = 0.23
        self.DUT.avg_fef = 0.7

        self.DUT.n_phases = 5

        self.assertEqual(self.DUT.assess_plan_feasibility(),
                         [0.4090909090909091, 0.0, -1, -1])
        self.assertEqual(self.DUT.lst_p_tpu,
                         [200.0, 300.0, 625.0, 500.0, 1000.0])
        self.assertEqual(self.DUT.lst_p_tpupw,
                         [19.17808219178082, 35.0, 56.81818181818182,
                          57.37704918032787, 58.333333333333336])

    @attr(all=True, unit=True)
    def test16c_assess_plan_feasibility_no_test_units(self):
        """
        (TestGrowth) assess_plan_feasibility should return a list of integers with the fifth position equal to the test phase with zero test units
        """

        self.DUT.lst_p_ms = [0.95, 0.9, 0.90, 0.8, 0.75]
        self.DUT.lst_p_fef = [0.7, 0.7, 0.7, 0.7, 0.7]
        self.DUT.lst_p_prob = [0.95, 0.975, 0.975, 0.99, 0.99]

        self.DUT.lst_p_mtbfa = [50.0, 66.0, 81.5, 95.0, 107.5]
        self.DUT.lst_p_mtbfi = [45.0, 60.0, 78.0, 90.0, 105.0]
        self.DUT.lst_p_start_date = [735599, 735689, 735764, 735856, 735964]
        self.DUT.lst_p_end_date = [735672, 735749, 735841, 735917, 736084]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_n_test_units = [5, 5, 0, 4, 3]

        self.DUT.lst_p_tpu = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_tpupw = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.DUT.mtbfg = 110.0
        self.DUT.mtbfgp = 150.0
        self.DUT.avg_growth = 0.23
        self.DUT.avg_fef = 0.7

        self.DUT.n_phases = 5

        self.assertEqual(self.DUT.assess_plan_feasibility(),
                         [0.4090909090909091, 0.7333333333333333, 2, -1])
        self.assertEqual(self.DUT.lst_p_tpu,
                         [200.0, 300.0, 0.0, 500.0, 1000.0])
        self.assertEqual(self.DUT.lst_p_tpupw,
                         [19.17808219178082, 35.0, 0.0, 57.37704918032787,
                          58.333333333333336])

    @attr(all=True, unit=True)
    def test16d_assess_plan_feasibility_same_dates(self):
        """
        (TestGrowth) assess_plan_feasibility should return a list of integers with the the sixth position equal to the test phase when the phase start and end dates are the same
        """

        self.DUT.lst_p_ms = [0.95, 0.9, 0.90, 0.8, 0.75]
        self.DUT.lst_p_fef = [0.7, 0.7, 0.7, 0.7, 0.7]
        self.DUT.lst_p_prob = [0.95, 0.975, 0.975, 0.99, 0.99]

        self.DUT.lst_p_mtbfa = [50.0, 66.0, 81.5, 95.0, 107.5]
        self.DUT.lst_p_mtbfi = [45.0, 60.0, 78.0, 90.0, 105.0]
        self.DUT.lst_p_start_date = [735599, 735689, 735764, 735856, 735964]
        self.DUT.lst_p_end_date = [735672, 735749, 735841, 735917, 735964]
        self.DUT.lst_p_test_time = [1000.0, 1500.0, 2500.0, 2000.0, 3000.0]
        self.DUT.lst_p_n_test_units = [5, 5, 4, 4, 3]

        self.DUT.lst_p_tpu = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.DUT.lst_p_tpupw = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.DUT.mtbfg = 110.0
        self.DUT.mtbfgp = 150.0
        self.DUT.avg_growth = 0.23
        self.DUT.avg_fef = 0.7

        self.DUT.n_phases = 5

        self.assertEqual(self.DUT.assess_plan_feasibility(),
                         [0.4090909090909091, 0.7333333333333333, -1, 4])
        self.assertEqual(self.DUT.lst_p_tpu,
                         [200.0, 300.0, 625.0, 500.0, 1000.0])
        self.assertEqual(self.DUT.lst_p_tpupw,
                         [19.17808219178082, 35.0, 56.81818181818182,
                          57.37704918032787, 0.0])

    @attr(all=True, unit=True)
    def test18_estimate_crow_amsaa_exact(self):
        """
        (TestGrowth) estimate_crow_amsaa should return False using exact failure times
        """

        # For example data, see http://www.reliawiki.org/index.php/Crow-AMSAA_%28NHPP%29#Example_-_Parameter_Estimation
        self.DUT.dic_test_data = {0: [1, 719163, 0.0, 2.7, 1],
                                  1: [2, 719163, 0.0, 10.3, 1],
                                  2: [3, 719163, 0.0, 12.5, 1],
                                  3: [4, 719163, 0.0, 30.6, 1],
                                  4: [5, 719163, 0.0, 57.0, 1],
                                  5: [6, 719163, 0.0, 61.3, 1],
                                  6: [7, 719163, 0.0, 80.0, 1],
                                  7: [8, 719163, 0.0, 109.5, 1],
                                  8: [9, 719163, 0.0, 125.0, 1],
                                  9: [10, 719163, 0.0, 128.6, 1],
                                  10: [11, 719163, 0.0, 143.8, 1],
                                  11: [12, 719163, 0.0, 167.9, 1],
                                  12: [13, 719163, 0.0, 229.2, 1],
                                  13: [14, 719163, 0.0, 296.7, 1],
                                  14: [15, 719163, 0.0, 320.6, 1],
                                  15: [16, 719163, 0.0, 328.2, 1],
                                  16: [17, 719163, 0.0, 366.2, 1],
                                  17: [18, 719163, 0.0, 396.7, 1],
                                  18: [19, 719163, 0.0, 421.1, 1],
                                  19: [20, 719163, 0.0, 438.2, 1],
                                  20: [21, 719163, 0.0, 501.2, 1],
                                  21: [22, 719163, 0.0, 620.0, 1]}

        self.DUT.grouped = False

        self.assertFalse(self.DUT.estimate_crow_amsaa())
        self.assertEqual(self.DUT.alpha_hat, [0.32279203293521613,
                                              0.42394221488057504,
                                              0.52924893703956533])
        self.assertEqual(self.DUT.beta_hat, [0.51077399351295227,
                                             0.6142103999317297,
                                             0.8474287960726461])

    @attr(all=True, unit=True)
    def test18a_estimate_crow_amsaa_grouped(self):
        """
        (TestGrowth) estimate_crow_amsaa should return False using grouped failure times
        """

        # For example data, see http://www.reliawiki.org/index.php/Crow-AMSAA_%28NHPP%29#Example_-_Parameter_Estimation
        self.DUT.dic_test_data = {0: [1, 719163, 0.0, 62.0, 12],
                                  1: [2, 719163, 0.0, 100.0, 6],
                                  2: [3, 719163, 62.0, 187.0, 15],
                                  3: [4, 719163, 187.0, 210.0, 3],
                                  4: [5, 719163, 210.0, 350.0, 18],
                                  5: [6, 719163, 350.0, 500.0, 16]}

        self.DUT.grouped = True

        self.assertFalse(self.DUT.estimate_crow_amsaa())
        self.assertEqual(self.DUT.alpha_hat, [0.38537715881590562,
                                              0.44585433767531873,
                                              0.50770467031237509])
        self.assertEqual(self.DUT.beta_hat, [0.7231246075396317,
                                             0.81360853965677293,
                                             0.95456866230721715])

    @attr(all=True, unit=True)
    def test19_calculate_crow_amsaa_mean(self):
        """
        (TestGrowth) calculate_crow_amsaa_mean should return False on success
        """

        self.DUT.dic_test_data = {0: [1, 719163, 0.0, 2.7, 1],
                                  1: [2, 719163, 0.0, 10.3, 1],
                                  2: [3, 719163, 0.0, 12.5, 1],
                                  3: [4, 719163, 0.0, 30.6, 1],
                                  4: [5, 719163, 0.0, 57.0, 1],
                                  5: [6, 719163, 0.0, 61.3, 1],
                                  6: [7, 719163, 0.0, 80.0, 1],
                                  7: [8, 719163, 0.0, 109.5, 1],
                                  8: [9, 719163, 0.0, 125.0, 1],
                                  9: [10, 719163, 0.0, 128.6, 1],
                                  10: [11, 719163, 0.0, 143.8, 1],
                                  11: [12, 719163, 0.0, 167.9, 1],
                                  12: [13, 719163, 0.0, 229.2, 1],
                                  13: [14, 719163, 0.0, 296.7, 1],
                                  14: [15, 719163, 0.0, 320.6, 1],
                                  15: [16, 719163, 0.0, 328.2, 1],
                                  16: [17, 719163, 0.0, 366.2, 1],
                                  17: [18, 719163, 0.0, 396.7, 1],
                                  18: [19, 719163, 0.0, 421.1, 1],
                                  19: [20, 719163, 0.0, 438.2, 1],
                                  20: [21, 719163, 0.0, 501.2, 1],
                                  21: [22, 719163, 0.0, 620.0, 1]}

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
        self.assertEqual(self.DUT.cum_mean[3], [4.8432788731340963,
                                                8.828139974276127,
                                                16.120046994855421])
        self.assertAlmostEqual(self.DUT.instantaneous_mean[0][1], 5.6336754)

    @attr(all=True, unit=True)
    def test20_calculate_cramer_vonmises_typei(self):
        """
        (TestGrowth) calculate_cramer_vonmises should return False on success with Type I (time terminated) data
        """

        self.DUT.dic_test_data = {0: [1, 719163, 0.0, 2.7, 1],
                                  1: [2, 719163, 0.0, 10.3, 1],
                                  2: [3, 719163, 0.0, 12.5, 1],
                                  3: [4, 719163, 0.0, 30.6, 1],
                                  4: [5, 719163, 0.0, 57.0, 1],
                                  5: [6, 719163, 0.0, 61.3, 1],
                                  6: [7, 719163, 0.0, 80.0, 1],
                                  7: [8, 719163, 0.0, 109.5, 1],
                                  8: [9, 719163, 0.0, 125.0, 1],
                                  9: [10, 719163, 0.0, 128.6, 1],
                                  10: [11, 719163, 0.0, 143.8, 1],
                                  11: [12, 719163, 0.0, 167.9, 1],
                                  12: [13, 719163, 0.0, 229.2, 1],
                                  13: [14, 719163, 0.0, 296.7, 1],
                                  14: [15, 719163, 0.0, 320.6, 1],
                                  15: [16, 719163, 0.0, 328.2, 1],
                                  16: [17, 719163, 0.0, 366.2, 1],
                                  17: [18, 719163, 0.0, 396.7, 1],
                                  18: [19, 719163, 0.0, 421.1, 1],
                                  19: [20, 719163, 0.0, 438.2, 1],
                                  20: [21, 719163, 0.0, 501.2, 1],
                                  21: [22, 719163, 0.0, 620.0, 1]}

        self.DUT.beta_hat = [0.51077399351295227,
                             0.6142103999317297,
                             0.8474287960726461]

        self.assertFalse(self.DUT.calculate_cramer_vonmises(t_star=650.0,
                                                            type2=False))
        self.assertAlmostEqual(self.DUT.cramer_vonmises, 0.03383013)

    @attr(all=True, unit=True)
    def test20a_calculate_cramer_vonmises_typeii(self):
        """
        (TestGrowth) calculate_cramer_vonmises should return False on success with Type II (failure terminated) data
        """

        self.DUT.dic_test_data = {0: [1, 719163, 0.0, 2.7, 1],
                                  1: [2, 719163, 0.0, 10.3, 1],
                                  2: [3, 719163, 0.0, 12.5, 1],
                                  3: [4, 719163, 0.0, 30.6, 1],
                                  4: [5, 719163, 0.0, 57.0, 1],
                                  5: [6, 719163, 0.0, 61.3, 1],
                                  6: [7, 719163, 0.0, 80.0, 1],
                                  7: [8, 719163, 0.0, 109.5, 1],
                                  8: [9, 719163, 0.0, 125.0, 1],
                                  9: [10, 719163, 0.0, 128.6, 1],
                                  10: [11, 719163, 0.0, 143.8, 1],
                                  11: [12, 719163, 0.0, 167.9, 1],
                                  12: [13, 719163, 0.0, 229.2, 1],
                                  13: [14, 719163, 0.0, 296.7, 1],
                                  14: [15, 719163, 0.0, 320.6, 1],
                                  15: [16, 719163, 0.0, 328.2, 1],
                                  16: [17, 719163, 0.0, 366.2, 1],
                                  17: [18, 719163, 0.0, 396.7, 1],
                                  18: [19, 719163, 0.0, 421.1, 1],
                                  19: [20, 719163, 0.0, 438.2, 1],
                                  20: [21, 719163, 0.0, 501.2, 1],
                                  21: [22, 719163, 0.0, 620.0, 1]}

        self.DUT.beta_hat = [0.51077399351295227,
                             0.6142103999317297,
                             0.8474287960726461]

        self.assertFalse(self.DUT.calculate_cramer_vonmises())
        self.assertAlmostEqual(self.DUT.cramer_vonmises, 0.04488069)

    @attr(all=True, unit=True)
    def test21_calculate_chi_square_exact_failure_terminated(self):
        """
        (TestGrowth) calculate_chi_square should return False on success with exact data
        """

        self.DUT.dic_test_data = {0: [1, 719163, 0.0, 2.7, 1],
                                  1: [2, 719163, 0.0, 10.3, 1],
                                  2: [3, 719163, 0.0, 12.5, 1],
                                  3: [4, 719163, 0.0, 30.6, 1],
                                  4: [5, 719163, 0.0, 57.0, 1],
                                  5: [6, 719163, 0.0, 61.3, 1],
                                  6: [7, 719163, 0.0, 80.0, 1],
                                  7: [8, 719163, 0.0, 109.5, 1],
                                  8: [9, 719163, 0.0, 125.0, 1],
                                  9: [10, 719163, 0.0, 128.6, 1],
                                  10: [11, 719163, 0.0, 143.8, 1],
                                  11: [12, 719163, 0.0, 167.9, 1],
                                  12: [13, 719163, 0.0, 229.2, 1],
                                  13: [14, 719163, 0.0, 296.7, 1],
                                  14: [15, 719163, 0.0, 320.6, 1],
                                  15: [16, 719163, 0.0, 328.2, 1],
                                  16: [17, 719163, 0.0, 366.2, 1],
                                  17: [18, 719163, 0.0, 396.7, 1],
                                  18: [19, 719163, 0.0, 421.1, 1],
                                  19: [20, 719163, 0.0, 438.2, 1],
                                  20: [21, 719163, 0.0, 501.2, 1],
                                  21: [22, 719163, 0.0, 620.0, 1]}

        self.DUT.ttt = 620.0
        self.DUT.beta_hat = [0.51077399351295227,
                             0.6142103999317297,
                             0.8474287960726461]
        self.DUT.grouped = False
        self.DUT.confidence = 0.90
        self.DUT.test_termination_time = 0.0

        self.assertFalse(self.DUT.calculate_chi_square())
        self.assertAlmostEqual(self.DUT.chi_square, 71.6366900)
        self.assertAlmostEqual(self.DUT.chi2_critical_value[0], 58.1240377)
        self.assertAlmostEqual(self.DUT.chi2_critical_value[1], 28.1440495)

    @attr(all=True, unit=True)
    def test21a_calculate_chi_square_exact_time_terminated(self):
        """
        (TestGrowth) calculate_chi_square should return False on success with exact data
        """

        self.DUT.dic_test_data = {0: [1, 719163, 0.0, 2.7, 1],
                                  1: [2, 719163, 0.0, 10.3, 1],
                                  2: [3, 719163, 0.0, 12.5, 1],
                                  3: [4, 719163, 0.0, 30.6, 1],
                                  4: [5, 719163, 0.0, 57.0, 1],
                                  5: [6, 719163, 0.0, 61.3, 1],
                                  6: [7, 719163, 0.0, 80.0, 1],
                                  7: [8, 719163, 0.0, 109.5, 1],
                                  8: [9, 719163, 0.0, 125.0, 1],
                                  9: [10, 719163, 0.0, 128.6, 1],
                                  10: [11, 719163, 0.0, 143.8, 1],
                                  11: [12, 719163, 0.0, 167.9, 1],
                                  12: [13, 719163, 0.0, 229.2, 1],
                                  13: [14, 719163, 0.0, 296.7, 1],
                                  14: [15, 719163, 0.0, 320.6, 1],
                                  15: [16, 719163, 0.0, 328.2, 1],
                                  16: [17, 719163, 0.0, 366.2, 1],
                                  17: [18, 719163, 0.0, 396.7, 1],
                                  18: [19, 719163, 0.0, 421.1, 1],
                                  19: [20, 719163, 0.0, 438.2, 1],
                                  20: [21, 719163, 0.0, 501.2, 1],
                                  21: [22, 719163, 0.0, 620.0, 1]}

        self.DUT.ttt = 620.0
        self.DUT.beta_hat = [0.51077399351295227,
                             0.6142103999317297,
                             0.8474287960726461]
        self.DUT.grouped = False
        self.DUT.confidence = 0.90
        self.DUT.test_termination_time = 620.0

        self.assertFalse(self.DUT.calculate_chi_square())
        self.assertAlmostEqual(self.DUT.chi_square, 71.6366900)
        self.assertAlmostEqual(self.DUT.chi2_critical_value[0], 60.4808866)
        self.assertAlmostEqual(self.DUT.chi2_critical_value[1], 29.7874771)

    @attr(all=True, unit=True)
    def test21b_calculate_chi_square_grouped(self):
        """
        (TestGrowth) calculate_chi_square should return False on success with grouped data
        """

        self.DUT.dic_test_data = {0: [1, 719163, 0.0, 330.0, 12],
                                  1: [2, 719163, 330.0, 660.0, 6],
                                  2: [3, 719163, 660.0, 990.0, 7],
                                  3: [4, 719163, 990.0, 1320.0, 5],
                                  4: [5, 719163, 1320.0, 1650.0, 4],
                                  5: [6, 719163, 1650.0, 1980.0, 3],
                                  6: [7, 719163, 1980.0, 2310.0, 1],
                                  7: [8, 719163, 2310.0, 2640.0, 4],
                                  8: [9, 719163, 2640.0, 3000.0, 4]}

        self.DUT.ttt = 3000.0
        self.DUT.beta_hat = [0.7231246075396317,
                             0.81360853965677293,
                             0.95456866230721715]
        self.DUT.grouped = True
        self.DUT.confidence = 0.90

        self.assertFalse(self.DUT.calculate_chi_square())
        self.assertAlmostEqual(self.DUT.chi_square, 15.3965744)
        self.assertAlmostEqual(self.DUT.chi2_critical_value[0], 3.4895391)
        self.assertAlmostEqual(self.DUT.chi2_critical_value[1], 13.3615661)

    @attr(all=True, unit=True)
    def test22_assess_growth_rate(self):
        """
        (TestGrowth) assess_growth_rate should return False on success
        """

        self.DUT.dic_test_data = {0: [1, 719163, 0.0, 2.7, 1],
                                  1: [2, 719163, 0.0, 10.3, 1],
                                  2: [3, 719163, 0.0, 12.5, 1],
                                  3: [4, 719163, 0.0, 30.6, 1],
                                  4: [5, 719163, 0.0, 57.0, 1],
                                  5: [6, 719163, 0.0, 61.3, 1],
                                  6: [7, 719163, 0.0, 80.0, 1],
                                  7: [8, 719163, 0.0, 109.5, 1],
                                  8: [9, 719163, 0.0, 125.0, 1],
                                  9: [10, 719163, 0.0, 128.6, 1],
                                  10: [11, 719163, 0.0, 143.8, 1],
                                  11: [12, 719163, 0.0, 167.9, 1],
                                  12: [13, 719163, 0.0, 229.2, 1],
                                  13: [14, 719163, 0.0, 296.7, 1],
                                  14: [15, 719163, 0.0, 320.6, 1],
                                  15: [16, 719163, 0.0, 328.2, 1],
                                  16: [17, 719163, 0.0, 366.2, 1],
                                  17: [18, 719163, 0.0, 396.7, 1],
                                  18: [19, 719163, 0.0, 421.1, 1],
                                  19: [20, 719163, 0.0, 438.2, 1],
                                  20: [21, 719163, 0.0, 501.2, 1],
                                  21: [22, 719163, 0.0, 620.0, 1]}

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
