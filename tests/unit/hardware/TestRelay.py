#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestRelay.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing Relay module algorithms and models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from hardware.component.relay.Relay import Model
from hardware.component.relay.Mechanical import Mechanical
from hardware.component.relay.SolidState import SolidState

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestRelayModel(unittest.TestCase):
    """
    Class for testing the Relay data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Relay class.
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
                             2, 3, 440.0, 50, 60, 7.0, 80.0, 90, '1', '2', 'Two',
                             'Three', '4')
        self._comp_values = (0, 0, 0.0, 30.0, 0.0, 358.0)

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestRelay) __init__ should return a Relay data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Relay class was properly initialized.
        self.assertEqual(self.DUT.category, 6)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.construction, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestRelay) set_attributes should return a 0 error code on success
        """

        _my_values = (1.0, 0.01, 2.0, 3.0, "")
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.quality, 1)
        self.assertEqual(self.DUT.construction, 2)
        self.assertEqual(self.DUT.q_override, 1.0)
        self.assertEqual(self.DUT.base_hr, 0.01)
        self.assertEqual(self.DUT.piQ, 2.0)
        self.assertEqual(self.DUT.piE, 3.0)
        self.assertEqual(self.DUT.reason, "")

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestRelay) set_attributes should return a 40 error code when too few items are passed
        """

        _my_values = (1.0, 0.01, 2.0, 1.0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestRelay) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (1.0, 0.01, None, 1.0, "")
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestRelay) get_attributes should return a tuple of attribute values
        """

        _my_values = (0, 0, 0.0, 0.0, 0.0, 0.0, "")
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
        (TestRelay) get_attributes(set_attributes(values)) == values
        """

        _my_values = (1.0, 0.01, 2.0, 3.0, "")
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

        self.assertEqual(_result[97:], _my_values)


class TestMechanicalModel(unittest.TestCase):
    """
    Class for testing the Mechanical data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Mechanical class.
        """

        self.DUT = Mechanical()

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
                             2, 3, 440.0, 50, 60, 7.0, 80.0, 90, '0', '1', '2', '3',
                             '4')
        self._comp_values = (0, 0, 0.0, 30.0, 0.0, 358.0)

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestMechanical) __init__ should return a Mechanical data model
        """

        self.assertTrue(isinstance(self.DUT, Mechanical))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify the Relay class was properly initialized.
        self.assertEqual(self.DUT.category, 6)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.construction, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

        # Verify the Mechanical Relay class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 64)
        self.assertEqual(self.DUT.temperature_rating, 0)
        self.assertEqual(self.DUT.load_type, 0)
        self.assertEqual(self.DUT.contact_form, 0)
        self.assertEqual(self.DUT.contact_rating, 0)
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.cycles_per_hour, 0.0)
        self.assertEqual(self.DUT.piL, 0.0)
        self.assertEqual(self.DUT.piCYC, 0.0)
        self.assertEqual(self.DUT.piC, 0.0)
        self.assertEqual(self.DUT.piF, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestMechanical) set_attributes should return a 0 error code on success
        """

        _my_values = (1.0, 0.01, 2.0, 3.0, "")
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.temperature_rating, 2)
        self.assertEqual(self.DUT.load_type, 3)
        self.assertEqual(self.DUT.contact_form, 4)
        self.assertEqual(self.DUT.contact_rating, 0)
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.cycles_per_hour, 14.0)
        self.assertEqual(self.DUT.piL, 15.0)
        self.assertEqual(self.DUT.piCYC, 16.0)
        self.assertEqual(self.DUT.piC, 17.0)
        self.assertEqual(self.DUT.piF, 18.0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestMechanical) set_attributes should return a 40 error code when too few items are passed
        """

        _my_values = (1.0, 0.01, 2.0, 3.0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestMechanical) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (1.0, 0.01, None, 3.0, "")
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestMechanical) get_attributes should return a tuple of attribute values
        """

        _my_values = (0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0)
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '',
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '',
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 30.0,
                   0, 0, 0.0, 0.0, 0.0, 0.0, "") + _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestMechanical) get_attributes(set_attributes(values)) == values
        """

        _my_values = (0.0, 0.0, 0.0, 0.0, '0', 2, 3, 4, 0, 0, 14.0, 15.0, 16.0, 17.0,
                      18.0)
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

        self.assertEqual(_result[97:], _my_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestMechanical) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.hazard_rate_type = 1
        self.DUT.environment_active = 5
        self.DUT.construction = 1
        self.DUT.quality = 2

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 3.8)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.14E-5)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestMechanical) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.environment_active = 2
        self.DUT.temperature_rating = 1
        self.DUT.temperature_active = 38.0
        self.DUT.operating_current = 1.25
        self.DUT.rated_current = 3.3
        self.DUT.load_type = 2
        self.DUT.contact_form = 4
        self.DUT.contact_rating = 1
        self.DUT.quality = 1
        self.DUT.cycles_per_hour = 0.0025
        self.DUT.application = 1
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piL * piC * piCYC * piF * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.006346104)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piL'], 2.4516263)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.1)
        self.assertEqual(self.DUT.hazard_rate_model['piCYC'], 0.1)
        self.assertEqual(self.DUT.hazard_rate_model['piF'], 4.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.4893241E-9)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_cycle(self):
        """
        (TestMechanical) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for a high cycle relay
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.environment_active = 2
        self.DUT.temperature_rating = 1
        self.DUT.temperature_active = 38.0
        self.DUT.operating_current = 1.25
        self.DUT.rated_current = 3.3
        self.DUT.load_type = 2
        self.DUT.contact_form = 4
        self.DUT.contact_rating = 1
        self.DUT.quality = 7
        self.DUT.cycles_per_hour = 1100
        self.DUT.application = 1
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piL * piC * piCYC * piF * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.006346104)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piL'], 2.4516263)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piCYC'], 121.0)
        self.assertEqual(self.DUT.hazard_rate_model['piF'], 8.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 5.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 0.0004518123)


class TestSolidStateModel(unittest.TestCase):
    """
    Class for testing the SolidState data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the SolidState class.
        """

        self.DUT = SolidState()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestMechanical) __init__ should return a SolidState data model
        """

        self.assertTrue(isinstance(self.DUT, SolidState))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify the Relay class was properly initialized.
        self.assertEqual(self.DUT.category, 6)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.construction, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

        # Verify the Mechanical Relay class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 65)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestSolidState) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.hazard_rate_type = 1
        self.DUT.environment_active = 5
        self.DUT.construction = 1
        self.DUT.quality = 2

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 6.8)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 4.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.72E-5)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestMechanical) calculate_part should return False on success when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.environment_active = 2
        self.DUT.quality = 2
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.4)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 4.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.8E-6)
