#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestSolder.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing Solder Connection module algorithms and models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from hardware.component.connection.Solder import PTH, NonPTH

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestPTHModel(unittest.TestCase):
    """
    Class for testing the Plated Through Hole (PTH) Connection data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Solder Connection class.
        """

        self.DUT = PTH()

        self._base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                             'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                             0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                             0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                             'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014)
        self._stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                               0.0, 1.0)
        self._rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                            0.0, 0)
        self._user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                             11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0,
                             2, 3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One',
                             'Two', 'Three', '4')
        self._comp_values = (0, 0, 0.0, 30.0, 0.0, 358.0)
        self._connection_values = (0.0, 0.0, 0.0, 0.0, 0, "")

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestPTH) __init__ should return a PTH Connection data model
        """

        self.assertTrue(isinstance(self.DUT, PTH))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Connection class was properly initialized.
        self.assertEqual(self.DUT.category, 8)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

        # Verify the PTH Connection class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 75)
        self.assertEqual(self.DUT.piC, 0.0)
        self.assertEqual(self.DUT.technology, 0)
        self.assertEqual(self.DUT.n_wave_soldered, 0)
        self.assertEqual(self.DUT.n_hand_soldered, 0)
        self.assertEqual(self.DUT.n_circuit_planes, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestPTH) set_attributes should return a 0 error code on success
        """

        _my_values = (2.0, 0, 0, 0, 0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._connection_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestPTH) set_attributes should return a 40 error code when too few items are passed
        """

        _my_values = (2.0, 0, 0, 0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._connection_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestPTH) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (None, 0, 0, 0, 0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._connection_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestPTH) get_attributes should return a tuple of attribute values
        """

        _my_values = (0.0, 0, 0, 0, 0)
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '',
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '',
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 30.0,
                   0.0, 0.0, 1.0, 0.0, 0, "") + _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestPTH) get_attributes(set_attributes(values)) == values
        """

        _my_values = (2.0, 0, 0, 0, 0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._connection_values + \
                  _my_values

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()

        self.assertEqual(_result[:38], self._base_values)
        self.assertEqual(_result[38:50], self._stress_values)
        self.assertEqual(_result[50:86], self._rel_values)
        self.assertEqual(_result[86], list(self._user_values[:20]))
        self.assertEqual(_result[87], list(self._user_values[20:30]))
        self.assertEqual(_result[88], list(self._user_values[30:35]))
        self.assertEqual(_result[89:95], self._comp_values)
        self.assertEqual(_result[95:101], self._connection_values)

        self.assertEqual(_result[101:], _my_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestPTH) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.27)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.7E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestPTH) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 2

        self.DUT.technology = 1
        self.DUT.n_wave_soldered = 5
        self.DUT.n_hand_soldered = 10
        self.DUT.n_circuit_planes = 10

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * (N1 * piC + N2 * (piC + 13.0)) * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.000041)
        self.assertEqual(self.DUT.hazard_rate_model['N1'], 5)
        self.assertEqual(self.DUT.hazard_rate_model['N2'], 10)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piC'], 2.7727669)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.8141007E-8)


class TestNonPTHModel(unittest.TestCase):
    """
    Class for testing the Plated Through Hole (NonPTH) Connection data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Solder Connection class.
        """

        self.DUT = NonPTH()

        self._base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                             'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                             0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                             0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                             'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014)
        self._stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                               0.0, 1.0)
        self._rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                            0.0, 0)
        self._user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                             11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0,
                             2, 3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One',
                             'Two', 'Three', '4')
        self._comp_values = (0, 0, 0.0, 30.0, 0.0, 358.0)
        self._connection_values = (0.0, 0.0, 0.0, 0.0, 0, "")

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestNonPTH) __init__ should return a NonPTH Connection data model
        """

        self.assertTrue(isinstance(self.DUT, NonPTH))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Connection class was properly initialized.
        self.assertEqual(self.DUT.category, 8)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

        # Verify the NonPTH Connection class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 76)
        self.assertEqual(self.DUT.connection_type, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestNonPTH) set_attributes should return a 0 error code on success
        """

        _my_values = (2, )
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._connection_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestNonPTH) set_attributes should return a 40 error code when too few items are passed
        """

        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._connection_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestNonPTH) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (None, )
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._connection_values + \
                  _my_values
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestNonPTH) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '',
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '',
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 30.0,
                   0.0, 0.0, 1.0, 0.0, 0, "", 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestNonPTH) get_attributes(set_attributes(values)) == values
        """

        _my_values = (2, )
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._connection_values + \
                  _my_values

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()

        self.assertEqual(_result[:38], self._base_values)
        self.assertEqual(_result[38:50], self._stress_values)
        self.assertEqual(_result[50:86], self._rel_values)
        self.assertEqual(_result[86], list(self._user_values[:20]))
        self.assertEqual(_result[87], list(self._user_values[20:30]))
        self.assertEqual(_result[88], list(self._user_values[30:35]))
        self.assertEqual(_result[89:95], self._comp_values)
        self.assertEqual(_result[95:101], self._connection_values)

        self.assertEqual(_result[101:], _my_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestNonPTH) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1
        self.DUT.connection_type = 3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.029)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.9E-9)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestNonPTH) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 2

        self.DUT.connection_type = 3

        self.assertFalse(self.DUT.calculate_part())

        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0026)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.2E-9)
