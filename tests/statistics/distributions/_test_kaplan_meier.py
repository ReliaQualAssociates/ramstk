#!/usr/bin/env python -O
"""
This is the test class for testing Kaplan-Meier module algorithms
and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.survival.TestKaplanMeier.py is part of The RAMSTK Project
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

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import unittest
from nose.plugins.attrib import attr
import numpy as np

import dao.DAO as _dao
from analyses.survival.KaplanMeier import *
from survival.Record import Model as Record

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestKaplanMeier(unittest.TestCase):
    """
    Class for testing the KaplanMeier data model class.
    """

    @attr(all=True, unit=True)
    def test_format_data(self):
        """
        (TestKaplanMeier) format_data should return a dictionary of lists on success
        """

        _data = {}
        _assembly_id = [0, 0, 0, 0, 1, 1, 1]
        _fail_times = [56.7, 116.4, 152.1, 198.4, 233.3, 286.1, 322.9]
        _status = [0, 0, 0, 1, 0, 0, 1]
        _n_failures = [1, 1, 1, 1, 1, 2, 1]
        for i in range(len(_fail_times)):
            _record = Record()
            _record.assembly_id = _assembly_id[i]
            _record.right_interval = _fail_times[i]
            _record.status = _status[i]
            _record.n_failures = _n_failures[i]
            _data[i] = _record

        self.assertEqual(
            format_data(_data), ([(0, 0.0, 56.7, 0.0, 0, 1, 719163),
                                  (1, 0.0, 116.4, 0.0, 0, 1, 719163),
                                  (2, 0.0, 152.1, 0.0, 0, 1, 719163),
                                  (3, 0.0, 198.4, 0.0, 1, 1, 719163),
                                  (4, 0.0, 233.3, 0.0, 0, 1, 719163),
                                  (5, 0.0, 286.1, 0.0, 0, 2, 719163),
                                  (6, 0.0, 322.9, 0.0, 1, 1, 719163)], 6))

    @attr(all=True, unit=True)
    def test_kaplan_meier(self):
        """
        (TestKaplanMeier) kaplan_meier should return a numpy matrix of floats on success
        """

        # Data is from Lee and Wang, page 69, example 4.2.
        _data = [('', 3.0, 3.0, 0.0, u'Event',
                  1), ('', 4.0, 4.0, 0.0, u'Right Censored',
                       1), ('', 5.7, 5.7, 0.0, u'Right Censored',
                            1), ('', 6.5, 6.5, 0.0, u'Event',
                                 1), ('', 6.5, 6.5, 0.0, u'Event', 1),
                 ('', 8.4, 8.4, 0.0, u'Right Censored',
                  1), ('', 10.0, 10.0, 0.0, u'Event',
                       1), ('', 10.0, 10.0, 0.0, u'Right Censored',
                            1), ('', 12.0, 12.0, 0.0, u'Event',
                                 1), ('', 15.0, 15.0, 0.0, u'Event', 1)]

        _km = kaplan_meier(_data, 0.0, 100000.0)
        self.assertTrue(
            np.allclose(_km[0], [[3.0, 0.71671928, 0.9, 0.96722054], [
                4.0, 0.71671928, 0.9, 0.96722054
            ], [5.7, 0.71671928, 0.9, 0.96722054], [
                6.5, 0.41797166, 0.64285714, 0.79948773
            ], [8.4, 0.41797166, 0.64285714, 0.79948773], [
                10.0, 0.25976276, 0.48214286, 0.67381139
            ], [12.0, 0.06504527, 0.24107143, 0.47680147],
                                 [15.0, 0.0, 0.0, 0.0]]))

        self.assertTrue(np.allclose(_km[1], [1, 4, 5, 7, 9, 10]))

    @attr(all=True, unit=True)
    def test_kaplan_meier_mean(self):
        """
        (TestKaplanMeier) kaplan_meier_mean should return a numpy 1-D matrix of integers on success
        """

        # This data is the result of the executing the Kaplan-Meier function
        # using the data set from the previous test.
        _data = np.array([[3.0, 0.71671928, 0.9,
                           0.96722054], [4.0, 0.71671928, 0.9, 0.96722054], [
                               5.7, 0.71671928, 0.9, 0.96722054
                           ], [6.5, 0.41797166, 0.64285714, 0.79948773], [
                               8.4, 0.41797166, 0.64285714, 0.79948773
                           ], [10.0, 0.25976276, 0.48214286, 0.67381139],
                          [12.0, 0.06504527, 0.24107143,
                           0.47680147], [15.0, 0.0, 0.0, 0.0]])
        _rank = [1, 4, 5, 7, 9, 10]

        _km_mean = kaplan_meier_mean(_data, _rank, 0.9)
        self.assertTrue(
            np.allclose(_km_mean, [8.14115869673, 10.0875, 12.0338413033]))

    @attr(all=True, unit=True)
    def test_kaplan_meier_hazard(self):
        """
        (TestKaplanMeier) kaplan_meier_hazard should return a numpy matrix of floats on success
        """

        _data = np.array([[3.0, 0.71671928, 0.9,
                           0.96722054], [4.0, 0.71671928, 0.9, 0.96722054], [
                               5.7, 0.71671928, 0.9, 0.96722054
                           ], [6.5, 0.41797166, 0.64285714, 0.79948773], [
                               8.4, 0.41797166, 0.64285714, 0.79948773
                           ], [10.0, 0.25976276, 0.48214286, 0.67381139],
                          [12.0, 0.06504527, 0.24107143,
                           0.47680147], [15.0, 0.0, 0.0, 0.0]])

        _km_hazard = kaplan_meier_hazard(_data)
        self.assertTrue(
            np.allclose(_km_hazard, [[
                3.00000000e+00, 4.00000000e+00, 5.70000000e+00, 6.50000000e+00,
                8.40000000e+00, 1.00000000e+01, 1.20000000e+01, 1.50000000e+01
            ], [
                1.11023678e-01, 8.32677588e-02, 5.84335150e-02, 1.34206407e-01,
                1.03850196e-01, 1.34798653e-01, 2.27722649e-01, 0.00000000e+00
            ], [
                3.51201719e-02, 2.63401289e-02, 1.84843010e-02, 6.79742703e-02,
                5.25991377e-02, 7.29514819e-02, 1.18555167e-01, 0.00000000e+00
            ], [
                1.11095811e-02, 8.33218584e-03, 5.84714796e-03, 3.44283221e-02,
                2.66409636e-02, 3.94805044e-02, 6.17212567e-02, 0.00000000e+00
            ], [
                3.33071035e-01, 3.33071035e-01, 3.33071035e-01, 8.72341648e-01,
                8.72341648e-01, 1.34798653e+00, 2.73267179e+00, -0.00000000e+00
            ], [
                1.05360516e-01, 1.05360516e-01, 1.05360516e-01, 4.41832757e-01,
                4.41832757e-01, 7.29514819e-01, 1.42266200e+00, -0.00000000e+00
            ], [
                3.33287433e-02, 3.33287433e-02, 3.33287433e-02, 2.23784094e-01,
                2.23784094e-01, 3.94805044e-01, 7.40655080e-01, -0.00000000e+00
            ], [
                -1.09939949e+00, -1.09939949e+00, -1.09939949e+00,
                -1.36574134e-01, -1.36574134e-01, 2.98612017e-01,
                1.00527981e+00, -0.00000000e+00
            ], [
                -2.25036733e+00, -2.25036733e+00, -2.25036733e+00,
                -8.16823847e-01, -8.16823847e-01, -3.15375598e-01,
                3.52529764e-01, -0.00000000e+00
            ], [
                -3.40133509e+00, -3.40133509e+00, -3.40133509e+00,
                -1.49707356e+00, -1.49707356e+00, -9.29363195e-01,
                -3.00220241e-01, -0.00000000e+00
            ]]))
