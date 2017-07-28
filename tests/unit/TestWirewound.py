#!/usr/bin/env python -O
"""
This is the test class for testing fixed and variable Wirewound resistor module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestWirewound.py is part of The RTK Project
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
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr
from hardware.component.resistor.fixed.Wirewound import Wirewound, \
                                                        WirewoundChassisMount, \
                                                        WirewoundPower
from hardware.component.resistor.variable.Wirewound import PowerWirewound, \
                                                           PrecisionWirewound, \
                                                           SemiPrecisionWirewound, \
                                                           VarWirewound

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestWirewoundModel(unittest.TestCase):
    """
    Class for testing the Wirewound resistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Wirewound resistor class.
        """

        self.DUT = Wirewound()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestWirewound) __init__ should return a Wirewound resistor model
        """

        self.assertTrue(isinstance(self.DUT, Wirewound))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Wirewound resistor class was properly initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 11.0, 5.0, 18.0, 15.0,
                                             18.0, 28.0, 35.0, 27.0, 0.8, 14.0,
                                             38.0, 610.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.03, 0.1, 0.3, 1.0, 5.0,
                                                    15.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.0085, 0.018, 0.10,
                                                       0.045, 0.16, 0.15, 0.17,
                                                       0.30, 0.38, 0.26,
                                                       0.0068, 0.13, 0.37,
                                                       5.4])
        self.assertEqual(self.DUT.subcategory, 29)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.16)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_active, 4.8E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_resistance(self):
        """
        (TestWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for low resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.075
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 3.3E3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.004010588)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.4063525E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid1_resistance(self):
        """
        (TestWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for mid-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.075
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 3.3E4

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.004010588)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.7)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.09079976E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid2_resistance(self):
        """
        (TestWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with mid-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.075
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 3.3E5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.004010588)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 7.2190584E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_resistance(self):
        """
        (TestWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with high resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.075
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 3.3E7

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.004010588)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 5.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.2031764E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestWirewound) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 1130.0
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E4

        self.assertTrue(self.DUT.calculate_part())


class TestWirewoundPowerModel(unittest.TestCase):
    """
    Class for testing the Wirewound Power resistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Wirewound Power resistor class.
        """

        self.DUT = WirewoundPower()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestWirewoundPower) __init__ should return a Wirewound Power resistor model
        """

        self.assertTrue(isinstance(self.DUT, WirewoundPower))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Wirewound Power resistor class was properly initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 10.0, 5.0, 16.0, 4.0,
                                             8.0, 9.0, 18.0, 23.0, 0.3, 13.0,
                                             34.0, 610.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.03, 0.1, 0.3, 1.0, 5.0,
                                                    15.0])
        self.assertEqual(self.DUT._lambdab_count, [[0.014, 0.031, 0.16, 0.077,
                                                    0.26, 0.073, 0.15, 0.19,
                                                    0.39, 0.42, 0.0042, 0.21,
                                                    0.62, 9.4],
                                                   [0.013, 0.028, 0.15, 0.070,
                                                    0.24, 0.065, 0.13, 0.18,
                                                    0.35, 0.38, 0.0038, 0.19,
                                                    0.56, 8.6]])
        self.assertEqual(self.DUT.subcategory, 30)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.style, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestWirewoundPower) set_attributes should return a 0 error code on success
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1, 3)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.specification, 1)
        self.assertEqual(self.DUT.style, 3)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestWirewoundPower) set_attributes should return a 40 error code with missing inputs
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestWirewoundPower) set_attributes should return a 10 error code with a wrong data type
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '', 2)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestWirewoundPower) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1,
                   0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0,
                   0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestWirewoundPower) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.specification = 2

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.24)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_active, 7.2E-9)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_rwr(self):
        """
        (TestWirewoundPower) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with RWR style resistors
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 8300.0
        self.DUT.specification = 1
        self.DUT.style = 3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.01135004)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.2)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 8.1720288E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_rw(self):
        """
        (TestWirewoundPower) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with RW style resistors
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 0.113
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 3300.0
        self.DUT.specification = 2
        self.DUT.style = 3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.01135004)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.2)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 8.1720288E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestWirewoundPower) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 1130.0
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E4

        self.assertTrue(self.DUT.calculate_part())


class TestWirewoundChassisMountModel(unittest.TestCase):
    """
    Class for testing the Wirewound Network resistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Wirewound Network resistor class.
        """

        self.DUT = WirewoundChassisMount()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestWirewoundChassisMount) __init__ should return a Wirewound Chassis Mount Power resistor model
        """

        self.assertTrue(isinstance(self.DUT, WirewoundChassisMount))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Wirewound Chassis Mount Power resistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 10.0, 5.0, 16.0, 4.0,
                                             8.0, 9.0, 18.0, 23.0, 0.5, 13.0,
                                             34.0, 610.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.03, 0.1, 0.3, 1.0, 5.0,
                                                    15.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.008, 0.18, 0.096,
                                                       0.045, 0.15, 0.044,
                                                       0.088, 0.12, 0.24, 0.25,
                                                       0.004, 0.13, 0.37, 5.5])
        self.assertEqual(self.DUT.subcategory, 31)
        self.assertEqual(self.DUT.characteristic, 0)
        self.assertEqual(self.DUT.style, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestWirewoundChassisMount) set_attributes should return a 0 error code on success
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.characteristic, 1)
        self.assertEqual(self.DUT.style, 1)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestWirewoundChassisMount) set_attributes should return a 40 error code with missing inputs
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestWirewoundChassisMount) set_attributes should return a 10 error code with a wrong data type
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestWirewoundChassisMount) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1,
                   0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0,
                   0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestWirewoundChassisMount) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.15)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_active, 4.5E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestWirewoundChassisMount) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with case temperature known
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.junction_temperature = 30.0
        self.DUT.operating_power = 0.075
        self.DUT.rated_power = 0.25
        self.DUT.specification = 1
        self.DUT.style = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piR * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001375020)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 8.25012E-11)


