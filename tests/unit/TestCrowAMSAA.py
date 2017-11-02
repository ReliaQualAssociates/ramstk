#!/usr/bin/env python -O
"""
This is the test class for testing Crow-AMSAA model algorithms.
"""

# -*- coding: utf-8 -*-
#
#       tests.statistics.TestCrowAMSAA.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from analyses.statistics.growth.CrowAMSAA import calculate_average_mtbf, \
                                                 calculate_cramer_vonmises, \
                                                 calculate_crow_amsaa_chi_square, \
                                                 calculate_crow_amsaa_mean, \
                                                 calculate_crow_amsaa_parameters, \
                                                 calculate_final_mtbf, \
                                                 calculate_growth_rate, \
                                                 calculate_initial_mtbf, \
                                                 calculate_n_failures, \
                                                 calculate_t1, \
                                                 calculate_total_time, \
                                                 cramer_vonmises_critical_value

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestCrowAMSAA(unittest.TestCase):
    """
    Class for testing the Crow-AMSAA model functions.
    """

    @attr(all=True, unit=True)
    def test00_calculate_initial_mtbf_program(self):
        """
        (TestCrowAMSAA) calculate_initial_mtbf should return a float value on success
        """

        _mtbfi = calculate_initial_mtbf(0.23, 110.0, 10000.0, 1000.0)
        self.assertAlmostEqual(_mtbfi, 49.8750576)

    @attr(all=True, unit=True)
    def test00a_calculate_initial_mtbf_program_zero_mtbfg(self):
        """
        (TestCrowAMSAA) calculate_initial_mtbf should return 0.0 when no goal MTBF is specified
        """

        _mtbfi = calculate_initial_mtbf(0.23, 0.0, 10000.0, 1000.0)
        self.assertAlmostEqual(_mtbfi, 0.0)

    @attr(all=True, unit=True)
    def test00b_calculate_initial_mtbf_program_zero_ttt(self):
        """
        (TestCrowAMSAA) calculate_initial_mtbf should return 0.0 when no total time on test is specified
        """

        _mtbfi = calculate_initial_mtbf(0.23, 110.0, 0.0, 1000.0)
        self.assertAlmostEqual(_mtbfi, 0.0)

    @attr(all=True, unit=True)
    def test00c_calculate_initial_mtbf_program_zero_t1(self):
        """
        (TestCrowAMSAA) calculate_initial_mtbf should return 0.0 when no first phase test time is specified
        """

        _mtbfi = calculate_initial_mtbf(0.23, 110.0, 10000.0, 0.0)
        self.assertAlmostEqual(_mtbfi, 0.0)

    @attr(all=True, unit=True)
    def test01_calculate_final_mtbf_program(self):
        """
        (TestCrowAMSAA) calculate_final_mtbf should return a float value on success
        """

        _mtbff = calculate_final_mtbf(0.23, 50.0, 10000.0, 1000.0)
        self.assertAlmostEqual(_mtbff, 110.2755618)

    @attr(all=True, unit=True)
    def test01a_calculate_final_mtbf_program_zero_growth_rate(self):
        """
        (TestCrowAMSAA) calculate_final_mtbf should return the average MTBF when a zero growth rate is passed
        """

        _mtbff = calculate_final_mtbf(0.0, 50.0, 10000.0, 1000.0)
        self.assertAlmostEqual(_mtbff, 50.0)

    @attr(all=True, unit=True)
    def test01b_calculate_final_mtbf_program_unity_growth_rate(self):
        """
        (TestCrowAMSAA) calculate_final_mtbf should return the average MTBF when a growth rate equal to one is passed
        """

        _mtbff = calculate_final_mtbf(1.0, 50.0, 10000.0, 1000.0)
        self.assertAlmostEqual(_mtbff, 0.0)

    @attr(all=True, unit=True)
    def test01c_calculate_final_mtbf_program_zero_mtbfa(self):
        """
        (TestCrowAMSAA) calculate_final_mtbf should return 0.0 when a zero MTBFA is passed
        """

        _mtbff = calculate_final_mtbf(0.23, 0.0, 10000.0, 1000.0)
        self.assertAlmostEqual(_mtbff, 0.0)

    @attr(all=True, unit=True)
    def test01d_calculate_final_mtbf_program_zero_ttt(self):
        """
        (TestCrowAMSAA) calculate_final_mtbf should return 0.0 when a zero ttt is passed
        """

        _mtbff = calculate_final_mtbf(0.23, 50.0, 0.0, 1000.0)
        self.assertAlmostEqual(_mtbff, 0.0)

    @attr(all=True, unit=True)
    def test01e_calculate_final_mtbf_program_zero_t1(self):
        """
        (TestCrowAMSAA) calculate_final_mtbf should return 0.0 when a zero first phase test time is passed
        """

        _mtbff = calculate_final_mtbf(0.23, 50.0, 10000.0, 0.0)
        self.assertAlmostEqual(_mtbff, 0.0)

    @attr(all=True, unit=True)
    def test01f_calculate_final_mtbf_phases(self):
        """
        (TestCrowAMSAA) calculate_final_mtbf should return a float value when calculating the final MTBF for a test phase
        """

        _mtbff2 = calculate_final_mtbf(0.23, 50.0, 2500.0, 1000.0)
        _mtbff3 = calculate_final_mtbf(0.23, 50.0, 5000.0, 1000.0)
        _mtbff4 = calculate_final_mtbf(0.23, 50.0, 7000.0, 1000.0)
        _mtbff5 = calculate_final_mtbf(0.23, 50.0, 10000.0, 1000.0)
        self.assertAlmostEqual(_mtbff2, 80.1688181)
        self.assertAlmostEqual(_mtbff3, 94.0247917)
        self.assertAlmostEqual(_mtbff4, 101.5902031)
        self.assertAlmostEqual(_mtbff5, 110.2755618)

    @attr(all=True, unit=True)
    def test02_calculate_failures(self):
        """
        (TestCrowAMSAA) calculate_n_failures should return a float value when calculating the expected number of failures for a test phase
        """

        _cum_failures = 0.0
        _n_failures1 = calculate_n_failures(0.23, 50.0, 1000.0, 1000.0, 0)
        _cum_failures += _n_failures1
        _n_failures2 = calculate_n_failures(0.23, 50.0, 2500.0, 1000.0,
                                            _cum_failures)
        _cum_failures += _n_failures2
        _n_failures3 = calculate_n_failures(0.23, 50.0, 5000.0, 1000.0,
                                            _cum_failures)
        _cum_failures += _n_failures3
        _n_failures4 = calculate_n_failures(0.23, 50.0, 7000.0, 1000.0,
                                            _cum_failures)
        _cum_failures += _n_failures4
        _n_failures5 = calculate_n_failures(0.23, 50.0, 10000.0, 1000.0,
                                            _cum_failures)
        self.assertEqual(_n_failures1, 20.0)
        self.assertAlmostEqual(_n_failures2, 20.4989536)
        self.assertAlmostEqual(_n_failures3, 28.5626882)
        self.assertAlmostEqual(_n_failures4, 20.4244387)
        self.assertAlmostEqual(_n_failures5, 28.2826505)

    @attr(all=True, unit=True)
    def test02a_calculate_failures_zero_mtbfa(self):
        """
        (TestCrowAMSAA) calculate_n_failures should return 0.0 when calculating the expected number of failures and the average MTBF equals zero
        """

        _n_failures = calculate_n_failures(0.23, 0.0, 1000.0, 1000.0, 0)
        self.assertEqual(_n_failures, 0.0)

    @attr(all=True, unit=True)
    def test02b_calculate_failures_zero_t1(self):
        """
        (TestCrowAMSAA) calculate_n_failures should return 0.0 when calculating the expected number of failures and the first phase test time equals zero
        """

        _n_failures = calculate_n_failures(0.23, 50.0, 1000.0, 0.0, 0)
        self.assertEqual(_n_failures, 0.0)

    @attr(all=True, unit=True)
    def test03_calculate_average_mtbf_with_mtbf(self):
        """
        (TestCrowAMSAA) calculate_average_mtbf should return a float value when calculating the phase average MTBF using initial and final MTBF
        """

        _mtbfa = calculate_average_mtbf(0.0, 0.0, 45.0, 55.0)
        self.assertEqual(_mtbfa, 50.0)

    @attr(all=True, unit=True)
    def test03a_calculate_average_mtbf_with_time(self):
        """
        (TestCrowAMSAA) calculate_average_mtbf should return a float value when calculating the phase average MTBF using test time and expected number of failures
        """

        _mtbfa = calculate_average_mtbf(1000.0, 20.0, 0.0, 0.0)
        self.assertEqual(_mtbfa, 50.0)

    @attr(all=True, unit=True)
    def test03b_calculate_average_mtbf_zero_mtbfi(self):
        """
        (TestCrowAMSAA) calculate_average_mtbf should return 0.0 when calculating the phase average MTBF and initial MTBF equals zero
        """

        _mtbfa = calculate_average_mtbf(0.0, 0.0, 0.0, 55.0)
        self.assertEqual(_mtbfa, 0.0)

    @attr(all=True, unit=True)
    def test03c_calculate_average_mtbf_zero_mtbff(self):
        """
        (TestCrowAMSAA) calculate_average_mtbf should return 0.0 when calculating the phase average MTBF and final MTBF equals zero
        """

        _mtbfa = calculate_average_mtbf(0.0, 0.0, 45.0, 0.0)
        self.assertEqual(_mtbfa, 0.0)

    @attr(all=True, unit=True)
    def test03d_calculate_average_mtbf_zero_test_time(self):
        """
        (TestCrowAMSAA) calculate_average_mtbf should return 0.0 when calculating the phase average MTBF and the test time equals zero
        """

        _mtbfa = calculate_average_mtbf(0.0, 20, 0.0, 0.0)
        self.assertEqual(_mtbfa, 0.0)

    @attr(all=True, unit=True)
    def test03e_calculate_average_mtbf_zero_failures(self):
        """
        (TestCrowAMSAA) calculate_average_mtbf should return 0.0 when calculating the phase average MTBF and the number of failures equals zero
        """

        _mtbfa = calculate_average_mtbf(1000.0, 0.0, 0.0, 0)
        self.assertEqual(_mtbfa, 0.0)

    @attr(all=True, unit=True)
    def test04_calculate_total_time_program(self):
        """
        (TestCrowAMSAA) calculate_total_time should return an integer value when calculating the total test time for the overall test program
        """

        _ttt = calculate_total_time(0.23, 50.0, 110.0, 1000.0)
        self.assertEqual(_ttt, 9892)

    @attr(all=True, unit=True)
    def test04a_calculate_total_time_program_zero_alpha(self):
        """
        (TestCrowAMSAA) calculate_total_time should return 0.0 when calculating the total test time for the overall test program and the growth rate equals zero
        """

        _ttt = calculate_total_time(0.0, 50.0, 110.0, 1000.0)
        self.assertEqual(_ttt, 0.0)

    @attr(all=True, unit=True)
    def test04b_calculate_total_time_program_zero_mtbfa(self):
        """
        (TestCrowAMSAA) calculate_total_time should return 0.0 when calculating the total test time for the overall test program and average MTBF equals zero
        """

        _ttt = calculate_total_time(0.23, 0.0, 110.0, 1000.0)
        self.assertEqual(_ttt, 0.0)

    @attr(all=True, unit=True)
    def test04c_calculate_total_time_phases(self):
        """
        (TestCrowAMSAA) calculate_total_time should return a float value when calculating total test time for a single phase
        """

        _ttt2 = calculate_total_time(0.23, 50.0, 80.1688181, 1000.0)
        _ttt3 = calculate_total_time(0.23, 50.0, 94.0247917, 1000.0)
        _ttt4 = calculate_total_time(0.23, 50.0, 101.5902031, 1000.0)
        _ttt5 = calculate_total_time(0.23, 50.0, 110.0, 1000.0)
        self.assertEqual(_ttt2, 2500.0)
        self.assertEqual(_ttt3, 5000.0)
        self.assertEqual(_ttt4, 7001.0)
        self.assertEqual(_ttt5, 9892.0)

    @attr(all=True, unit=True)
    def test05_calculate_t1(self):
        """
        (TestCrowAMSAA) calculate_t1 should return a float value when calculating the minimum required test time for the first phase
        """

        _t1 = calculate_t1(0.23, 50.0, 110.0, 10000.0)
        self.assertEqual(_t1, 1011)

    @attr(all=True, unit=True)
    def test05a_calculate_t1_zero_alpha(self):
        """
        (TestCrowAMSAA) calculate_t1 should return 0.0 when calculating the minimum required test time for the first phase and the growth rate equals zero
        """

        _t1 = calculate_t1(0.0, 50.0, 110.0, 10000.0)
        self.assertEqual(_t1, 0)

    @attr(all=True, unit=True)
    def test05b_calculate_t1_zero_mtbfa(self):
        """
        (TestCrowAMSAA) calculate_t1 should return 0.0 when calculating the minimum required test time for the first phase and the average MTBF equals zero
        """

        _t1 = calculate_t1(0.23, 0.0, 110.0, 10000.0)
        self.assertEqual(_t1, 0)

    @attr(all=True, unit=True)
    def test06_calculate_growth_rate_program(self):
        """
        (TestCrowAMSAA) calculate_growth_rate should return a float value when calculating the average growth rate for the overall program
        """

        _alpha = calculate_growth_rate(50.0, 110.0, 10000.0, 1000.0)
        self.assertAlmostEqual(_alpha, 0.2306829)

    @attr(all=True, unit=True)
    def test06a_calculate_growth_rate_program_zero_mtbfa(self):
        """
        (TestCrowAMSAA) calculate_growth_rate should return 0.0 when calculating the average growth rate for the overall program and the average MTBF equals zero
        """

        _alpha = calculate_growth_rate(0.0, 110.0, 10000.0, 1000.0)
        self.assertEqual(_alpha, 0.0)

    @attr(all=True, unit=True)
    def test06b_calculate_growth_rate_program_zero_t1(self):
        """
        (TestCrowAMSAA) calculate_growth_rate should return 0.0 when calculating the average growth rate for the overall program and the first phase test time equals zero
        """

        _alpha = calculate_growth_rate(50.0, 110.0, 10000.0, 0.0)
        self.assertEqual(_alpha, 0.0)

    @attr(all=True, unit=True)
    def test06c_calculate_growth_rate_phases(self):
        """
        (TestCrowAMSAA) calculate_growth_rate should return a float value when calculating the average growth rate for a test phase
        """

        _alpha2 = calculate_growth_rate(50.0, 80.1688181, 2500.0, 1000.0)
        _alpha3 = calculate_growth_rate(50.0, 94.0247917, 5000.0, 1000.0)
        _alpha4 = calculate_growth_rate(50.0, 101.5902031, 7000.0, 1000.0)
        _alpha5 = calculate_growth_rate(50.0, 110.0, 10000.0, 1000.0)
        self.assertAlmostEqual(_alpha2, 0.2322887)
        self.assertAlmostEqual(_alpha3, 0.2317304)
        self.assertAlmostEqual(_alpha4, 0.2315471)
        self.assertAlmostEqual(_alpha5, 0.2306829)

    @attr(all=True, unit=True)
    def test07_calculate_crow_amsaa_parameters_exact(self):
        """
        (TestCrowAMSAA) calculate_crow_amsaa_parameters should return 0 when encountering no errors using exact failure times
        """

        # See http://reliawiki.org/index.php/Crow-AMSAA_%28NHPP%29 for example
        # data.
        n_failures = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1]
        fail_times = [2.7, 10.3, 12.5, 30.6, 57.0, 61.3, 80.0, 109.5, 125.0,
                      128.6, 143.8, 167.9, 229.2, 296.7, 320.6, 328.2, 366.2,
                      396.7, 421.1, 438.2, 501.2, 620.0]

        _alpha_hat, _beta_hat = calculate_crow_amsaa_parameters(n_failures,
                                                                fail_times)
        self.assertAlmostEqual(_alpha_hat, 0.4239422)
        self.assertAlmostEqual(_beta_hat, 0.6142104)

    @attr(all=True, unit=True)
    def test07_calculate_crow_amsaa_parameters_grouped(self):
        """
        (TestCrowAMSAA) calculate_crow_amsaa_parameters should return 0 when encountering no errors using grouped data
        """

        # See http://reliawiki.org/index.php/Crow-AMSAA_%28NHPP%29 for example
        # data.  (Helicopter example data)
        n_failures = [12, 6, 15, 3, 18, 16]
        fail_times = [62.0, 100.0, 187.0, 210.0, 350.0, 500.0]

        _alpha_hat, _beta_hat = calculate_crow_amsaa_parameters(n_failures,
                                                                fail_times,
                                                                grouped=True)
        self.assertAlmostEqual(_alpha_hat, 0.4458543)
        self.assertAlmostEqual(_beta_hat, 0.8136085)

    @attr(all=True, unit=True)
    def test08_calculate_crow_amsaa_parameters_no_failures(self):
        """
        (TestCrowAMSAA) calculate_crow_amsaa_parameters should return 1 when passed an empty list of failure counts
        """

        n_failures = []
        fail_times = [62.0, 100.0, 187.0, 210.0, 350.0, 500.0]

        _alpha_hat, _beta_hat = calculate_crow_amsaa_parameters(n_failures,
                                                                fail_times,
                                                                grouped=True)
        self.assertAlmostEqual(_alpha_hat, 0.0)
        self.assertAlmostEqual(_beta_hat, 0.0)

    @attr(all=True, unit=True)
    def test09_calculate_crow_amsaa_mean(self):
        """
        (TestCrowAMSAA) calculate_crow_amsaa_mean should return False
        """

        # See http://reliawiki.org/index.php/Crow-AMSAA_%28NHPP%29 for example
        # data.  (Helicopter example data)
        _time = 500.0
        _alpha = 0.44585
        _beta = 0.81361

        _cum_mean, _instantaneous_mean = calculate_crow_amsaa_mean(_time,
                                                                   _alpha,
                                                                   _beta)
        self.assertAlmostEqual(_cum_mean, 7.1428618)
        self.assertAlmostEqual(_instantaneous_mean, 8.7792208)

    @attr(all=True, unit=True)
    def test10_calculate_cramer_vonmises(self):
        """
        (TestCrowAMSAA) calculate_cramer_vonmises should return False
        """

        # See MIL-HDBK-189, 5.3.4, Example 1 for example data.
        n_failures = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1]
        fail_times = [2.4, 24.9, 52.5, 53.4, 54.7, 57.2, 118.6, 140.2, 185.0,
                      207.6, 293.9, 322.3, 365.9, 366.8, 544.8, 616.8, 627.5,
                      646.8, 664.0, 738.1, 764.7, 765.1, 779.6, 799.9, 852.9,
                      1116.3, 1161.1, 1257.1, 1276.3, 1308.9, 1340.3, 1437.3,
                      1482.0, 1489.9, 1715.1, 1828.9, 1971.5, 2303.4, 2429.7,
                      2457.4, 2535.2, 2609.9, 2674.2, 2704.8, 2849.6, 2923.5]
        beta = 0.616

        _Cvm = calculate_cramer_vonmises(n_failures, fail_times, beta, 3000.0,
                                         False)
        self.assertAlmostEqual(_Cvm, 0.04909242)

    @attr(all=True, unit=True)
    def test11_cramer_vonmises_critical_value_exact(self):
        """
        (TestCrowAMSAA) cramer_vonmises_critical_value should return the critical value when the degrees of freedom is a key
        """

        _Cvm = cramer_vonmises_critical_value(16, 90.0)
        self.assertAlmostEqual(_Cvm, 0.171)

    @attr(all=True, unit=True)
    def test12_cramer_vonmises_critical_value_interpolate_df(self):
        """
        (TestCrowAMSAA) cramer_vonmises_critical_value should return the critical value when the degrees of freedom is not a key
        """

        _Cvm = cramer_vonmises_critical_value(26, 90.0)
        self.assertAlmostEqual(_Cvm, 0.1725)

    @attr(all=True, unit=True)
    def test13_cramer_vonmises_critical_value_interpolate_confidence(self):
        """
        (TestCrowAMSAA) cramer_vonmises_critical_value should return the critical value when the confidence level is not a key
        """

        _Cvm = cramer_vonmises_critical_value(16, 75.0)
        self.assertAlmostEqual(_Cvm, 0.127)

    @attr(all=True, unit=True)
    def test14_calculate_crow_amsaa_chi_square_exact(self):
        """
        (TestCrowAMSAA) calculate_crow_amsaa_chi_square should return the chi-square test statistic when using exact data
        """

        # See MIL-HDBK-189, 5.3.5.1, Example 2 for example data.
        n_failures = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1]
        fail_times = [2.4, 24.9, 52.5, 53.4, 54.7, 57.2, 118.6, 140.2, 185.0,
                      207.6, 293.9, 322.3, 365.9, 366.8, 544.8, 616.8, 627.5,
                      646.8, 664.0, 738.1, 764.7, 765.1, 779.6, 799.9, 852.9,
                      1116.3, 1161.1, 1257.1, 1276.3, 1308.9, 1340.3, 1437.3,
                      1482.0, 1489.9, 1715.1, 1828.9, 1971.5, 2303.4, 2429.7,
                      2457.4, 2535.2, 2609.9, 2674.2, 2704.8, 2849.6, 2923.5]
        ttt = 3000.0
        beta = 0.616

        _chi_square = calculate_crow_amsaa_chi_square(n_failures, fail_times,
                                                      beta, ttt, False)
        self.assertAlmostEqual(_chi_square, 149.3506494)

    @attr(all=True, unit=True)
    def test14a_calculate_crow_amsaa_chi_square_grouped(self):
        """
        (TestCrowAMSAA) calculate_crow_amsaa_chi_square should return the chi-square test statistic when using grouped data
        """

        # See MIL-HDBK-189, 5.3.5.3, Example 3 for example data.
        n_failures = [12, 6, 7, 5, 4, 3, 1, 4, 4]
        fail_times = [330.0, 660.0, 990.0, 1320.0, 1650.0, 1980.0, 2310.0,
                      2640.0, 3000.0]
        ttt = 3000.0
        beta = 0.616

        _chi_square = calculate_crow_amsaa_chi_square(n_failures, fail_times,
                                                      beta, ttt)
        self.assertAlmostEqual(_chi_square, 15.3965744)
