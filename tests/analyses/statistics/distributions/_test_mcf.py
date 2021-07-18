#!/usr/bin/env python -O
"""
This is the test class for testing Mean Cumulative Function module algorithms
and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.survival.TestMCF.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
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

# Standard Library Imports
import sys
import unittest
from functools import reduce
from os.path import dirname

# Third Party Imports
import numpy as np
from analyses.survival.MCF import *
from nose.plugins.attrib import attr
from survival.Record import Model as Record

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/ramstk",
)


__author__ = "Doyle Rowland"
__email__ = "doyle.rowland@reliaqual.com"
__organization__ = "ReliaQual Associates, LLC"
__copyright__ = 'Copyright 2015 Doyle "weibullguy" Rowland'


class TestMeanCumulativeFunction(unittest.TestCase):
    """
    Class for testing the MCF data model class.
    """

    @attr(all=True, unit=True)
    def test_format_data(self):
        """
        (TestMCF) format_data should return a dictionary of lists on success
        """

        _data = {}
        _assembly_id = [0, 0, 0, 0, 1, 1, 1]
        _fail_times = [56.7, 116.4, 152.1, 198.4, 233.3, 286.1, 322.9]
        _status = [1, 1, 1, 2, 1, 1, 2]
        _n_failures = [1, 1, 1, 1, 1, 2, 1]
        for i in range(len(_fail_times)):
            _record = Record()
            _record.assembly_id = _assembly_id[i]
            _record.right_interval = _fail_times[i]
            _record.status = _status[i]
            _record.n_failures = _n_failures[i]
            _data[i] = _record

        self.assertEqual(
            format_data(_data),
            {0: [56.7, 116.4, 152.1, "198.4+"], 1: [233.3, 286.1, 286.1, "322.9+"]},
        )

    @attr(all=True, unit=True)
    def test_d_matrix(self):
        """
        (TestMCF) d_matrix should return a numpy 1-D matrix of integers on success with censoring
        """

        _data = {1: [5, 8], 2: [], 3: [1, 8, 16]}
        _times = [1, 5, 8, 16]

        _d_matrix = d_matrix(_data, _times)
        self.assertTrue(
            np.array_equal(
                _d_matrix,
                [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [1.0, 0.0, 1.0], [0.0, 0.0, 1.0]],
            )
        )

    @attr(all=True, unit=True)
    def test_mcf_build_d_matrix_no_censoring(self):
        """
        (TestMCF) d-matrix should return a numpy 1-D matrix of integers on success with no censoring
        """

        _data = {1: [5, 8], 3: [1, 8, 16]}
        _times = reduce(lambda x, y: x + y, _data.values())
        _times = set([float(f) for f in _times if isinstance(f, int)])
        _times = sorted(list(_times))

        _d_matrix = d_matrix(_data, _times)
        self.assertTrue(
            np.array_equal(_d_matrix, [[0.0, 1.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
        )

    @attr(all=True, unit=True)
    def test_delta_matrix(self):
        """
        (TestMCF) delta_matrix should return a numpy 1-D matrix of integers on success with censoring
        """

        _data = {1: [5, 8, "12+"], 2: ["16+"], 3: [1, 8, 16, "20+"]}
        _times = [1, 5, 8, 16]

        _delta_matrix = delta_matrix(_data, _times)
        self.assertTrue(
            np.array_equal(
                _delta_matrix,
                [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [0.0, 1.0, 1.0]],
            )
        )

    @attr(all=True, unit=True)
    def test_delta_matrix_no_censoring(self):
        """
        (TestMCF) delta_matrix should return a numpy 1-D matrix of integers on success with no censoring
        """

        _data = {1: [5, 8], 3: [1, 8, 16]}
        _times = reduce(lambda x, y: x + y, _data.values())
        _times = set([float(f) for f in _times if isinstance(f, int)])
        _times = sorted(list(_times))

        _delta_matrix = delta_matrix(_data, _times)
        self.assertTrue(
            np.array_equal(
                _delta_matrix, [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [0.0, 1.0]]
            )
        )

    @attr(all=True, unit=True)
    def test_mcf_variance(self):
        """
        (TestMCF) mcf_variance should return a numpy 1-D matrix of floats
        """

        _data = {1: [5, 8, "12+"], 2: ["16+"], 3: [1, 8, 16, "20+"]}
        _times = reduce(lambda x, y: x + y, _data.values())
        _times = set([float(f) for f in _times if isinstance(f, int)])
        _times = sorted(list(_times))

        _d_matrix = d_matrix(_data, _times)
        _delta_matrix = delta_matrix(_data, _times)

        _delta_dot = _delta_matrix.sum(axis=1)
        _d_dot = _d_matrix.sum(axis=1)

        _d_bar = _d_dot / _delta_dot

        _variance = mcf_variance(_delta_matrix, _d_matrix, _delta_dot, _d_bar)
        self.assertTrue(
            np.allclose(_variance, [[0.07407407], [0.07407407], [0.07407407], [0.125]])
        )

    @attr(all=True, unit=True)
    def test_mean_cumulative_function(self):
        """
        (TestMCF) mean_cumulative_function should return a numpy matrix on success
        """

        _data = {1: [5, 8, "12+"], 2: ["16+"], 3: [1, 8, 16, "20+"]}

        _mcf = mean_cumulative_function(_data)
        self.assertTrue(
            np.allclose(
                _mcf,
                [
                    [1.0, 1.0, 0.13030615, 0.33333333, 0.85269279],
                    [5.0, 1.0, 0.41682314, 0.66666667, 1.06626625],
                    [8.0, 2.0, 1.05429046, 1.33333333, 1.6862315],
                    [16.0, 1.0, 1.46857718, 1.83333333, 2.28868537],
                ],
            )
        )

    @attr(all=True, unit=True)
    def test_mil_handbook(self):
        """
        (TestMCF) mil_handbook should return a float value on success
        """

        # Data is U.S.S Halfbeak Number 4 Main Propulsion Diesel Engine
        # unscheduled maintenance action times from Meeker and Escobar.
        _times = [
            1.382,
            2.990,
            4.124,
            6.827,
            7.472,
            7.567,
            8.845,
            9.450,
            9.794,
            10.848,
            11.993,
            12.300,
            15.413,
            16.497,
            17.352,
            17.632,
            18.122,
            19.067,
            19.172,
            19.299,
            19.360,
            19.686,
            19.940,
            19.944,
            20.121,
            20.132,
            20.431,
            20.525,
            21.057,
            21.061,
            21.309,
            21.310,
            21.378,
            21.391,
            21.456,
            21.461,
            21.603,
            21.658,
            21.688,
            21.750,
            21.815,
            21.820,
            21.822,
            21.888,
            21.930,
            21.943,
            21.946,
            22.181,
            22.311,
            22.634,
            22.635,
            22.669,
            22.691,
            22.846,
            22.947,
            23.149,
            23.305,
            23.491,
            23.526,
            23.774,
            23.791,
            23.822,
            24.006,
            24.286,
            25.000,
            25.010,
            25.048,
            25.268,
            25.400,
            25.500,
            25.518,
        ]

        _mil_hdbk = mil_handbook(_times)
        self.assertAlmostEqual(_mil_hdbk, 51.4429465)

    @attr(all=True, unit=True)
    def test_laplace(self):
        """
        (TestMCF) laplace should return a float value on success
        """

        # Data is U.S.S Halfbeak Number 4 Main Propulsion Diesel Engine
        # unscheduled maintenance action times from Meeker and Escobar.
        _times = [
            1.382,
            2.990,
            4.124,
            6.827,
            7.472,
            7.567,
            8.845,
            9.450,
            9.794,
            10.848,
            11.993,
            12.300,
            15.413,
            16.497,
            17.352,
            17.632,
            18.122,
            19.067,
            19.172,
            19.299,
            19.360,
            19.686,
            19.940,
            19.944,
            20.121,
            20.132,
            20.431,
            20.525,
            21.057,
            21.061,
            21.309,
            21.310,
            21.378,
            21.391,
            21.456,
            21.461,
            21.603,
            21.658,
            21.688,
            21.750,
            21.815,
            21.820,
            21.822,
            21.888,
            21.930,
            21.943,
            21.946,
            22.181,
            22.311,
            22.634,
            22.635,
            22.669,
            22.691,
            22.846,
            22.947,
            23.149,
            23.305,
            23.491,
            23.526,
            23.774,
            23.791,
            23.822,
            24.006,
            24.286,
            25.000,
            25.010,
            25.048,
            25.268,
            25.400,
            25.500,
            25.518,
        ]
        _N = 71

        _zlp = laplace(_times, _N)
        self.assertAlmostEqual(_zlp, 7.5960410)

    @attr(all=True, unit=True)
    def test_lewis_robinson(self):
        """
        (TestMCF) lewis_robinson should return a float value on success
        """

        # Data is U.S.S Halfbeak Number 4 Main Propulsion Diesel Engine
        # unscheduled maintenance action times from Meeker and Escobar.
        _times = [
            1.382,
            2.990,
            4.124,
            6.827,
            7.472,
            7.567,
            8.845,
            9.450,
            9.794,
            10.848,
            11.993,
            12.300,
            15.413,
            16.497,
            17.352,
            17.632,
            18.122,
            19.067,
            19.172,
            19.299,
            19.360,
            19.686,
            19.940,
            19.944,
            20.121,
            20.132,
            20.431,
            20.525,
            21.057,
            21.061,
            21.309,
            21.310,
            21.378,
            21.391,
            21.456,
            21.461,
            21.603,
            21.658,
            21.688,
            21.750,
            21.815,
            21.820,
            21.822,
            21.888,
            21.930,
            21.943,
            21.946,
            22.181,
            22.311,
            22.634,
            22.635,
            22.669,
            22.691,
            22.846,
            22.947,
            23.149,
            23.305,
            23.491,
            23.526,
            23.774,
            23.791,
            23.822,
            24.006,
            24.286,
            25.000,
            25.010,
            25.048,
            25.268,
            25.400,
            25.500,
            25.518,
        ]
        _N = 71

        _zlr = lewis_robinson(_times, _N)
        self.assertAlmostEqual(_zlr, 4.7370351)

    @attr(all=True, unit=True)
    def test_serial_correlation(self):
        """
        (TestMCF) serial_correlation should return a float value on success
        """

        # Data is U.S.S Halfbeak Number 4 Main Propulsion Diesel Engine
        # unscheduled maintenance action times from Meeker and Escobar.
        _times = [
            1.382,
            2.990,
            4.124,
            6.827,
            7.472,
            7.567,
            8.845,
            9.450,
            9.794,
            10.848,
            11.993,
            12.300,
            15.413,
            16.497,
            17.352,
            17.632,
            18.122,
            19.067,
            19.172,
            19.299,
            19.360,
            19.686,
            19.940,
            19.944,
            20.121,
            20.132,
            20.431,
            20.525,
            21.057,
            21.061,
            21.309,
            21.310,
            21.378,
            21.391,
            21.456,
            21.461,
            21.603,
            21.658,
            21.688,
            21.750,
            21.815,
            21.820,
            21.822,
            21.888,
            21.930,
            21.943,
            21.946,
            22.181,
            22.311,
            22.634,
            22.635,
            22.669,
            22.691,
            22.846,
            22.947,
            23.149,
            23.305,
            23.491,
            23.526,
            23.774,
            23.791,
            23.822,
            24.006,
            24.286,
            25.000,
            25.010,
            25.048,
            25.268,
            25.400,
            25.500,
            25.518,
        ]
        _N = 71

        _rho = serial_correlation(_times, _N)
        self.assertAlmostEqual(_rho, 3.6684394)