class TestVarWirewoundModel(unittest.TestCase):
    """
    Class for testing the Variable Wirewound resistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Variable Wirewound resistor class.
        """

        self.DUT = VarWirewound()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestVarWirewound) __init__ should return a Variable Wirewound resistor model
        """

        self.assertTrue(isinstance(self.DUT, VarWirewound))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Variable Wirewound resistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 12.0, 6.0, 20.0, 5.0,
                                             8.0, 9.0, 15.0, 33.0, 0.5, 18.0,
                                             48.0, 870.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.02, 0.06, 0.2, 0.6, 3.0,
                                                    10.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.025, 0.055, 0.35,
                                                       0.15, 0.58, 0.16, 0.26,
                                                       0.35, 0.58, 1.1, 0.013,
                                                       0.52, 1.6, 24.0])
        self.assertEqual(self.DUT.subcategory, 33)
        self.assertEqual(self.DUT.n_taps, 3)
        self.assertEqual(self.DUT.piTAPS, 0.0)
        self.assertEqual(self.DUT.piV, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestVarWirewound) set_attributes should return a 0 error code on success
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.5, 0.75, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 2)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.n_taps, 2)
        self.assertEqual(self.DUT.piTAPS, 0.5)
        self.assertEqual(self.DUT.piV, 0.75)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestVarWirewound) set_attributes should return a 40 error code with missing inputs
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestVarWirewound) set_attributes should return a 10 error code with a wrong data type
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestVarWirewound) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1,
                   0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0,
                   0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 3, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestVarWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.58)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_active, 1.74E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_resistance(self):
        """
        (TestWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for low-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.75
        self.DUT.rated_voltage = 40.0
        self.DUT.resistance = 3.3E1
        self.DUT.n_taps = 5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.02200512)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.05)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.02)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.1452998E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid_resistance(self):
        """
        (TestVarWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for mid-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.75
        self.DUT.rated_voltage = 40.0
        self.DUT.resistance = 3.3E3
        self.DUT.n_taps = 5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.02200512)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.4)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.02)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.0541329E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_resistance(self):
        """
        (TestWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with high resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.75
        self.DUT.rated_voltage = 40.0
        self.DUT.resistance = 1.3E4
        self.DUT.n_taps = 5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.02200512)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.02)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.363047E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestWirewound) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 1130.0
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E4

        self.assertTrue(self.DUT.calculate_part())


