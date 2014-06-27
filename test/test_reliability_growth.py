#!/usr/bin/env python -O
"""
This is the test class for testing reliability growth algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       test_calculations.py is part of The RTK Project
#
# All rights reserved.

import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from numpy import nan
from scipy.optimize import fsolve

from rtk._calculations_.growth import *


class TestGrowthPlanning(unittest.TestCase):
    """
    Class for testing the calculations used to construct reliability growth
    plans.
    """

    def test_initial_mtbf(self):
        """
        Method to test the calculation of the ideal growth curve initial MTBF.
        This uses the reliability growth plan found in MIL-HDBK-189, page 46,
        Case 2 as the test case.
        """

        # Test the calculation based on the model for the overall program
        # initial MTBF.
        self.assertAlmostEqual(initial_mtbf(10000.0, 1000.0, 110.0,
                                            0.23, 0.0, 1.0),
                               50.1207851)

        # Test the calculation based on probability for the overall program
        # initial MTBF.
        self.assertAlmostEqual(initial_mtbf(10000.0, 1000.0, 0.0,
                                            0.0, 0.15, 0.95),
                               50.0712301)

    def test_final_mtbf(self):
        """
        Method to test the calculation of the final MTBF.  This uses the
        reliability growth plan found in MIL-HDBK-189, page 46, Case 2 as the
        test case for growth phase tests.
        """

        # Test the final MTBF calculation for the overall program final MTBF.
        self.assertAlmostEqual(final_mtbf(10000.0, 1000.0, 50.0, 0.23),
                               109.7349131)

        # Test the final MTBF calculation for each test phase.
        self.assertAlmostEqual(final_mtbf(1000.0, 1000.0, 50.0, 0.23),
                               64.6167074)
        self.assertAlmostEqual(final_mtbf(2500.0, 1000.0, 50.0, 0.23),
                               79.7757739)
        self.assertAlmostEqual(final_mtbf(5000.0, 1000.0, 50.0, 0.23),
                               93.5638158)
        self.assertAlmostEqual(final_mtbf(7000.0, 1000.0, 50.0, 0.23),
                               101.0921361)
        self.assertAlmostEqual(final_mtbf(10000.0, 1000.0, 50.0, 0.23),
                               109.7349131)

    def test_average_mtbf(self):
        """
        Method to test the calculation of the average MTBF.
        """

        # Test the number of failures and average MTBF for each phase in Case 2
        # on page 46 in MIL-HDBK-189.
        self.assertEqual(average_mtbf(1000.0, 1000.0, 50.0, 0.23,
                                      0.0, 0.0),
                         (20.0, 50.0))
        self.assertEqual(average_mtbf(2500.0, 1000.0, 50.0, 0.23,
                                      1000.0, 20.0),
                         (20.498953614393976, 73.17446676628062))
        self.assertEqual(average_mtbf(5000.0, 1000.0, 50.0, 0.23,
                                      2500.0, 40.5),
                         (28.561641863448614, 87.52998206308799))
        self.assertEqual(average_mtbf(7000.0, 1000.0, 50.0, 0.23,
                                      5000.0, 69.1),
                         (20.386080525121073, 98.1061561851219))
        self.assertEqual(average_mtbf(10000.0, 1000.0, 50.0, 0.23,
                                      7000.0, 89.5),
                         (28.2687310711178, 106.12432487516584))

    def test_total_time(self):
        """
        Method to test the calculation of the total test time.  This uses the
        reliability growth plan found in MIL-HDBK-189, page 46, Case 2 as the
        test case.
        """

        # Test the total time calculation for the entire test program using
        # the model.
        self.assertAlmostEqual(total_time(1000.0, 50.0, 110.0, 0.23,
                                          0.0, 0, 0.0),
                               9891.8080028)

        # Test the total time calculation using the model.
        self.assertAlmostEqual(total_time(1000.0, 50.0, 50.0, 0.23,
                                          0.0, 0, 0.0),
                               1000.0000000)
        self.assertAlmostEqual(total_time(1000.0, 50.0, 80.2, 0.23,
                                          0.0, 0, 0.0),
                               2504.2304991)
        self.assertAlmostEqual(total_time(1000.0, 50.0, 94.0, 0.23,
                                          0.0, 0, 0.0),
                               4994.2705210)
        self.assertAlmostEqual(total_time(1000.0, 50.0, 101.6, 0.23,
                                          0.0, 0, 0.0),
                               7002.9354810)
        self.assertAlmostEqual(total_time(1000.0, 50.0, 110.3, 0.23,
                                          0.0, 0, 0.0),
                               10009.6387862)

        # Test the total time calculation using the average MTBF.
        self.assertAlmostEqual(total_time(0.0, 0.0, 0.0, 0.0,
                                          50.0, 20, 0.0),
                               1000.0000000)
        self.assertAlmostEqual(total_time(0.0, 0.0, 0.0, 0.0,
                                          73.2, 21, 1000.0),
                               2537.2000000)
        self.assertAlmostEqual(total_time(0.0, 0.0, 0.0, 0.0,
                                          87.5, 29, 2500.0),
                               5037.5000000)
        self.assertAlmostEqual(total_time(0.0, 0.0, 0.0, 0.0,
                                          97.9, 21, 5000.0),
                               7055.9000000)
        self.assertAlmostEqual(total_time(0.0, 0.0, 0.0, 0.0,
                                          106.1, 29, 7000.0),
                               10076.9000000)

    def test_minimum_first_phase_time(self):
        """
        Method to test the calculation of the minimum required first phase
        time.
        """

        # Calculate the minimum recommended test time for the first phase
        # based on the model.
        self.assertAlmostEqual(minimum_first_phase_time(10000.0, 110.0,
                                                        50.0, 0.23),
                               1010.9375351)

    def test_management_strategy(self):
        """
        Method to test the calculation of the minimum required average
        management strategy.
        """

        self.assertAlmostEqual(management_strategy(45.0, 140.0, 0.7),
                               0.9693878)

    def test_growth_rate(self):
        """
        Method to test the calculation of the minimum required average
        growth rate.  This uses the reliability growth plan found in
        MIL-HDBK-189, page 46, Case 2 as the test case.
        """

        # Calculate the average growth rate for the entire program.
        self.assertAlmostEqual(growth_rate(10000.0, 1000.0, 50.0, 110.0),
                               0.2306829)

        # Calculate the average growth rate for each test phase.
        self.assertAlmostEqual(growth_rate(1000.0, 1000.0, 45.0, 50.0),
                               0.1003277)

        self.assertAlmostEqual(growth_rate(1500.0, 1000.0, 50.0, 80.2),
                               0.3034331)

        self.assertAlmostEqual(growth_rate(2500.0, 1000.0, 80.2, 94.0),
                               0.0811358)

        self.assertAlmostEqual(growth_rate(2000.0, 1000.0, 94.0, 101.6),
                               0.0453133)

        self.assertAlmostEqual(growth_rate(3000.0, 1000.0, 101.6, 110.0),
                               0.0375167)

    def test_probability(self):
        """
        Method to test the calculation of the probability of seeing at least
        one failure.
        """

        self.assertAlmostEqual(prob(75.0, 45.0, 0.95),
                               0.7947103)

    def test_growth_potential(self):
        """
        Method to test the calculation of the growth potential MTBF.
        """

        self.assertAlmostEqual(growth_potential(45.0, 0.95, 0.7),
                               134.3283582)

    def test_idealized(self):
        """
        Function to test the calculation of ideal growth curve values.
        """

        # Test the idealized growth curve MTBF calculations.
        self.assertEqual(idealized_values(10.0, 2.0, 10.0, 0.23, mtbf=True),
                         [10.0, 10.0, nan, 14.256412877770796,
                          15.231622717297126, 16.033763625928838,
                          16.720419273729014, 17.323870356850943,
                          17.864179456360308, 18.354736450490236])

        # Test the idealized growth curve failure intensity calculations.
        self.assertEqual(idealized_values(10.0, 2.0, 10.0, 0.23, mtbf=False),
                         [0.1, 0.1, nan, 0.0701438719945634,
                         0.06565288666613267, 0.06236838856616672,
                         0.059807112706269976, 0.057723821490302106,
                         0.055977941916831954, 0.05448185010432503])


class TestGrowthAssessment(unittest.TestCase):
    """
    Class for testing reliability growth assessment models.
    """

    # Data used to test Duane model algorithms.  This is the data from
    # example #2 at http://www.reliawiki.org/index.php/Duane_Model
    DUANE_FAILS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                   1, 1, 1, 1]
    DUANE_TIMES = [9.2, 25, 61.5, 260, 300, 710, 916, 1010, 1220, 2530, 3350,
                   4200, 4410, 4990, 5570, 8310, 8530, 9200, 10500, 12100,
                   13400, 14600, 22000]

    # Data used to test Crow-AMSAA algorithms.
    # See http://www.reliawiki.org/index.php/Crow-AMSAA_%28NHPP%29#Example_-_Parameter_Estimation
    CROW_EXACT_FAILS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        1, 1, 1, 1]
    CROW_EXACT_TIMES = [2.7, 10.3, 12.5, 30.6, 57.0, 61.3, 80.0, 109.5, 125.0,
                        128.6, 143.8, 167.9, 229.2, 296.7, 320.6, 328.2, 366.2,
                        396.7, 421.1, 438.2, 501.2, 620.0]
    CROW_GROUP_FAILS = [12, 6, 15, 3, 18, 16]
    CROW_GROUP_TIMES = [62.0, 100.0, 187.0, 210.0, 350.0, 500.0]

    # Data used to test NHPP - Power Law and Duane algorithms.
    # See http://www.itl.nist.gov/div898/handbook/apr/section2/apr223.htm#Case%20Study%201:%20Reliability%20Improvement%20Test
    POWER_LAW_FAILS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    POWER_LAW_TIMES = [5, 40, 43, 175, 389, 712, 747, 795, 1299, 1478]

    def test_duane_model(self):
        """
        Method to test the Duane model algorithms.
        """

        # Check the value of the b (scale) and alpha (shape) parameter for
        # exact failure times using regression.
        self.assertAlmostEqual(duane_parameters(self.DUANE_FAILS,
                                                self.DUANE_TIMES)[0],
                               1.9149030)
        self.assertAlmostEqual(duane_parameters(self.DUANE_FAILS,
                                                self.DUANE_TIMES)[1],
                               0.6149699)

        # Check the value of the standard errors for b (scale) and alpha
        # (shape) parameters at 90%.
        self.assertAlmostEqual(duane_standard_error(self.DUANE_FAILS,
                                                    self.DUANE_TIMES,
                                                    1.9456631, 0.6132337)[0],
                               0.0076408)
        self.assertAlmostEqual(duane_standard_error(self.DUANE_FAILS,
                                                    self.DUANE_TIMES,
                                                    1.9456631, 0.6132337)[1],
                               0.0684070)
        self.assertAlmostEqual(duane_standard_error(self.DUANE_FAILS,
                                                    self.DUANE_TIMES,
                                                    1.9456631, 0.6132337)[2],
                               0.0087652)

        # Check the value of the cumulative and instantaneous means.
        self.assertAlmostEqual(duane_mean(1.9456631, 0.6132337, 22000)[0],
                               895.3391396)
        self.assertAlmostEqual(duane_mean(1.9456631, 0.6132337, 22000)[1],
                               2314.9357624)

    def test_crow_amsaa_model_exact_times(self):
        """
        Method to test the Crow-AMSAA model algorithms.
        """

        # Check the value of lambda and beta for exact failure times with a
        # failure terminated test.
        self.assertAlmostEqual(crow_amsaa_parameters(self.CROW_EXACT_FAILS,
                                                     self.CROW_EXACT_TIMES)[0],
                               0.4239422)
        self.assertAlmostEqual(crow_amsaa_parameters(self.CROW_EXACT_FAILS,
                                                     self.CROW_EXACT_TIMES)[1],
                               0.6142104)

    def test_crow_amsaa_model_grouped_times(self):
        """
        Test of the Crow-AMSAA parameter estimation function using
        grouped failure times.
        """

        _logT = [log(x) for x in self.CROW_GROUP_TIMES]
        _failures = np.array([0.0] + self.CROW_GROUP_FAILS)
        _times = np.array([0.0] + self.CROW_GROUP_TIMES)
        _logt = np.array([0.0] + _logT)

        self.assertAlmostEqual(fsolve(beta_grouped, 1.0,
                                      args=(_failures, _times, _logt))[0],
                               0.8136085)

        # Check the value of lambda and beta for grouped failure times.
        self.assertAlmostEqual(crow_amsaa_parameters(self.CROW_GROUP_FAILS,
                                                     self.CROW_GROUP_TIMES,
                                                     grouped=True)[0],
                               0.4458543)
        self.assertAlmostEqual(crow_amsaa_parameters(self.CROW_GROUP_FAILS,
                                                     self.CROW_GROUP_TIMES,
                                                     grouped=True)[1],
                               0.8136085)

#        self.assertAlmostEqual(crow_amsaa_parameters(self.CROW_GROUP_FAILS,
#                                                     self.CROW_GROUP_TIMES,
#                                                     grouped=False)[0],
#                               0.4458543)

        # Check the value of the cumulative and instantaneous means.
        self.assertAlmostEqual(crow_amsaa_mean(0.4239, 0.6142, 620)[0],
                               28.1865095)
        self.assertAlmostEqual(crow_amsaa_mean(0.4239, 0.6142, 620)[1],
                               45.8914188)

    def test_goodness_of_fits(self):
        """
        Method to test goodness of fit algorithms.
        """

        # Check the chi-square GoF statistic.
        self.assertAlmostEqual(crow_amsaa_chi_square(self.CROW_GROUP_FAILS,
                                                     self.CROW_GROUP_TIMES,
                                                     0.4458543, 0.8136085,
                                                     grouped=True),
                               0.6879676)

        # Check the Cramer-vonMises GoF statistics.
        self.assertAlmostEqual(cramer_von_mises(self.CROW_EXACT_TIMES,
                                                0.6142104),
                               0.0003027)   # Failure terminated test.

    def test_variance_covariance(self):
        """
        Test of the variance-covariance matrix function.
        """

        # Check the variance-covariance matrix for alpha (scale) and beta
        # (shape) parameters.
        self.assertAlmostEqual(var_covar(22, 620.0, 0.4239, 0.6142)[0][0],
                               0.1351777,
                               msg="FAIL: Scale parameter variance.")
        self.assertAlmostEqual(var_covar(22, 620.0, 0.4239, 0.6142)[1][1],
                               0.0171030,
                               msg="FAIL: Shape parameter variance.")
        self.assertAlmostEqual(var_covar(22, 620.0, 0.4239, 0.6142)[0][1],
                               -0.0466074,
                               msg="FAIL: Scale-shape parameter covariance.")


    def test_nhpp_power_law_regression_models(self):
        """
        Test of the NHPP - Power Law parameter estimation function using
        regression.
        """

        # Check the value of alpha (scale) and beta (shape) for exact failure
        # times using regression and 90% two-sided confidence bounds.
        self.assertEqual(power_law(self.DUANE_FAILS,
                                   self.DUANE_TIMES,
                                   2, fitmeth=2, conftype=3, alpha=0.90)[0],
                         [0.4588177906295521,
                          0.5139636320066449,
                          0.5757375158949376],
                         msg="FAIL: NHPP - Power Law alpha parameter exact "
                             "failure times using regression.")
        self.assertEqual(power_law(self.DUANE_FAILS,
                                   self.DUANE_TIMES,
                                   2, fitmeth=2, conftype=3, alpha=0.90)[1],
                         [0.59869079960521943,
                          0.6132337462228403,
                          0.62777669284046123],
                         msg="FAIL: NHPP - Power Law beta parameter exact "
                             "failure times using regression.")

    def test_nhpp_power_law_mle_model(self):
        """
        Test of the NHPP - Power Law parameter estimation function using MLE.
        """

        # Check the value of beta and alpha for exact failure times using MLE
        # and 90% two-sided confidence bounds.
        self.assertEqual(power_law(self.CROW_EXACT_FAILS,
                                   self.CROW_EXACT_TIMES,
                                   3, fitmeth=1, conftype=3, alpha=0.90)[0],
                         [0.13928340594382735,
                          0.42394221488057504,
                          1.2903690884062031],
                         msg="FAIL: NHPP - Power Law scale parameter exact "
                             "failure times using MLE.")

        self.assertEqual(power_law(self.CROW_EXACT_FAILS,
                                   self.CROW_EXACT_TIMES,
                                   3, fitmeth=1, conftype=3, alpha=0.90)[1],
                         [0.46736466889703443,
                          0.6142103999317297,
                          0.8071949817571866],
                         msg="FAIL: NHPP - Power Law shape parameter exact "
                             "failure times using MLE.")

        # Test that all zeros are returned when the wrong confidence type is
        # passed.


class TestFisherBounds(unittest.TestCase):
    """
    Class for testing functions used to calculate Crow confidence bounds.
    """

    def test_fisher_shape_parameter_bounds(self):
        """
        Test of the Fisher confidence bounds function for calculating the
        alpha % bounds on teh shape parameter.
        """

        # Check the 90% two-sided Fisher bounds on the shape parameter.
        self.assertAlmostEqual(fisher_bounds(0.6142, 0.0171030, 0.9)[0],
                               0.4675220,
                               msg="FAIL: Fisher shape parameter lower bound.")

        self.assertAlmostEqual(fisher_bounds(0.6142, 0.0171030, 0.9)[1],
                               0.8068960,
                               msg="FAIL: Fisher shape paramter upper bound.")

    def test_fisher_scale_parameter_bounds(self):
        """
        Test of the Fisher confidence bounds function for calculating the
        alpha % bounds on teh scale parameter.
        """

        # Check the 90% two-sided Fisher bounds on the scale parameter.
        self.assertAlmostEqual(fisher_bounds(0.4239, 0.0171030, 0.9)[0],
                               0.2854660,
                               msg="FAIL: Fisher scale parameter lower bound.")
        self.assertAlmostEqual(fisher_bounds(0.4239, 0.0171030, 0.9)[1],
                               0.6294662,
                               msg="FAIL: Fisher scale parameter upper bound.")

    def test_nhpp_cumulative_mean_variance(self):
        """
        Test of the function used to calculate the variance on the estimate of
        the NHPP cumulative mean.
        """

        self.assertAlmostEqual(nhpp_mean_variance(22, 620.0, 0.4239422,
                                                  0.6142104),
                               36.1006787)

    def test_fisher_cum_mean_bounds(self):
        """
        Test of the Fisher confidence bounds function for calculating the
        alpha % bounds for the cumulative MTBF.
        """

        self.assertAlmostEqual(fisher_bounds(28.1848929, 36.1006787, 0.9)[0],
                               21.4470736,
                               msg="FAIL: NHPP - Power Law cum. MTBF lower "
                                   "bound.")

        self.assertAlmostEqual(fisher_bounds(28.1848929, 36.1006787, 0.9)[1],
                               37.0394676,
                               msg="FAIL: NHPP - Power Law cum. MTBF upper "
                                   "bound.")

    def test_nhpp_instantaneous_mean_variance(self):
        """
        Test of the function used to calculate the variance on the estimate of
        the NHPP instantaneous mean.
        """

        self.assertAlmostEqual(nhpp_mean_variance(22, 620.0, 0.4239422,
                                                  0.6142104, metric=2),
                               191.3863557)

    def test_fisher_inst_mean_bounds(self):
        """
        Test of the Fisher confidence bounds function for calculating the
        alpha % bounds for the instantaneous MTBF.
        """

        self.assertAlmostEqual(fisher_bounds(45.8914188, 191.3863557, 0.9)[0],
                               31.1852952)

        self.assertAlmostEqual(fisher_bounds(45.8914188, 191.3863557, 0.9)[1],
                               67.5325441)


class TestCrowBounds(unittest.TestCase):
    """
    Class for testing functions used to calculate Crow confidence bounds.
    """

    def test_crow_shape_parameter_bounds(self):
        """
        Test of the Crow confidence bounds function for calculating the
        alpha % bounds on teh shape parameter.
        """

        # Check the Crow lower bound on the shape parameter.
        self.assertAlmostEqual(crow_bounds(22, 620.0, 0.4239422, 0.6142104,
                                           0.9, 1)[0],
                               0.4527382,
                               msg="FAIL: Crow shape parameter lower bound.")

        # Check the Crow upper bound on the shape parameter.
        self.assertAlmostEqual(crow_bounds(22, 620.0, 0.4239422, 0.6142104,
                                           0.9, 1)[1],
                               0.9350102,
                               msg="FAIL: Crow shape parameter upper bound.")

    def test_crow_scale_parameter_bounds(self):
        """
        Test of the Crow confidence bounds function for calculating the
        alpha % bounds on the scale parameter.
        """

        # Check the Crow lower bound on the scale parameter.
        self.assertAlmostEqual(crow_bounds(22, 620.0, 0.4239422, 0.6142104,
                                           0.9, 2)[0],
                               0.2870038,
                               msg="FAIL: Crow scale parameter lower bound.")

        # Check the Crow upper bound on the scale parameter.
        self.assertAlmostEqual(crow_bounds(22, 620.0, 0.4239422, 0.6142104,
                                           0.9, 2)[1],
                               0.5827364,
                               msg="FAIL: Crow scale parameter upper bound.")

    def test_crow_cun_failure_rate_bounds(self):
        """
        Test of the Crow confidence bounds function for calculating the
        alpha % bounds on the cumulative failure intensity.
        """

        # Check the Crow lower bound on cumulative failure intensity.
        self.assertAlmostEqual(crow_bounds(22, 620.0, 0.4239422, 0.6142104,
                                           0.9, 3)[0],
                               0.0240222)

        # Check the Crow upper bound on cumulative failure intensity.
        self.assertAlmostEqual(crow_bounds(22, 620.0, 0.4239422, 0.6142104,
                                           0.9, 3)[1],
                               0.0487749)

    def test_crow_inst_failure_rate_bounds(self):
        """
        Test of the Crow confidence bounds function for calculating the
        alpha % bounds on the instantaneous failure intensity.
        """

        # Check the Crow lower bound on instantaneous failure intensity.
        self.assertAlmostEqual(crow_bounds(22, 620.0, 0.0, 0.0, 0.9, 3)[0],
                               0.0240222)

        # Check the Crow upper bound on instantaneous failure intensity.
        self.assertAlmostEqual(crow_bounds(22, 620.0, 0.0, 0.0, 0.9, 3)[1],
                               0.0487749)


if __name__ == '__main__':
    unittest.main()
