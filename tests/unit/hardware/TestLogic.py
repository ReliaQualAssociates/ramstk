#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestLogic.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing Logic IC module algorithms and models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from hardware.component.integrated_circuit.Logic import Logic

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestLogicModel(unittest.TestCase):
    """
    Class for testing the Logic IC data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Logic IC class.
        """

        self.DUT = Logic()

        self._base_values = (0, 1, 'Alt Part #', 'Attachments', 'CAGE Code',
                             'Comp Ref Des', 6.0, 7.0, 8.0, 'Description',
                             10.0, 11, 12, 'Figure #', 14.0, 'LCN', 16, 17,
                             18.0, 'Name', 'NSN', 21, 'Page #', 23, 24,
                             'Part #', 26, 'Ref Des', 28.0, 29, 'Remarks',
                             31.0, 'Spec #', 33, 34.0, 35.0, 36.0, 2014,
                             38, 39, 40, 41.0, 1, 1)
        self._stress_values = (44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0,
                               52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0,
                               'Sixty')
        self._rel_values = (61.0, 62.0, 63.0, 64.0, 65.0, 66, 67.0, 68.0, 69.0,
                            70.0, 71.0, 72.0, 73, 74.0, {}, 76.0, 77.0, 78.0,
                            79, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0,
                            88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96)
        self._user_values = (97.0, 98.0, 99.0, 100.0, 101.0, 102, 103, 104.0,
                             105.0, 106.0, 107.0, 108, 109, 110.0, 111, 112.0,
                             113.0, 114.0, 115, 116.0, 117.0, 118.0, 119, 120,
                             121.0, 122, 123, 124.0, 125.0, 126, 'Thirty',
                             'Thirty One', '32', '33', '34')

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestLogic) __init__ should return an Logic IC data model
        """

        self.assertTrue(isinstance(self.DUT, Logic))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)

        # Verify the Component class was properly intialized.
        self.assertEqual(self.DUT.junction_temperature, 30.0)

        # Verify the Integrated Circuit class was properly initialized.
        self.assertEqual(self.DUT.category_id, 1)
        self.assertEqual(self.DUT.quality_id, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)

        # Verify the Logic IC class was properly initialized.
        self.assertEqual(self.DUT.subcategory_id, 2)
        self.assertEqual(self.DUT.package_id, 0)
        self.assertEqual(self.DUT.n_pins, 0)
        self.assertEqual(self.DUT.family_id, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestLogic) set_attributes should return a 0 error code on success
        """

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + self._user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[5], 0)
        self.assertEqual(self.DUT.package_id, 120)
        self.assertEqual(self.DUT.n_pins, 121)
        self.assertEqual(self.DUT.family_id, 122)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestLogic) set_attributes should return a 40 error code when too few items are passed
        """

        _user_values = (97.0, 98.0, 99.0, 100.0, 101.0, 102, 103, 104.0,
                        105.0, 106.0, 107.0, 108, 109, 110.0, 111, 112.0,
                        113.0, 114.0, 115, 116.0, 117, 118, 119, 120)

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + _user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[5], 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestLogic) set_attributes should return a 10 error code when the wrong type is passed
        """

        _user_values = (97.0, 98.0, 99.0, 100.0, 101.0, 102, 103, 104.0, 105.0,
                        106.0, 107.0, 108, 109, 110.0, 111, 112.0, 113.0,
                        114.0, 115, 116.0, 117, 118, 119, None, 121.0, 122,
                        123, 124.0, 125.0, 126, 'Thirty', 'Thirty One', '32',
                        '33', '34')

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + _user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[5], 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestLogic) get_attributes should return a tuple of attribute values
        """

        _base_values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0,
                        0, 0, '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0,
                        '', 1, '', 1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0,
                        2014, 0, 0, 0, 0.0, 1, 2)
        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                          0.0, 1.0, 30.0, 25.0, 0.0, 25.0, '')
        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)
        _comp_values = (0.0, 30.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
                        0.0, 0, 0, 0, 0, 0)

        _all_values = _base_values + _stress_values + _rel_values + \
            _comp_values

        _result = self.DUT.get_attributes()
        self.assertEqual(_result[:38], _base_values[:38])
        self.assertEqual(_result[38:50], _stress_values[:12])
        self.assertEqual(_result[50], _stress_values[16])
        self.assertEqual(_result[51:87], _rel_values)
        self.assertEqual(_result[87:89], _base_values[42:44])
        self.assertEqual(_result[89:93], _stress_values[12:16])
        self.assertEqual(_result[93:], _comp_values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestLogic) get_attributes(set_attributes(values)) == values
        """

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + self._user_values

        self.DUT.set_attributes(_all_values)
        _result = self.DUT.get_attributes()

        self.assertEqual(_result[:38], self._base_values[:38])
        self.assertEqual(_result[38:50], self._stress_values[:12])
        self.assertEqual(_result[50], self._stress_values[16])
        self.assertEqual(_result[51:87], self._rel_values)
        self.assertEqual(_result[87:89], self._base_values[42:44])
        self.assertEqual(_result[89:93], self._stress_values[12:16])
        self.assertEqual(_result[93:104], self._user_values[:11])
        self.assertEqual(_result[104:107], self._user_values[20:23])
        self.assertEqual(_result[107:109], self._user_values[23:25])

    @attr(all=True, unit=False)
    def test_calculate_217_count(self):
        """
        (TestLogic) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality_id = 1
        self.DUT.technology_id = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')

    @attr(all=True, unit=True)
    def test_calculate_217_count_all(self):
        """
        (TestLogic) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.num_elements = 100
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.035)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 8.75E-9)

        self.DUT.num_elements = 1000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.055)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.375E-8)

        self.DUT.num_elements = 3000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.097)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.425E-8)

        self.DUT.num_elements = 10000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.33)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 8.25E-8)

        self.DUT.num_elements = 30000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.48)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.2E-7)

        self.DUT.num_elements = 60000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.63)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.575E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestLogic) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality_id = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.technology_id = 1
        self.DUT.family_id = 2
        self.DUT.package_id = 3
        self.DUT.num_elements = 206
        self.DUT.n_pins = 18
        self.DUT.years_produced = 1.5
        self.DUT.case_temperature = 35.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.junction_temperature, 50.0)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         '(C1 * piT + C2 * piE) * piQ * piL')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C1'], 0.005)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C2'], 0.0063511495)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.3709554)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piL'], 1.2458647)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.379876E-8)
