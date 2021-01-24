# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.statistics.distributions.test_exponential.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test exponential distribution algorithms and models."""

# Third Party Imports
import numpy as np
import pytest
from scipy.stats import chi2

# RAMSTK Package Imports
from ramstk.analyses.statistics.distributions import exponential


class TestExponentialDistribution():
    """Class for testing the Exponential distribution data models."""

    # Data is the same as that used in the ReliaSoft wiki examples.
    # The table can be found at the following URL, for example.
    # http://reliawiki.org/index.php/The_Lognormal_Distribution#Rank_Regression_on_Y
    # lambda = 0.02711 and rho = -0.9679 when fit to the EXP.
    wiki_data = np.array([['', 0.0, 5.0, 0, 1, 1], ['', 0.0, 10.0, 0, 1, 1],
                          ['', 0.0, 15.0, 0, 1, 1], ['', 0.0, 20.0, 0, 1, 1],
                          ['', 0.0, 25.0, 0, 1, 1], ['', 0.0, 30.0, 0, 1, 1],
                          ['', 0.0, 35.0, 0, 1, 1], ['', 0.0, 40.0, 0, 1, 1],
                          ['', 0.0, 50.0, 0, 1, 1], ['', 0.0, 60.0, 0, 1, 1],
                          ['', 0.0, 70.0, 0, 1, 1], ['', 0.0, 80.0, 0, 1, 1],
                          ['', 0.0, 90.0, 0, 1, 1], ['', 0.0, 100.0, 0, 1, 1]])

    # Data set of 100 exponentially distributed points with a mean of 100.
    EXP_TEST = np.array([[0.0, 1.585, 1, 1, 1.585], [0.0, 1.978, 1, 1, 1.978],
                         [0.0, 2.81, 1, 1, 2.81], [0.0, 3.679, 1, 1, 3.679],
                         [0.0, 4.248, 1, 1, 4.248], [0.0, 5.137, 1, 1, 5.137],
                         [0.0, 5.566, 1, 1, 5.566], [0.0, 6.328, 1, 1, 6.328],
                         [0.0, 7.876, 1, 1, 7.876], [0.0, 10.79, 1, 1, 10.79],
                         [0.0, 12.398, 1, 1, 12.398],
                         [0.0, 13.095, 1, 1,
                          13.095], [0.0, 13.64, 1, 1, 13.64],
                         [0.0, 14.003, 1, 1, 14.003],
                         [0.0, 14.259, 1, 1, 14.259],
                         [0.0, 14.558, 1, 1, 14.558],
                         [0.0, 14.808, 1, 1, 14.808],
                         [0.0, 14.848, 1, 1, 14.848],
                         [0.0, 16.452, 1, 1, 16.452],
                         [0.0, 17.743, 1, 1, 17.743],
                         [0.0, 18.793, 1, 1, 18.793],
                         [0.0, 18.917, 1, 1, 18.917],
                         [0.0, 19.664, 1, 1, 19.664],
                         [0.0, 20.564, 1, 1, 20.564],
                         [0.0, 28.693, 1, 1, 28.693],
                         [0.0, 34.931, 1, 1, 34.931],
                         [0.0, 35.461, 1, 1, 35.461],
                         [0.0, 36.169, 1, 1, 36.169],
                         [0.0, 37.765, 1, 1, 37.367],
                         [0.0, 38.951, 1, 1, 38.951],
                         [0.0, 39.576, 1, 1,
                          39.576], [0.0, 40.36, 1, 1, 40.36],
                         [0.0, 41.559, 1, 1, 41.559],
                         [0.0, 42.486, 1, 1, 42.486],
                         [0.0, 46.984, 1, 1, 46.984],
                         [0.0, 48.146, 1, 1, 48.146],
                         [0.0, 48.398, 1, 1, 48.398],
                         [0.0, 49.315, 1, 1, 49.315],
                         [0.0, 49.364, 1, 1,
                          49.364], [0.0, 49.76, 1, 1, 49.76],
                         [0.0, 49.855, 1, 1, 49.855],
                         [0.0, 52.315, 1, 1, 52.315],
                         [0.0, 52.885, 1, 1, 52.885],
                         [0.0, 53.127, 1, 1, 53.127],
                         [0.0, 53.18, 1, 1, 53.18], [0.0, 54.07, 1, 1, 54.07],
                         [0.0, 58.595, 1, 1, 58.595],
                         [0.0, 61.993, 1, 1, 61.993],
                         [0.0, 65.542, 1, 1,
                          65.542], [0.0, 66.69, 1, 1, 66.69],
                         [0.0, 66.864, 1, 1, 66.864],
                         [0.0, 67.342, 1, 1, 67.342],
                         [0.0, 69.776, 1, 1, 69.776],
                         [0.0, 71.048, 1, 1, 71.048],
                         [0.0, 74.057, 1, 1, 74.057],
                         [0.0, 75.549, 1, 1, 75.549],
                         [0.0, 77.095, 1, 1, 77.095],
                         [0.0, 78.747, 1, 1, 78.747],
                         [0.0, 80.172, 1, 1,
                          80.172], [0.0, 82.16, 1, 1, 82.16],
                         [0.0, 82.223, 1, 1, 82.223],
                         [0.0, 86.769, 1, 1, 86.769],
                         [0.0, 87.229, 1, 1, 87.229],
                         [0.0, 88.862, 1, 1, 88.862],
                         [0.0, 89.103, 1, 1, 89.103],
                         [0.0, 94.072, 1, 1, 94.072],
                         [0.0, 96.415, 1, 1, 96.415],
                         [0.0, 101.977, 1, 1, 101.977],
                         [0.0, 111.147, 1, 1, 111.147],
                         [0.0, 115.532, 1, 1, 115.532],
                         [0.0, 120.144, 1, 1, 120.144],
                         [0.0, 121.963, 1, 1, 121.963],
                         [0.0, 134.763, 1, 1, 134.763],
                         [0.0, 137.072, 1, 1, 137.072],
                         [0.0, 141.988, 1, 1, 141.988],
                         [0.0, 143.687, 1, 1, 143.687],
                         [0.0, 143.918, 1, 1, 143.918],
                         [0.0, 148.07, 1, 1, 148.07],
                         [0.0, 158.98, 1, 1, 158.98],
                         [0.0, 159.732, 1, 1, 159.732],
                         [0.0, 163.827, 1, 1, 163.827],
                         [0.0, 169.175, 1, 1, 169.175],
                         [0.0, 171.813, 1, 1, 171.813],
                         [0.0, 172.663, 1, 1, 172.663],
                         [0.0, 177.992, 1, 1, 177.992],
                         [0.0, 184.263, 1, 1, 184.263],
                         [0.0, 185.254, 1, 1, 185.254],
                         [0.0, 194.039, 1, 1, 194.039],
                         [0.0, 212.279, 1, 1, 212.279],
                         [0.0, 222.93, 1, 1, 222.93],
                         [0.0, 226.918, 1, 1, 226.918],
                         [0.0, 241.044, 1, 1, 241.044],
                         [0.0, 263.548, 1, 1, 263.548],
                         [0.0, 275.491, 1, 1, 275.491],
                         [0.0, 294.418, 1, 1, 294.418],
                         [0.0, 297.467, 1, 1, 297.467],
                         [0.0, 317.922, 1, 1, 317.922],
                         [0.0, 323.763, 1, 1, 323.763],
                         [0.0, 350.577, 1, 1, 350.577],
                         [0.0, 351.347, 1, 1, 351.347]])

    # Data set of alpha particle interarrival times.  Data is from Table 7.1 in
    # Meeker and Escobar.
    ALPHA = np.array([[0.0, 100.0, 1609, 4, 50.0],
                      [100.0, 300.0, 2424, 4, 200.0],
                      [300.0, 500.0, 1770, 4, 400.0],
                      [500.0, 700.0, 1306, 4, 600.0],
                      [700.0, 1000.0, 1213, 4, 850.0],
                      [1000.0, 2000.0, 1528, 4, 1500.0],
                      [2000.0, 4000.0, 354, 4, 3000.0],
                      [4000.0, np.inf, 16, 2, np.inf]])

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_theoretical_distribution(self):
        """theoretical_distribution() should return a numpy array of floats on
        success."""
        _para = [0.0106235]

        _data = [x[1] for x in self.EXP_TEST]
        _probs = exponential.theoretical_distribution(np.array(_data), _para)
        np.testing.assert_almost_equal(_probs, [
            0.01669728, 0.02079404, 0.02941086, 0.03832994, 0.04412548,
            0.05311054, 0.05741615, 0.06501567, 0.08026591, 0.10830182,
            0.12340496, 0.12987181, 0.13489513, 0.13822483, 0.14056535,
            0.14329095, 0.14556324, 0.14592625, 0.16035645, 0.17179350,
            0.18098054, 0.18205874, 0.18852403, 0.19624570, 0.26274399,
            0.31001780, 0.31389180, 0.31903296, 0.33048150, 0.33886416,
            0.34323935, 0.34868668, 0.35693022, 0.36323208, 0.39294418,
            0.40039192, 0.40199499, 0.40779232, 0.40810052, 0.41058535,
            0.41117991, 0.42636869, 0.42983176, 0.43129571, 0.43161583,
            0.43696453, 0.46339015, 0.48241558, 0.50156667, 0.50760853,
            0.50851787, 0.51100731, 0.52348941, 0.52988523, 0.54467532,
            0.55183544, 0.55913595, 0.56680563, 0.57331415, 0.58223105,
            0.58251057, 0.60219386, 0.60413312, 0.61094146, 0.61193628,
            0.63189015, 0.64093963, 0.66154112, 0.69295782, 0.70693305,
            0.72094595, 0.72628666, 0.76108674, 0.76687591, 0.77873839,
            0.78269619, 0.78322880, 0.79258251, 0.81528183, 0.81675164,
            0.82455262, 0.83424270, 0.83882353, 0.84027239, 0.84906379,
            0.85879153, 0.86027036, 0.87272094, 0.89514176, 0.90635993,
            0.91024427, 0.92275174, 0.93917791, 0.94642532, 0.95618371,
            0.95758023, 0.96586542, 0.96791916, 0.97587134, 0.97606791
        ])

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_theoretical_distribution_zero_parameter(self):
        """theoretical_distribution() should return a numpy array of 0's on
        success when passed a parameter = 0.0."""
        _para = [0.0]

        _data = [x[1] for x in self.EXP_TEST]
        _probs = exponential.theoretical_distribution(np.array(_data), _para)
        np.testing.assert_almost_equal(_probs, [
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        ])

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_log_pdf(self):
        """log_pdf() should return a numpy array of floats on success."""
        data = np.array(self.wiki_data[:, 2], dtype=float)
        _log_pdf = exponential.log_pdf(data, 0.02222222, 0.0)

        np.testing.assert_allclose(_log_pdf, [
            -3.91777369, -4.02888479, -4.13999589, -4.25110699, -4.36221809,
            -4.47332919, -4.58444029, -4.69555139, -4.91777359, -5.13999579,
            -5.36221799, -5.58444019, -5.80666239, -6.02888459
        ])

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_log_pdf_positive_location(self):
        """log_pdf() should return a numpy array of floats on success when
        passed a positive valued location parameter."""
        data = np.array(self.wiki_data[:, 2], dtype=float)
        _log_pdf = exponential.log_pdf(data, 0.02222222, 10.0)

        np.testing.assert_allclose(_log_pdf, [
            -3.69555149, -3.80666259, -3.91777369, -4.02888479, -4.13999589,
            -4.25110699, -4.36221809, -4.47332919, -4.69555139, -4.91777359,
            -5.13999579, -5.36221799, -5.58444019, -5.80666239
        ])

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_log_pdf_negative_location(self):
        """log_pdf() should return a numpy array of floats on success when
        passed a negative valued location parameter."""
        data = np.array(self.wiki_data[:, 2], dtype=float)
        _log_pdf = exponential.log_pdf(data, 0.02222222, -10.0)

        np.testing.assert_allclose(_log_pdf, [
            -4.13999589, -4.25110699, -4.36221809, -4.47332919, -4.58444029,
            -4.69555139, -4.80666249, -4.91777359, -5.13999579, -5.36221799,
            -5.58444019, -5.80666239, -6.02888459, -6.25110679
        ])

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_log_pdf_negative_theta(self):
        """log_pdf() should return a numpy array of nan when passed a negative
        theta value."""
        data = np.array(self.wiki_data[:, 2], dtype=float)
        _log_pdf = exponential.log_pdf(data, -0.02222222, 0.0)

        np.testing.assert_allclose(_log_pdf, [
            np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
        ])

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_log_pdf_zero_theta(self):
        """log_pdf() should return a numpy array of nan when passed a negative
        theta value."""
        data = np.array(self.wiki_data[:, 2], dtype=float)
        _log_pdf = exponential.log_pdf(data, 0.0, 0.0)

        np.testing.assert_allclose(_log_pdf, -np.inf)

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_partial_derivatives_exact(self):
        """partial_derivatives() should return a float on success when passed
        an array of exact data."""

        # Leukemia remission times.  Data is from Example 7.2 of Lee and Wang.
        leukemia_data = np.array([[0.0, 1.0, 1, 1], [0.0, 1.0, 1, 1],
                                  [0.0, 2.0, 1, 1], [0.0, 2.0, 1, 1],
                                  [0.0, 3.0, 1, 1], [0.0, 4.0, 1, 1],
                                  [0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1],
                                  [0.0, 5.0, 1, 1], [0.0, 6.0, 1, 1],
                                  [0.0, 8.0, 1, 1], [0.0, 8.0, 1, 1],
                                  [0.0, 9.0, 1, 1], [0.0, 10.0, 1, 1],
                                  [0.0, 10.0, 1, 1], [0.0, 12.0, 1, 1],
                                  [0.0, 14.0, 1, 1], [0.0, 16.0, 1, 1],
                                  [0.0, 20.0, 1, 1], [0.0, 24.0, 1, 1],
                                  [0.0, 34.0, 1, 1]])

        _part_deriv = exponential.partial_derivatives(1.0, leukemia_data)
        assert _part_deriv == -177.0

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_partial_derivatives_right(self):
        """partial_derivatives() should return a float on success when passed
        an array of right-censored data."""

        # Cancerous mice data.  Data is from Example 7.3 in Lee and Wang.
        mice_data = np.array([[0.0, 4.0, 1, 1], [0.0, 5.0, 1, 1],
                              [0.0, 8.0, 1, 1], [0.0, 9.0, 1, 1],
                              [0.0, 10.0, 1, 1], [0.0, 10.0, 1, 2],
                              [0.0, 10.0, 1, 2], [0.0, 10.0, 1, 2],
                              [0.0, 10.0, 1, 2], [0.0, 10.0, 1, 2]])

        _part_deriv = exponential.partial_derivatives(1.0, mice_data)
        assert _part_deriv == -81.0

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_partial_derivatives_interval(self):
        """partial_derivatives() should return a float on success when passed
        an array of exact, right, and interval censored data."""
        # Danish AIDS patients.  Data retrieved from:
        # https://encrypted.google.com/books?id=Jwf3M6TtHTkC&pg=PA33&lpg=PA33&dq=exponential+data+set+example+with+interval+censoring&source=bl&ots=_VK8lx0yqP&sig=zbUtQTK8ZHR10Y5LDA_0aZz_OqI&hl=en&sa=X&ei=ekqwU8mWBtCGqgb204LwDw&ved=0CH4Q6AEwCQ#v=onepage&q=exponential%20data%20set%20example%20with%20interval%20censoring&f=false
        aids_data = np.array([[0.0, 24.0, 24, 3], [24.0, 39.0, 1, 3],
                              [24.0, 113.0, 4, 3], [28.0, 88.0, 1, 3],
                              [39.0, 113.0, 2, 3], [57.0, 113.0, 1, 3],
                              [0.0, 39.0, 2, 3], [24.0, 57.0, 10, 3],
                              [24.0, 28.0, 4, 3], [24.0, 88.0, 3, 3],
                              [28.0, 39.0, 4, 3], [39.0, 57.0, 3, 3],
                              [57.0, 88.0, 5, 3], [88.0, 113.0, 1, 3],
                              [0.0, 88.0, 34, 2], [0.0, 24.0, 61, 2],
                              [0.0, 28.0, 8, 2], [0.0, 39.0, 15, 2],
                              [0.0, 57.0, 22, 2], [0.0, 113.0, 92, 2]])

        # Parameter is 0.0034 for exponential.
        _part_deriv = exponential.partial_derivatives(0.0034, aids_data)
        assert _part_deriv == pytest.approx(-115.5080488)

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_log_likelihood_exact(self):
        """log_likelihood() should return a float on success when passed an
        array of exact data."""
        _log_like = exponential.log_likelihood(0.01062350, 0.0, self.EXP_TEST)

        assert _log_like == pytest.approx(-554.4686897933581)

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_log_likelihood_interval(self):
        """log_likelihood() should return a float on success when passed an
        array of interval censored data."""
        _log_like = exponential.log_likelihood(0.001062350, 0.0, self.ALPHA)

        assert _log_like == -np.inf

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_maximum_likelihood_estimate_exact_times(self):
        """mle() should return a numpy array of floats on success with exact
        failure times."""
        _fit = exponential.mle(self.EXP_TEST, 0.0, 10000000.0)

        # Check the mean for exact failure time data.
        assert _fit[0][0] == pytest.approx(0.01062350)

        # Check the variance for exact failure time data.
        assert _fit[1][0] == pytest.approx(1.1529539e-06)

        # Check the goodness of fit statistics for exact failure time data.
        assert _fit[2][0] == pytest.approx(-554.4686898)  # Log-likelihood
        assert _fit[2][1] == pytest.approx(1110.9373796)  # AIC
        assert _fit[2][2] == pytest.approx(1112.3978199)  # BIC

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_maximum_likelihood_estimate_interval_censored(self):
        """mle() should return a numpy array of floats on success with interval
        censored failure times."""
        _fit = exponential.mle(self.ALPHA, 0.0, 10000000.0)

        # Check the mean for interval censored failure time data.
        np.testing.assert_array_equal(_fit[0], [0.0016958399594908262, 0.0])

        # Check the variance for interval censored failure time data.
        np.testing.assert_array_equal(_fit[1],
                                      [4.1646989502606359e-07, 0.0, 0.0])

        # Check the goodness of fit for interval censored failure time data.
        assert _fit[2][0] == pytest.approx(6547.2989156)  # Log-likelihood
        assert _fit[2][1] == pytest.approx(-13092.5978312)  # AIC
        assert _fit[2][2] == pytest.approx(-13093.7966509)  # BIC

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_hazard_function(self):
        """hazard_function() should return a dict of lists of floats on
        success."""
        _parameters = [0.0101382, 0.0106235, 0.0113429]

        _hazard = exponential.hazard_function(_parameters, 0, 10, 1)
        assert _hazard == {
            0: _parameters,
            1: _parameters,
            2: _parameters,
            3: _parameters,
            4: _parameters,
            5: _parameters,
            6: _parameters,
            7: _parameters,
            8: _parameters,
            9: _parameters
        }

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_mean(self):
        """mean() should return a dict of lists of floats on success."""
        _para = [0.0101382, 0.0106235, 0.0113429]

        _hazard = exponential.mean(_para, 0, 10, 1)
        assert _hazard == {
            0: [88.1608759664636, 94.13093613215985, 98.63683888658737],
            1: [88.1608759664636, 94.13093613215985, 98.63683888658737],
            2: [88.1608759664636, 94.13093613215985, 98.63683888658737],
            3: [88.1608759664636, 94.13093613215985, 98.63683888658737],
            4: [88.1608759664636, 94.13093613215985, 98.63683888658737],
            5: [88.1608759664636, 94.13093613215985, 98.63683888658737],
            6: [88.1608759664636, 94.13093613215985, 98.63683888658737],
            7: [88.1608759664636, 94.13093613215985, 98.63683888658737],
            8: [88.1608759664636, 94.13093613215985, 98.63683888658737],
            9: [88.1608759664636, 94.13093613215985, 98.63683888658737]
        }

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_reliability_function(self):
        """reliability_function() should return a dict of lists of floats on
        success."""
        _para = [0.0101382, 0.0106235, 0.0113429]

        _reliability = exponential.reliability_function(_para, 0, 10, 1)
        assert _reliability == {
            0: [1.0, 1.0, 1.0],
            1: [0.98991301831630807, 0.98943273007988608, 0.98872118814618748],
            2: [0.97992778383210333, 0.97897712735333664, 0.97756958788920878],
            3: [0.97004327022524806, 0.9686320118029762, 0.9665437644333974],
            4: [0.9602584615260974, 0.95839621588099111, 0.95564229916587751],
            5: [0.95057235201307344, 0.94826858437736083, 0.94486378947404071],
            6: [0.9409839461092937, 0.93824797428948092, 0.93420684856508274],
            7: [0.93149225828024107, 0.92833325469316386, 0.92367010528757409],
            8: [0.92209631293246741, 0.91852330661500337, 0.91325220395504447],
            9: [0.91279514431331776, 0.90881702290608701, 0.90295180417155596]
        }

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_log_likelihood_ratio_exact(self):
        """log_likelihood_ratio() should return a float on success when passed
        an array of exact data."""
        _constant = chi2.ppf(0.95, 1) / 2.0
        _log_like_ratio = exponential.log_likelihood_ratio(
            0.01062350, 0.0, self.EXP_TEST, _constant)

        assert _log_like_ratio == pytest.approx(-556.3894192)

    @pytest.mark.unit
    @pytest.mark.calculation
    def test_likelihood_bounds_exact(self):
        """likelihood_bounds() should return a tuple of floats on success when
        passed an array of exact data."""
        _bounds = exponential.likelihood_bounds(0.01062350, 0.0, 0.90,
                                                self.EXP_TEST)

        assert _bounds[0] == pytest.approx(0.01062678)
        assert _bounds[1] == pytest.approx(0.01072973)
