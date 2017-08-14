#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestMeter.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing Meter module algorithms and models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from hardware.component.meter.Meter import Model, ElapsedTime, Panel

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestMeterModel(unittest.TestCase):
    """
    Class for testing the Meter data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Meter class.
        """

        self.DUT = Model()

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

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestMeter) __init__ should return a Meter data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Meter class was properly initialized.
        self.assertEqual(self.DUT.category, 9)
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestMeter) set_attributes should return a 0 error code on success
        """

        _my_values = (0.05, 1.0, 3, "")
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.application, 3)
        self.assertEqual(self.DUT.base_hr, 0.05)
        self.assertEqual(self.DUT.piE, 1.0)
        self.assertEqual(self.DUT.reason, "")

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestMeter) set_attributes should return a 40 error code when too few items are passed
        """

        _my_values = (0.05, 1.0, 3)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestMeter) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (0.05, None, 3, "")
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestMeter) get_attributes should return a tuple of attribute values
        """

        _my_values = (0, 0.0, 0.0, "")
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '',
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '',
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 30.0) + \
                   _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestMeter) get_attributes(set_attributes(values)) == values
        """

        _my_values = (0.05, 1.0, 3, "")
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()

        self.assertEqual(_result[:38], self._base_values)
        self.assertEqual(_result[38:50], self._stress_values)
        self.assertEqual(_result[50:86], self._rel_values)
        self.assertEqual(_result[86], list(self._user_values[:20]))
        self.assertEqual(_result[87], list(self._user_values[20:30]))
        self.assertEqual(_result[88], list(self._user_values[30:35]))
        self.assertEqual(_result[89:95], self._comp_values)

        self.assertEqual(_result[95:], _my_values)

    @attr(all=True, unit=True)
    def test_calculate_attribute_error(self):
        """
        (TestMeter) calculate_part should return True when there is an AttributeError.
        """

        self.DUT.hazard_rate_type = 1
        self.DUT.environment_active = 1

        self.assertTrue(self.DUT.calculate_part())


class TestElapsedTimeModel(unittest.TestCase):
    """
    Class for testing the Elapsed Time Meter data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Elapsed Time Meter class.
        """

        self.DUT = ElapsedTime()

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
        self._meter_values = (0.05, 1.0, 0, "")

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestElapsedTime) __init__ should return an Elapsed Time Meter data model
        """

        self.assertTrue(isinstance(self.DUT, ElapsedTime))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Meter class was properly initialized.
        self.assertEqual(self.DUT.category, 9)
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

        # Verify the Elapsed Time Meter was properly initialized.
        self.assertEqual(self.DUT.piT, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestElapsedTime) set_attributes should return a 0 error code on success
        """

        _my_values = (0.5, )
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._meter_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.piT, 0.5)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestElapsedTime) set_attributes should return a 40 error code when too few items are passed
        """

        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._meter_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestElapsedTime) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (None, )
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._meter_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestMeter) get_attributes should return a tuple of attribute values
        """

        _my_values = (0.0, )
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '',
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '',
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0.0, "") + _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=False, unit=True)
    def test_calculate_217_count(self):
        """
        (TestElapsedTime) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1
        self.DUT.application = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 180.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.8E-4)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestElapsedTime) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.application = 1
        self.DUT.temperature_active = 45.0
        self.DUT.max_rated_temperature = 105.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 20.0)
        self.assertEqual(self.DUT.hazard_rate_model['piT'], 0.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_active, 2.0E-5)


class TestPanelModel(unittest.TestCase):
    """
    Class for testing the Panel Meter data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Panel Meter class.
        """

        self.DUT = Panel()

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
        self._meter_values = (0.05, 1.0, 0, "")

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestPanel) __init__ should return an Panel Meter data model
        """

        self.assertTrue(isinstance(self.DUT, Panel))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Meter class was properly initialized.
        self.assertEqual(self.DUT.category, 9)
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

        # Verify the Panel Meter was properly initialized.
        self.assertEqual(self.DUT.subcategory, 2)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.function, 0)
        self.assertEqual(self.DUT.piA, 0.0)
        self.assertEqual(self.DUT.piF, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestPanel) set_attributes should return a 0 error code on success
        """

        _my_values = (0.5, 0.01, 0.02, 0.03, 1, 2)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._meter_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.quality, 1)
        self.assertEqual(self.DUT.function, 2)
        self.assertEqual(self.DUT.q_override, 0.5)
        self.assertEqual(self.DUT.piA, 0.01)
        self.assertEqual(self.DUT.piF, 0.02)
        self.assertEqual(self.DUT.piQ, 0.03)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestPanel) set_attributes should return a 40 error code when too few items are passed
        """

        _my_values = (0.5, 0.01, 0.02, 1, 2)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._meter_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestPanel) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (0.5, 0.01, None, 0.03, 1, 2)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._meter_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestMeter) get_attributes should return a tuple of attribute values
        """

        _my_values = (0, 0, 0.0, 0.0, 0.0, 0.0)
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '',
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '',
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0.0, "") + _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=False, unit=True)
    def test_calculate_217_count(self):
        """
        (TestPanel) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.application = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 3.2)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.2E-6)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestPanel) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.application = 1
        self.DUT.function = 3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piA * piF * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.09)
        self.assertEqual(self.DUT.hazard_rate_model['piA'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piF'], 2.8)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 4.0)
        self.assertEqual(self.DUT.hazard_rate_active, 1.008E-6)
