#!/usr/bin/env python -O
"""
This is the test class for testing Multi-Pin Connection module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
<<<<<<< HEAD
#       tests.hardware.TestMultipin.py is part of The RTK Project
#
# All rights reserved.

=======
#       tests.unit.TestMultipin.py is part of The RTK Project
#
# All rights reserved.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

<<<<<<< HEAD
import dao.DAO as _dao
=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
from hardware.component.connection.Multipin import Multipin

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestMultipinModel(unittest.TestCase):
    """
    Class for testing the Multi-Pin Connection data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Multi-Pin Connection class.
        """

<<<<<<< HEAD
        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = Multipin()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestMultipin) __init__ should return a Multi-Pin Connection data model
        """

        self.assertTrue(isinstance(self.DUT, Multipin))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Connection class was properly initialized.
        self.assertEqual(self.DUT.category, 8)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

        # Verify the Multi-Pint Connection class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 72)
        self.assertEqual(self.DUT.insert, 0)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.configuration, 0)
        self.assertEqual(self.DUT.contact_gauge, 22)
        self.assertEqual(self.DUT.mate_unmate_cycles, 0)
        self.assertEqual(self.DUT.n_active_contacts, 0)
        self.assertEqual(self.DUT.contact_temperature, 30.0)
        self.assertEqual(self.DUT.amps_per_contact, 0.0)
        self.assertEqual(self.DUT.piK, 0.0)
        self.assertEqual(self.DUT.piP, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestMultipin) set_attributes should return a 0 error code on success
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
                   110.0, 0.002, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 2, 3, 20, 5, 20)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestMultipin) set_attributes should return a 40 error code when too few items are passed
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
                   110.0, 0.002, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 2, 3, 20)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestMultipin) set_attributes should return a 10 error code when the wrong type is passed
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
                   110.0, 0.002, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 2, 3, '', 5, 20)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestMultipin) get_attributes should return a tuple of attribute values
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
                   0, 0, 0, 22, 0, 0.0, 0.0, 0.0, 0.0, 30.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestMultipin) get_attributes(set_attributes(values)) == values
        """

        _in_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                      'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                      0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                      'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                      'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                      1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                      0.0, 1.0,
                      0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      1, 0.0, 'Equation', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                      0.0, 0,
                      0, 0, 1, 0.0,
                      0, 0,
                      0.0, 30.0, 0.0, 358.0,
                      0.0, 0.0, 1.0, 0.0,
                      0.0, 0.0, 0.005, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0,
                      1, 2, 3, 4, 20, 15)
        _out_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                       0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                       0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                       'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                       1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       0.0, 1.0,
                       0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, 'Equation', 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0,
                       1.0, 0.0, 0.0, 0,
                       0, 0,
                       0.0, 30.0, 0.0, 358.0,
                       0.0, 0.0, 1.0, 0.0, 1, '',
                       2, 3, 4, 20, 15, 0.0, 0.0, 0.005, 0.5, 0.0)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
<<<<<<< HEAD
        (TestMultipin) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestMultipin) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.configuration = 1
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
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.2)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.0E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_insert_a(self):
        """
<<<<<<< HEAD
        (TestMultipin) calculate should return False on success when calculating MIL-HDBK-217F parts stress results for insert group A
=======
        (TestMultipin) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results for insert group A
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.temperature_active = 30.0
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.configuration = 1
        self.DUT.specification = 3
        self.DUT.insert = 1
        self.DUT.amps_per_contact = 0.005
        self.DUT.contact_gauge = 22
        self.DUT.mate_unmate_cycles = 10
        self.DUT.n_active_contacts = 15

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piE * piK * piP')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0001145779)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 13.0)
        self.assertEqual(self.DUT.hazard_rate_model['piK'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piP'], 3.2787411002)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.4651180E-8)
        self.assertAlmostEqual(self.DUT.temperature_rise, 5.4738236E-5)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_insert_b(self):
        """
<<<<<<< HEAD
        (TestMultipin) calculate should return False on success when calculating MIL-HDBK-217F parts stress results for insert group B
=======
        (TestMultipin) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results for insert group B
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.temperature_active = 30.0
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.configuration = 1
        self.DUT.specification = 1
        self.DUT.insert = 1
        self.DUT.amps_per_contact = 0.005
        self.DUT.contact_gauge = 20
        self.DUT.mate_unmate_cycles = 10
        self.DUT.n_active_contacts = 15

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piE * piK * piP')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0005676702)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 13.0)
        self.assertEqual(self.DUT.hazard_rate_model['piK'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piP'], 3.2787411002)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 7.2588501E-8)
        self.assertAlmostEqual(self.DUT.temperature_rise, 3.5422114E-5)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_insert_c(self):
        """
<<<<<<< HEAD
        (TestMultipin) calculate should return False on success when calculating MIL-HDBK-217F parts stress results for insert group C
=======
        (TestMultipin) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results for insert group C
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.temperature_active = 30.0
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.configuration = 3
        self.DUT.specification = 1
        self.DUT.insert = 1
        self.DUT.amps_per_contact = 0.005
        self.DUT.contact_gauge = 16
        self.DUT.mate_unmate_cycles = 10
        self.DUT.n_active_contacts = 15

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piE * piK * piP')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0039613902)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 13.0)
        self.assertEqual(self.DUT.hazard_rate_model['piK'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piP'], 3.2787411002)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.0654655E-7)
        self.assertAlmostEqual(self.DUT.temperature_rise, 1.5165093E-5)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_insert_d(self):
        """
<<<<<<< HEAD
        (TestMultipin) calculate should return False on success when calculating MIL-HDBK-217F parts stress results for insert group D
=======
        (TestMultipin) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results for insert group D
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.temperature_active = 30.0
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.configuration = 2
        self.DUT.specification = 1
        self.DUT.insert = 7
        self.DUT.amps_per_contact = 0.005
        self.DUT.contact_gauge = 12
        self.DUT.mate_unmate_cycles = 10
        self.DUT.n_active_contacts = 15

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piE * piK * piP')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0078140276)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 13.0)
        self.assertEqual(self.DUT.hazard_rate_model['piK'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piP'], 3.2787411002)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 9.9918676E-7)
        self.assertAlmostEqual(self.DUT.temperature_rise, 5.5347054E-6)