class TestPrecisionWirewoundModel(unittest.TestCase):
    """
    Class for testing the Precision Variable Wirewound resistor data model
    class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Precision Variable Wirewound resistor
        class.
        """

        self.DUT = PrecisionWirewound()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestPrecisionWirewound) __init__ should return a Precision Variable Wirewound resistor model
        """

        self.assertTrue(isinstance(self.DUT, PrecisionWirewound))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Precision Variable Wirewound resistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piC, [2.0, 1.0, 3.0, 1.5])
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 18.0, 8.0, 30.0, 8.0,
                                             12.0, 13.0, 18.0, 53.0, 0.5, 29.0,
                                             76.0, 1400.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [2.5, 5.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.33, 0.73, 7.0, 2.9,
                                                       12.0, 3.5, 5.3, 7.1,
                                                       9.8, 23.0, 0.16, 11.0,
                                                       33.0, 510.0])
        self.assertEqual(self.DUT.subcategory, 34)
        self.assertEqual(self.DUT.n_taps, 3)
        self.assertEqual(self.DUT.construction, 0)
        self.assertEqual(self.DUT.piTAPS, 0.0)
        self.assertEqual(self.DUT.piV, 0.0)
        self.assertEqual(self.DUT.piC, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestPrecisionWirewound) set_attributes should return a 0 error code on success
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.5, 0.75, 0.3,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 4, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.n_taps, 4)
        self.assertEqual(self.DUT.construction, 1)
        self.assertEqual(self.DUT.piTAPS, 0.5)
        self.assertEqual(self.DUT.piV, 0.75)
        self.assertEqual(self.DUT.piC, 0.3)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestPrecisionWirewound) set_attributes should return a 40 error code with missing inputs
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestPrecisionWirewound) set_attributes should return a 10 error code with a wrong data type
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1, '')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestPrecisionWirewound) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1,
                   0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0,
                   0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 3, 0, 0.0, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestPrecisionWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 12.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_active, 3.6E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_resistance(self):
        """
        (TestPrecisionWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for low-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.75
        self.DUT.rated_voltage = 40.0
        self.DUT.resistance = 3.3E2
        self.DUT.n_taps = 5
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piC * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.1780886)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.2068982E-06)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid_resistance(self):
        """
        (TestPrecisionWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for mid-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.75
        self.DUT.rated_voltage = 40.0
        self.DUT.resistance = 3.3E4
        self.DUT.n_taps = 5
        self.DUT.construction = 2

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piC * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.1780886)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.4)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.0896574E-06)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_resistance(self):
        """
        (TestPrecisionWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with high resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.75
        self.DUT.rated_voltage = 40.0
        self.DUT.resistance = 3.3E5
        self.DUT.n_taps = 5
        self.DUT.construction = 3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piC * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.1780886)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 3.5)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.3172431E-05)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestPrecisionWirewound) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 1130.0
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E4

        self.assertTrue(self.DUT.calculate_part())


class TestSemiPrecisionWirewoundModel(unittest.TestCase):
    """
    Class for testing the SemiPrecision Variable Wirewound resistor data model
    class.
    """

    def setUp(self):
        """
        Setup the test fixture for the SemiPrecision Variable Wirewound resistor
        class.
        """

        self.DUT = SemiPrecisionWirewound()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestSemiPrecisionWirewound) __init__ should return a SemiPrecision Variable Wirewound resistor model
        """

        self.assertTrue(isinstance(self.DUT, SemiPrecisionWirewound))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the SemiPrecision Variable Wirewound resistor class was
        # properly initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 16.0, 7.0, 28.0, 8.0,
                                             12.0, 0.0, 0.0, 38.0, 0.5, 0.0,
                                             0.0, 0.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [2.0, 4.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.15, 0.35, 3.1, 1.2,
                                                       5.4, 1.9, 2.8, 0.0, 0.0,
                                                       9.0, 0.075, 0.0, 0.0,
                                                       0.0])
        self.assertEqual(self.DUT.subcategory, 35)
        self.assertEqual(self.DUT.n_taps, 3)
        self.assertEqual(self.DUT.piTAPS, 0.0)
        self.assertEqual(self.DUT.piV, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestSemiPrecisionWirewound) set_attributes should return a 0 error code on success
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.5, 0.75, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 4)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.n_taps, 4)
        self.assertEqual(self.DUT.piTAPS, 0.5)
        self.assertEqual(self.DUT.piV, 0.75)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestSemiPrecisionWirewound) set_attributes should return a 40 error code with missing inputs
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestSemiPrecisionWirewound) set_attributes should return a 10 error code with a wrong data type
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestSemiPrecisionWirewound) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1,
                   0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0,
                   0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 3, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestSemiPrecisionWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 5.4)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_active, 1.62E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_resistance(self):
        """
        (TestSemiPrecisionWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for low-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.75
        self.DUT.rated_voltage = 40.0
        self.DUT.resistance = 3.3E2
        self.DUT.n_taps = 5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.1406202)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.970339E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid_resistance(self):
        """
        (TestSemiPrecisionWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for mid-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.75
        self.DUT.rated_voltage = 40.0
        self.DUT.resistance = 3.3E3
        self.DUT.n_taps = 5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.1406202)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.4)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.9516946E-06)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_resistance(self):
        """
        (TestSemiPrecisionWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with high resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.75
        self.DUT.rated_voltage = 40.0
        self.DUT.resistance = 8.3E3
        self.DUT.n_taps = 5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.1406202)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.7881354E-06)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestSemiPrecisionWirewound) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 1130.0
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E3

        self.assertTrue(self.DUT.calculate_part())


