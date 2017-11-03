#!/usr/bin/env python -O
"""
This is the test class for testing Hazard module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestHazard.py is part of The RTK Project
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

import dao.DAO as _dao
from analyses.hazard.Hazard import Model, Hazard

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2015 Andrew "weibullguy" Rowland'


class TestHazardModel(unittest.TestCase):
    """
    Class for testing the Hazard data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Hazard class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestHazard) __init__ should return a Hazard model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.hardware_id, None)
        self.assertEqual(self.DUT.hazard_id, None)
        self.assertEqual(self.DUT.potential_hazard, '')
        self.assertEqual(self.DUT.potential_cause, '')
        self.assertEqual(self.DUT.assembly_effect, '')
        self.assertEqual(self.DUT.assembly_severity, 0)
        self.assertEqual(self.DUT.assembly_probability, 0)
        self.assertEqual(self.DUT.assembly_hri, 0)
        self.assertEqual(self.DUT.assembly_mitigation, '')
        self.assertEqual(self.DUT.assembly_severity_f, 0)
        self.assertEqual(self.DUT.assembly_probability_f, 0)
        self.assertEqual(self.DUT.assembly_hri_f, 0)
        self.assertEqual(self.DUT.system_effect, '')
        self.assertEqual(self.DUT.system_severity, 0)
        self.assertEqual(self.DUT.system_probability, 0)
        self.assertEqual(self.DUT.system_hri, 0)
        self.assertEqual(self.DUT.system_mitigation, '')
        self.assertEqual(self.DUT.system_severity_f, 0)
        self.assertEqual(self.DUT.system_probability_f, 0)
        self.assertEqual(self.DUT.system_hri_f, 0)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.function_1, '')
        self.assertEqual(self.DUT.function_2, '')
        self.assertEqual(self.DUT.function_3, '')
        self.assertEqual(self.DUT.function_4, '')
        self.assertEqual(self.DUT.function_5, '')
        self.assertEqual(self.DUT.result_1, 0.0)
        self.assertEqual(self.DUT.result_2, 0.0)
        self.assertEqual(self.DUT.result_3, 0.0)
        self.assertEqual(self.DUT.result_4, 0.0)
        self.assertEqual(self.DUT.result_5, 0.0)
        self.assertEqual(self.DUT.user_blob_1, '')
        self.assertEqual(self.DUT.user_blob_2, '')
        self.assertEqual(self.DUT.user_blob_3, '')
        self.assertEqual(self.DUT.user_float_1, 0.0)
        self.assertEqual(self.DUT.user_float_2, 0.0)
        self.assertEqual(self.DUT.user_float_3, 0.0)
        self.assertEqual(self.DUT.user_int_1, 0)
        self.assertEqual(self.DUT.user_int_2, 0)
        self.assertEqual(self.DUT.user_int_3, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestHazard) set_attributes should return (0, '') on success
        """

        _values = (0, 32, '', '', '', 4, 5, 20, '', 4, 5, 20, '', 4, 5, 20,
                   '', 4, 5, 20, '', '', '', '', '', '', 0.0, 0.0, 0.0, 0.0,
                   0.0, '', '', '', 0.0, 0.0, 0.0, 0, 0, 0)

        self.assertEqual(self.DUT.set_attributes(_values), (0, ''))

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestHazard) set_attributes should return 10 when the wrong data type is passed
        """

        _values = (0, 32, '', '', '', 4, 5, 20, '', 4, 5, 20, '', 4, 5, 20,
                   '', 4, 5, 20, '', '', '', '', '', '', 0.0, None, 0.0, 0.0,
                   0.0, '', '', '', 0.0, 0.0, 0.0, 0, 0, 0)

        self.assertEqual(self.DUT.set_attributes(_values)[0], 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestHazard) set_attributes should return 40 when one or more values is missing
        """

        _values = (0, 32, '', '', '', 4, 5, 20, '', 4, 5, 20, '', 4, 5, 20,
                   '', 4, 5, 20, '', '', '', '', '', '', 0.0, 0.0, 0.0, 0.0,
                   0.0, '', '', '', 0.0, 0.0, 0.0, 0)

        self.assertEqual(self.DUT.set_attributes(_values)[0], 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestHazard) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', 0, 0, 0, '', 0, 0, 0, '', 0, 0, 0,
                   '', 0, 0, 0, '', '', '', '', '', '', 0.0, 0.0, 0.0, 0.0,
                   0.0, '', '', '', 0.0, 0.0, 0.0, 0, 0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestHazard) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 32, '', '', '', 4, 5, 20, '', 4, 5, 20, '', 4, 5, 20,
                   '', 4, 5, 20, '', '', '', '', '', '', 0.0, 0.0, 0.0, 0.0,
                   0.0, '', '', '', 0.0, 0.0, 0.0, 0, 0, 0)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)

    @attr(all=True, unit=True)
    def test_calculate_assembly_hri(self):
        """
        (TestHazard) calculate should return 0 on success and assembly HRI = 6
        """

        self.DUT.assembly_probability = 2
        self.DUT.assembly_severity = 3

        self.assertFalse(self.DUT.calculate())

        self.assertEqual(self.DUT.assembly_hri, 6)

    @attr(all=True, unit=True)
    def test_calculate_assembly_hri_f(self):
        """
        (TestHazard) calculate should return 0 on success and final assembly HRI = 4
        """

        self.DUT.assembly_probability_f = 2
        self.DUT.assembly_severity_f = 2

        self.assertFalse(self.DUT.calculate())

        self.assertEqual(self.DUT.assembly_hri_f, 4)

    @attr(all=True, unit=True)
    def test_calculate_system_hri(self):
        """
        (TestHazard) calculate should return 0 on success and system HRI = 16
        """

        self.DUT.system_probability = 4
        self.DUT.system_severity = 4

        self.assertFalse(self.DUT.calculate())

        self.assertEqual(self.DUT.system_hri, 16)

    @attr(all=True, unit=True)
    def test_calculate_system_hri_f(self):
        """
        (TestHazard) calculate should return 0 on success and final system HRI = 8
        """

        self.DUT.system_probability_f = 2
        self.DUT.system_severity_f = 4

        self.assertFalse(self.DUT.calculate())

        self.assertEqual(self.DUT.system_hri_f, 8)

    @attr(all=True, unit=True)
    def test_calculate_user_function_1(self):
        """
        (TestHazard) calculate should return 0 on success and user-defined function result = 0.00425
        """

        self.DUT.user_float_1 = 0.005
        self.DUT.user_float_2 = 0.85
        self.DUT.function_1 = 'uf1 * uf2'

        self.assertFalse(self.DUT.calculate())

        self.assertEqual(self.DUT.result_1, 0.00425)

    @attr(all=True, unit=True)
    def test_calculate_user_function_2(self):
        """
        (TestHazard) calculate should return 0 on success and user-defined function result = 0.04
        """

        self.DUT.user_float_3 = 0.005
        self.DUT.user_int_2 = 8
        self.DUT.function_2 = 'ui2 * uf3'

        self.assertFalse(self.DUT.calculate())

        self.assertEqual(self.DUT.result_2, 0.04)

    @attr(all=True, unit=True)
    def test_calculate_user_function_3(self):
        """
        (TestHazard) calculate should return 0 on success and user-defined function result = 0.00116618
        """

        self.DUT.user_float_1 = 0.005
        self.DUT.user_float_2 = 3.5
        self.DUT.user_int_1 = 3
        self.DUT.user_int_2 = 10
        self.DUT.function_3 = 'ui2 * uf1 / (uf2**ui1)'

        self.assertFalse(self.DUT.calculate())

        self.assertAlmostEqual(self.DUT.result_3, 0.00116618)

    @attr(all=True, unit=True)
    def test_calculate_user_function_4(self):
        """
        (TestHazard) calculate should return 0 on success and user-defined function result = -9.45
        """

        self.DUT.user_float_1 = 0.05
        self.DUT.user_float_2 = 3.5
        self.DUT.user_int_1 = 3
        self.DUT.user_int_2 = 10
        self.DUT.function_4 = 'uf2 + uf1 - (ui2 + ui1)'

        self.assertFalse(self.DUT.calculate())

        self.assertAlmostEqual(self.DUT.result_4, -9.45)


class TestHazardController(unittest.TestCase):
    """
    Class for testing the Hazard data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Hazard class.
        """

        self.DUT = Hazard()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestHazard) __init__ should create an Hazard data controller
        """

        self.assertTrue(isinstance(self.DUT, Hazard))
        self.assertEqual(self.DUT.dicHazard, {})
        self.assertEqual(self.DUT.dao, None)

