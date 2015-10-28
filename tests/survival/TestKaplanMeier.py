#!/usr/bin/env python -O
"""
This is the test class for testing Kaplan-Meier module algorithms
and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.survival.TestKaplanMeier.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr
import numpy as np

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from analyses.survival.KaplanMeier import *


class TestKaplanMeier(unittest.TestCase):
    """
    Class for testing the KaplanMeier data model class.
    """

    @attr(all=True, unit=True)
    def test_kaplan_meier(self):
        """
        (TestKaplanMeier) kaplan_meier should return a numpy matrix of floats on success
        """

        # Data is from Lee and Wang, page 69, example 4.2.
        _data = [('', 3.0, 3.0, 0.0, u'Event', 1),
                 ('', 4.0, 4.0, 0.0, u'Right Censored', 1),
                 ('', 5.7, 5.7, 0.0, u'Right Censored', 1),
                 ('', 6.5, 6.5, 0.0, u'Event', 1),
                 ('', 6.5, 6.5, 0.0, u'Event', 1),
                 ('', 8.4, 8.4, 0.0, u'Right Censored', 1),
                 ('', 10.0, 10.0, 0.0, u'Event', 1),
                 ('', 10.0, 10.0, 0.0, u'Right Censored', 1),
                 ('', 12.0, 12.0, 0.0, u'Event', 1),
                 ('', 15.0, 15.0, 0.0, u'Event', 1)]

        _km = kaplan_meier(_data, 0.0, 100000.0)
        self.assertTrue(np.allclose(_km[0],
                                    [[3.0, 0.71671928, 0.9, 0.96722054],
                                     [4.0, 0.71671928, 0.9, 0.96722054],
                                     [5.7, 0.71671928, 0.9, 0.96722054],
                                     [6.5, 0.41797166, 0.64285714, 0.79948773],
                                     [8.4, 0.41797166, 0.64285714, 0.79948773],
                                     [10.0, 0.25976276, 0.48214286, 0.67381139],
                                     [12.0, 0.06504527, 0.24107143, 0.47680147],
                                     [15.0, 0.0, 0.0, 0.0]]))

        self.assertTrue(np.allclose(_km[1], [1, 4, 5, 7, 9, 10]))

    @attr(all=True, unit=True)
    def test_kaplan_meier_mean(self):
        """
        (TestKaplanMeier) kaplan_meier_mean should return a numpy 1-D matrix of integers on success
        """

        # This data is the result of the executing the Kaplan-Meier function
        # using the data set from the previous test.
        _data = np.array([[3.0, 0.71671928, 0.9, 0.96722054],
                          [4.0, 0.71671928, 0.9, 0.96722054],
                          [5.7, 0.71671928, 0.9, 0.96722054],
                          [6.5, 0.41797166, 0.64285714, 0.79948773],
                          [8.4, 0.41797166, 0.64285714, 0.79948773],
                          [10.0, 0.25976276, 0.48214286, 0.67381139],
                          [12.0, 0.06504527, 0.24107143, 0.47680147],
                          [15.0, 0.0, 0.0, 0.0]])
        _rank = [1, 4, 5, 7, 9, 10]

        _km_mean = kaplan_meier_mean(_data, _rank, 0.9)
        self.assertTrue(np.allclose(_km_mean,
                                   [8.14115869673, 10.0875, 12.0338413033]))

    @attr(all=True, unit=True)
    def test_kaplan_meier_hazard(self):
        """
        (TestKaplanMeier) kaplan_meier_hazard should return a numpy matrix of floats on success
        """

        _data = np.array([[3.0, 0.71671928, 0.9, 0.96722054],
                          [4.0, 0.71671928, 0.9, 0.96722054],
                          [5.7, 0.71671928, 0.9, 0.96722054],
                          [6.5, 0.41797166, 0.64285714, 0.79948773],
                          [8.4, 0.41797166, 0.64285714, 0.79948773],
                          [10.0, 0.25976276, 0.48214286, 0.67381139],
                          [12.0, 0.06504527, 0.24107143, 0.47680147],
                          [15.0, 0.0, 0.0, 0.0]])

        _km_hazard = kaplan_meier_hazard(_data)
        self.assertTrue(np.allclose(_km_hazard,
                                    [[0.11102368, 0.08326776, 0.05843351, 0.13420641, 0.1038502, 0.13479865, 0.22772265, -0.0],
                                     [0.03512017, 0.02634013, 0.0184843, 0.06797427, 0.05259914, 0.07295148, 0.11855517, -0.0],
                                     [0.01110958, 0.00833219, 0.00584715, 0.03442832, 0.02664096, 0.0394805, 0.06172126, -0.0],
                                     [0.33307104, 0.33307104, 0.33307104, 0.87234165, 0.87234165, 1.34798653, 2.73267179,-0.0],
                                     [0.10536052, 0.10536052, 0.10536052, 0.44183276, 0.44183276, 0.72951482, 1.422662, -0.0],
                                     [0.03332874, 0.03332874, 0.03332874, 0.22378409, 0.22378409, 0.39480504, 0.74065508, -0.0],
                                     [-1.09939949, -1.09939949, -1.09939949, -0.13657413, -0.13657413, 0.29861202, 1.00527981, -0.0],
                                     [-2.25036733, -2.25036733, -2.25036733, -0.81682385, -0.81682385, -0.3153756, 0.35252976, -0.0],
                                     [-3.40133509, -3.40133509, -3.40133509, -1.49707356, -1.49707356, -0.9293632, -0.30022024, -0.0]]))