class TestPowerWirewoundModel(unittest.TestCase):
    """
    Class for testing the Power Variable Wirewound resistor data model
    class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Power Variable Wirewound resistor
        class.
        """

        self.DUT = PowerWirewound()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestPowerWirewound) __init__ should return a Power Variable Wirewound resistor model
        """

        self.assertTrue(isinstance(self.DUT, PowerWirewound))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Power Variable Wirewound resistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piC, [2.0, 1.0])
        self.assertEqual(self.DUT._lst_piE, [1.0, 3.0, 16.0, 7.0, 28.0, 8.0,
                                             12.0, 0.0, 0.0, 38.0, 0.5, 0.0,
                                             0.0, 0.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.03, 0.1, 0.3, 1.0, 3.0,
                                                   10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [2.0, 4.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.15, 0.34, 2.9, 1.2,
                                                       5.0, 1.6, 2.4, 0.0, 0.0,
                                                       7.6, 0.076, 0.0, 0.0,
                                                       0.0])
        self.assertEqual(self.DUT.subcategory, 36)
        self.assertEqual(self.DUT.n_taps, 3)
        self.assertEqual(self.DUT.construction, 0)
        self.assertEqual(self.DUT.piTAPS, 0.0)
        self.assertEqual(self.DUT.piV, 0.0)
        self.assertEqual(self.DUT.piC, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestPowerWirewound) set_attributes should return a 0 error code on success
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.5, 0.75, 0.3,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 4, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.n_taps, 4)
        self.assertEqual(self.DUT.construction, 1)
        self.assertEqual(self.DUT.piTAPS, 0.5)
        self.assertEqual(self.DUT.piV, 0.75)
        self.assertEqual(self.DUT.piC, 0.3)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestPowerWirewound) set_attributes should return a 40 error code with missing inputs
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestPowerWirewound) set_attributes should return a 10 error code with a wrong data type
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1, 8.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1, '')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestPowerWirewound) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1,
                   0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0,
                   0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 3, 0, 0.0, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestPowerWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 5.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_active, 1.5E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_resistance(self):
        """
        (TestPowerWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for low-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.75
        self.DUT.rated_voltage = 40.0
        self.DUT.resistance = 3.3
        self.DUT.n_taps = 5
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piC * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.1369368)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 1.1)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.2399601E-06)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid_resistance(self):
        """
        (TestPowerWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for mid-range resistances
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.75
        self.DUT.rated_voltage = 40.0
        self.DUT.resistance = 3.3E3
        self.DUT.n_taps = 5
        self.DUT.construction = 2

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piC * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.1369368)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.4)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.8508583E-06)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_resistance(self):
        """
        (TestPowerWirewound) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with high resistance
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.temperature_active = 30.0
        self.DUT.operating_power = 0.75
        self.DUT.rated_voltage = 40.0
        self.DUT.resistance = 8.3E3
        self.DUT.n_taps = 5
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piTAPS * piC * piR * piV * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.1369368)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piTAPS'], 1.2392136)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piV'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 8.1453094E-06)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestPowerWirewound) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 1130.0
        self.DUT.rated_power = 0.25
        self.DUT.resistance = 1.1E4

        self.assertTrue(self.DUT.calculate_part())
