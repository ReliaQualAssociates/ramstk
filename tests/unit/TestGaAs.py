#!/usr/bin/env python -O
"""
This is the test class for testing Gallium Arsenide (GaAS) IC module algorithms
and models.
"""

# -*- coding: utf-8 -*-
#
<<<<<<< HEAD
#       tests.hardware.TestGaAs.py is part of The RTK Project
=======
#       tests.unit.TestGaAs.py is part of The RTK Project
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

<<<<<<< HEAD
import dao.DAO as _dao
from hardware.component.integrated_circuit.GaAs import *
=======
from hardware.component.integrated_circuit.GaAs import GaAs
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestGaAsModel(unittest.TestCase):
    """
    Class for testing the GaAs IC data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the GaAs IC class.
        """

<<<<<<< HEAD
        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = GaAs()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestGaAs) __init__ should return an GaAs IC data model
        """

        self.assertTrue(isinstance(self.DUT, GaAs))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Integrated Circuit class was properly initialized.
        self.assertEqual(self.DUT.category, 1)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piQ, 1.0)

        # Verify the GaAs IC class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 9)
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.package, 0)
        self.assertEqual(self.DUT.n_elements, 0)
        self.assertEqual(self.DUT.n_pins, 0)
        self.assertEqual(self.DUT.years_production, 0.0)
        self.assertEqual(self.DUT.case_temperature, 0.0)
        self.assertEqual(self.DUT.C1, 0.0)
        self.assertEqual(self.DUT.C2, 0.0)
        self.assertEqual(self.DUT.piL, 0.0)
        self.assertEqual(self.DUT.piA, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestGaAs) set_attributes should return a 0 error code on success
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
                   0.0, 0.0, 1.0, 0.0, 1.5, 75.0, 0.0025, 0.0097, 1.2, 0.0038,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 3, 200, 24)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.application, 1)
        self.assertEqual(self.DUT.package, 3)
        self.assertEqual(self.DUT.n_elements, 200)
        self.assertEqual(self.DUT.n_pins, 24)
        self.assertEqual(self.DUT.years_production, 1.5)
        self.assertEqual(self.DUT.case_temperature, 75.0)
        self.assertEqual(self.DUT.C1, 0.0025)
        self.assertEqual(self.DUT.C2, 0.0097)
        self.assertEqual(self.DUT.piL, 1.2)
        self.assertEqual(self.DUT.piA, 0.0038)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestGaAs) set_attributes should return a 40 error code when too few items are passed
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
                   0.0, 0.0, 1.0, 0.0, 1.5, 75.0, 0.0025, 0.0097, 1.2, 0.0038,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 3, 200, 24)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestGaAs) set_attributes should return a 10 error code when the wrong type is passed
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
                   0.0, 0.0, 1.0, 0.0, 1.5, 75.0, 0.0025, 0.0097, 1.2, 0.0038,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 3, '', 24)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestGaAs) get_attributes should return a tuple of attribute values
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
                   0.0, 0.0, 1.0, 0.0, 0.0, 0, '',
                   0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestGaAs) get_attributes(set_attributes(values)) == values
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
                      0.0, 0.0, 1.0, 0.0, 1.5, 75.0, 0.0025, 0.0097, 1.2,
                      0.0038, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 1, 3, 200, 24)
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
                       0.0, 0.0, 1.0, 0.0, 1.5, 0, '',
                       1, 3, 200, 24, 1.5, 75.0, 0.0025, 0.0097, 1.2, 0.0038)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=False, unit=False)
    def test_calculate_217_count(self):
        """
<<<<<<< HEAD
        (TestGaAs) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestGaAs) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1
<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')

    @attr(all=True, unit=True)
    def test_calculate_217_count_all(self):
        """
<<<<<<< HEAD
        (TestGaAs) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestGaAs) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.application = 1
        self.DUT.n_elements = 6
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.052)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.3E-8)

        self.DUT.application = 1
        self.DUT.n_elements = 11
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.079)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.975E-8)

        self.DUT.application = 4
        self.DUT.n_elements = 56
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.084)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.1E-8)

        self.DUT.application = 4
        self.DUT.n_elements = 2011
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.15)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.75E-8)

    @attr(all=True, unit=True)
<<<<<<< HEAD
    def test_calculate_217_stress(self):
        """
        (TestGaAs) calculate should return False on success when calculating MIL-HDBK-217F parts stress results
=======
    def test_calculate_217_stress_part(self):
        """
        (TestGaAs) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.application = 1
        self.DUT.package = 3
        self.DUT.n_elements = 16
        self.DUT.n_pins = 18
        self.DUT.years_production = 1.5
        self.DUT.case_temperature = 35.0

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.junction_temperature, 50.0)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         '(C1 * piT * piA + C2 * piE) * piQ * piL')
        self.assertEqual(self.DUT.hazard_rate_model['C1'], 4.5)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C2'], 0.0063511495)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'],
                               2.92952497E-7)
        self.assertEqual(self.DUT.hazard_rate_model['piA'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piL'], 1.2458647)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.18694199E-8)
