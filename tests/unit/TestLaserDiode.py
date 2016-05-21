#!/usr/bin/env python -O
"""
This is the test class for testing Laser Diode module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
<<<<<<< HEAD
#       tests.hardware.TestLaserDiode.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

=======
#       tests.unit.TestLaserDiode.py is part of The RTK Project
#
# All rights reserved.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

<<<<<<< HEAD
import dao.DAO as _dao
=======
import unittest
from nose.plugins.attrib import attr

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
from hardware.component.semiconductor.optoelectronic.LaserDiode import *

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestLaserDiodeModel(unittest.TestCase):
    """
    Class for testing the Optoelectronic Laser Diode data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Optoelectronic Laser Diode class.
        """

<<<<<<< HEAD
        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = LaserDiode()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestLaserDiode) __init__ should return a Optoelectronic LaserDiode data model
        """

        self.assertTrue(isinstance(self.DUT, LaserDiode))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify the Semiconductor class was properly initialized.
        self.assertEqual(self.DUT.category, 2)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piT, 0.0)

        # Verify the Optoelectronic Laser Diode class was properly initialized.
        self.assertEqual(self.DUT._lst_lambdab, [3.23, 5.65])
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 8.0, 5.0, 12.0, 4.0,
                                             6.0, 6.0, 8.0, 17.0, 0.5, 9.0,
                                             24.0, 450.0])
        self.assertEqual(self.DUT._lst_piQ_count, [1.0, 1.0, 3.3])
        self.assertEqual(self.DUT._lst_piQ_stress, [1.0, 1.0, 3.3])
        self.assertEqual(self.DUT._lambdab_count, [[5.1, 16.0, 49.0, 32.0,
                                                    110.0, 58.0, 72.0, 100.0,
                                                    170.0, 230.0, 2.6, 87.0,
                                                    350.0, 2000.0],
                                                   [8.9, 28.0, 85.0, 55.0,
                                                    190.0, 100.0, 130.0, 180.0,
                                                    300.0, 400.0, 4.5, 150.0,
                                                    600.0, 3500.0]])
        self.assertEqual(self.DUT.subcategory, 24)
        self.assertEqual(self.DUT.type, 0)
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.required_power, 0.0)
        self.assertEqual(self.DUT.piI, 0.0)
        self.assertEqual(self.DUT.piA, 0.0)
        self.assertEqual(self.DUT.piP, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestLaserDiode) set_attributes should return a 0 error code on success
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
                   1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.03, 2.3, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 2, 8)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.type, 2)
        self.assertEqual(self.DUT.application, 8)
        self.assertEqual(self.DUT.required_power, 0.5)
        self.assertEqual(self.DUT.piI, 0.8)
        self.assertEqual(self.DUT.piA, 0.03)
        self.assertEqual(self.DUT.piP, 2.3)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestLaserDiode) set_attributes should return a 40 error code when too few items are passed
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
                   1.0, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 2)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestLaserDiode) set_attributes should return a 10 error code when the wrong type is passed
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
                   1.0, 1.0, 0.01, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '', 2)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestLaserDiode) get_attributes should return a tuple of attribute values
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
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 0, 0, 0.0, 0.0, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestLaserDiode) get_attributes(set_attributes(values)) == values
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
                      1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.03, 2.3, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 4, 8)
        _out_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                       0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                       0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                       'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                       1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       0.0, 1.0,
                       0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0,
                       0, 0, 0.0, 30.0, 0.0, 358.0,
                       3, 1.0, 0.01, 2.0, 1.0, 1.0, '', 4, 8, 0.5, 0.8, 0.03,
                       2.3)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_overstressed_high_voltage(self):
        """
        (TestLaserDiode) _overstressed should return False and overstress=False on success with operating voltage greater than rated
        """

        self.DUT.operating_voltage = 18.0
        self.DUT.rated_voltage = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_high_temperature(self):
        """
        (TestLaserDiode) _overstressed should return False and overstress=False on success with junction temperature greater than 125C
        """

        self.DUT.junction_temperature = 135.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_calculate_217_count_gaas(self):
        """
<<<<<<< HEAD
        (TestLaserDiode) calculate should return False on success when calculating MIL-HDBK-217F parts count results for a GaAs laser
=======
        (TestLaserDiode) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results for a GaAs laser
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.type = 1

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 110.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.1E-04)

    @attr(all=True, unit=True)
    def test_calculate_217_count_ingaas(self):
        """
<<<<<<< HEAD
        (TestLaserDiode) calculate should return False on success when calculating MIL-HDBK-217F parts count results for an InGaAs laser
=======
        (TestLaserDiode) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results for an InGaAs laser
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.type = 2

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 190.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.9E-04)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_gaas(self):
        """
<<<<<<< HEAD
        (TestLaserDiode) calculate should return False on success when calculating MIL-HDBK-217F stress results
=======
        (TestLaserDiode) calculate_part should return False on success when calculating MIL-HDBK-217F stress results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_current = 2.0
        self.DUT.rated_power = 33.0
        self.DUT.type = 1
        self.DUT.application = 1
        self.DUT.required_power = 15.0

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piQ * piI * piA * piP * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 3.23)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.24066949)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piI'], 1.60213976)
        self.assertEqual(self.DUT.hazard_rate_model['piA'], 4.4)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piP'], 0.91666667)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.0046576E-05)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_ingaas(self):
        """
<<<<<<< HEAD
        (TestLaserDiode) calculate should return False on success when calculating MIL-HDBK-217F stress results
=======
        (TestLaserDiode) calculate_part should return False on success when calculating MIL-HDBK-217F stress results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_current = 2.0
        self.DUT.rated_power = 33.0
        self.DUT.type = 2
        self.DUT.application = 1
        self.DUT.required_power = 15.0

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piQ * piI * piA * piP * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 5.65)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.24066949)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piI'], 1.60213976)
        self.assertEqual(self.DUT.hazard_rate_model['piA'], 4.4)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piP'], 0.91666667)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.7573732E-05)
