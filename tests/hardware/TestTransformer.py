#!/usr/bin/env python -O
"""
This is the test class for testing Transformer module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.hardware.TestTransformer.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
import configuration as _conf
from hardware.component.inductor.Transformer import *


class TestTransformerModel(unittest.TestCase):
    """
    Class for testing the Transformer data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Transformer class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Transformer()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestTransformer) __init__ should return an Transformer data model
        """

        self.assertTrue(isinstance(self.DUT, Transformer))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Inductor class was properly initialized.
        self.assertEqual(self.DUT.category, 5)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.insulation_class, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piQ, 1.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.hot_spot_temperature, 0.0)

        # Verify the Transformer class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 62)
        self.assertEqual(self.DUT.family, 0)
        self.assertEqual(self.DUT.power_loss, 0.0)
        self.assertEqual(self.DUT.case_area, 0.0)
        self.assertEqual(self.DUT.weight, 0.0)
        self.assertEqual(self.DUT.input_power, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestTransformer) set_attributes should return a 0 error code on success
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
                   0.0, 0.0, 1.0, 0.0,
                   0.0, 0.75, 0.5, 0.25, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 2, 0, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.family, 1)
        self.assertEqual(self.DUT.power_loss, 0.75)
        self.assertEqual(self.DUT.case_area, 0.5)
        self.assertEqual(self.DUT.weight, 0.25)
        self.assertEqual(self.DUT.input_power, 1.5)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestTransformer) set_attributes should return a 40 error code when too few items are passed
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
                   0.0, 0.0, 1.0, 0.0,
                   0.0, 0.75, 0.5, 0.25, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 2, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestTransformer) set_attributes should return a 10 error code when the wrong type is passed
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
                   0.0, 0.0, 1.0, 0.0,
                   0.0, 0.75, 0.5, 0.25, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 2, 0, '')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestTransformer) get_attributes should return a tuple of attribute values
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
                   0.0, 0.0, 1.0, 0.0, 0, '',
                   0, 0, 0.0, 0, 0.0, 0.0, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestTransformer) get_attributes(set_attributes(values)) == values
        """

        _in_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
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
                      0.0, 0.0, 0.0, 0.0,
                      0.0, 0.75, 0.5, 0.25, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0,
                      1, 2, 0, 1)
        _out_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                       0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                       0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                       'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                       1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       0.0, 1.0,
                       0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0,
                       1.0, 0.0, 0.0, 0,
                       0, 0,
                       0.0, 30.0, 0.0, 358.0,
                       0.0, 0.0, 0.0, 0.0, 1, '',
                       2, 0, 0.0, 1, 0.75, 0.5, 0.25, 1.5)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestTransformer) calculate should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1
        self.DUT.family = 1
        self.assertFalse(self.DUT.calculate())

        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.13)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.5)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.95E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_pl_sa(self):
        """
        (TestTransformer) calculate should return False on success when calculating MIL-HDBK-217F parts stress results using power loss and surface area to calculate hot spot temperature
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.specification = 1
        self.DUT.family = 1
        self.DUT.insulation_class = 1
        self.DUT.power_loss = 2.25
        self.DUT.case_area = 11.0

        self.assertFalse(self.DUT.calculate())

        self.assertAlmostEqual(self.DUT.hot_spot_temperature, 58.125)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0054381526)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 1.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.8943373E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_pl_wt(self):
        """
        (TestTransformer) calculate should return False on success when calculating MIL-HDBK-217F parts stress results using power loss and weight to calculate hot spot temperature
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.specification = 1
        self.DUT.family = 2
        self.DUT.insulation_class = 2
        self.DUT.power_loss = 2.25
        self.DUT.weight = 0.25

        self.assertFalse(self.DUT.calculate())

        self.assertAlmostEqual(self.DUT.hot_spot_temperature, 102.7154730)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.024154461)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.3478029E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_wt_ip(self):
        """
        (TestTransformer) calculate should return False on success when calculating MIL-HDBK-217F parts stress results using weight and input power to calculate hot spot temperature
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.specification = 1
        self.DUT.family = 3
        self.DUT.insulation_class = 3
        self.DUT.weight = 0.25
        self.DUT.input_power = 3.0

        self.assertFalse(self.DUT.calculate())

        self.assertAlmostEqual(self.DUT.hot_spot_temperature, 47.7046369)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.002509514)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 8.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.2045667E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_class_4(self):
        """
        (TestTransformer) calculate should return False on success when calculating MIL-HDBK-217F parts stress results for insulation class 4
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.specification = 1
        self.DUT.family = 4
        self.DUT.insulation_class = 4
        self.DUT.power_loss = 2.25
        self.DUT.case_area = 11.0

        self.assertFalse(self.DUT.calculate())

        self.assertAlmostEqual(self.DUT.hot_spot_temperature, 58.125)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0023262707)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 12)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.6749149E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_class_5(self):
        """
        (TestTransformer) calculate should return False on success when calculating MIL-HDBK-217F parts stress results for insulation class 5
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 2

        self.DUT.specification = 1
        self.DUT.family = 2
        self.DUT.insulation_class = 5
        self.DUT.power_loss = 2.25
        self.DUT.weight = 0.25

        self.assertFalse(self.DUT.calculate())

        self.assertAlmostEqual(self.DUT.hot_spot_temperature, 102.7154730)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0027912821)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 7.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.2560769E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_class_6(self):
        """
        (TestTransformer) calculate should return False on success when calculating MIL-HDBK-217F parts stress results for insulation class 6
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 2

        self.DUT.specification = 1
        self.DUT.family = 3
        self.DUT.insulation_class = 6
        self.DUT.weight = 0.25
        self.DUT.input_power = 3.0

        self.assertFalse(self.DUT.calculate())

        self.assertAlmostEqual(self.DUT.hot_spot_temperature, 47.7046369)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0016476614)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 30.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.9657905E-7)
