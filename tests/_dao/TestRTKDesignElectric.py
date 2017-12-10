#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKDesignElectric.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing RTKDesignElectric module algorithms and models."""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKDesignElectric import RTKDesignElectric

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKDesignElectric(unittest.TestCase):
    """Class for testing the RTKDesignElectric class."""

    _attributes = {
        'voltage_ac_operating': 0.0,
        'frequency_operating': 0.0,
        'type_id': 0,
        'resistance': 0.0,
        'package_id': 0,
        'technology_id': 0,
        'n_cycles': 0,
        'n_circuit_planes': 1,
        'contact_gauge': 0,
        'current_operating': 0.0,
        'n_hand_soldered': 0,
        'contact_rating_id': 0,
        'area': 0.0,
        'contact_form_id': 0,
        'years_in_production': 1,
        'n_active_pins': 0,
        'capacitance': 0.0,
        'temperature_case': 0.0,
        'current_rated': 0.0,
        'power_operating': 0.0,
        'configuration_id': 0,
        'temperature_hot_spot': 0.0,
        'temperature_junction': 0.0,
        'current_ratio': 0.0,
        'insulation_id': 0,
        'construction_id': 0,
        'insert_id': 0,
        'theta_jc': 0.0,
        'voltage_dc_operating': 0.0,
        'power_ratio': 0.0,
        'family_id': 0,
        'overstress': 1,
        'voltage_rated': 0.0,
        'feature_size': 0.0,
        'operating_life': 0.0,
        'application_id': 0,
        'weight': 0.0,
        'temperature_rated_max': 0.0,
        'voltage_ratio': 0.0,
        'temperature_rated_min': 0.0,
        'power_rated': 0.0,
        'environment_active_id': 0,
        'hardware_id': 3,
        'specification_id': 0,
        'matching_id': 0,
        'n_elements': 0,
        'environment_dormant_id': 0,
        'reason': u'',
        'voltage_esd': 0.0,
        'manufacturing_id': 0,
        'n_wave_soldered': 0,
        'temperature_rise': 0.0
    }

    def setUp(self):
        """(TestRTKDesignElectric) Set up the test fixture for the RTKDesignElectric class."""
        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKDesignElectric).first()
        self.DUT.overstress = 1

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkdesignelectric_create(self):
        """(TestRTKDesignElectric) __init__ should create an RTKDesignElectric model."""
        self.assertTrue(isinstance(self.DUT, RTKDesignElectric))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_design_electric')
        self.assertEqual(self.DUT.hardware_id, 3)
        self.assertEqual(self.DUT.application_id, 0)
        self.assertEqual(self.DUT.area, 0.0)
        self.assertEqual(self.DUT.capacitance, 0.0)
        self.assertEqual(self.DUT.configuration_id, 0)
        self.assertEqual(self.DUT.construction_id, 0)
        self.assertEqual(self.DUT.contact_form_id, 0)
        self.assertEqual(self.DUT.contact_gauge, 0)
        self.assertEqual(self.DUT.contact_rating_id, 0)
        self.assertEqual(self.DUT.current_operating, 0.0)
        self.assertEqual(self.DUT.current_rated, 0.0)
        self.assertEqual(self.DUT.current_ratio, 0.0)
        self.assertEqual(self.DUT.environment_active_id, 0)
        self.assertEqual(self.DUT.environment_dormant_id, 0)
        self.assertEqual(self.DUT.family_id, 0)
        self.assertEqual(self.DUT.feature_size, 0.0)
        self.assertEqual(self.DUT.frequency_operating, 0.0)
        self.assertEqual(self.DUT.insert_id, 0)
        self.assertEqual(self.DUT.insulation_id, 0)
        self.assertEqual(self.DUT.manufacturing_id, 0)
        self.assertEqual(self.DUT.matching_id, 0)
        self.assertEqual(self.DUT.n_active_pins, 0)
        self.assertEqual(self.DUT.n_circuit_planes, 1)
        self.assertEqual(self.DUT.n_cycles, 0)
        self.assertEqual(self.DUT.n_elements, 0)
        self.assertEqual(self.DUT.n_hand_soldered, 0)
        self.assertEqual(self.DUT.n_wave_soldered, 0)
        self.assertEqual(self.DUT.operating_life, 0.0)
        self.assertEqual(self.DUT.overstress, 1)
        self.assertEqual(self.DUT.package_id, 0)
        self.assertEqual(self.DUT.power_operating, 0.0)
        self.assertEqual(self.DUT.power_rated, 0.0)
        self.assertEqual(self.DUT.power_ratio, 0.0)
        self.assertEqual(self.DUT.reason, '')
        self.assertEqual(self.DUT.resistance, 0.0)
        self.assertEqual(self.DUT.specification_id, 0)
        self.assertEqual(self.DUT.technology_id, 0)
        self.assertEqual(self.DUT.temperature_case, 0.0)
        self.assertEqual(self.DUT.temperature_hot_spot, 0.0)
        self.assertEqual(self.DUT.temperature_junction, 0.0)
        self.assertEqual(self.DUT.temperature_rated_max, 0.0)
        self.assertEqual(self.DUT.temperature_rated_min, 0.0)
        self.assertEqual(self.DUT.temperature_rise, 0.0)
        self.assertEqual(self.DUT.theta_jc, 0.0)
        self.assertEqual(self.DUT.type_id, 0)
        self.assertEqual(self.DUT.voltage_ac_operating, 0.0)
        self.assertEqual(self.DUT.voltage_dc_operating, 0.0)
        self.assertEqual(self.DUT.voltage_esd, 0.0)
        self.assertEqual(self.DUT.voltage_rated, 0.0)
        self.assertEqual(self.DUT.voltage_ratio, 0.0)
        self.assertEqual(self.DUT.weight, 0.0)
        self.assertEqual(self.DUT.years_in_production, 1)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """(TestRTKDesignElectric) get_attributes should return a tuple of attribute values."""
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """(TestRTKDesignElectric) set_attributes should return a zero error code on success."""
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKDesignElectric " \
                               "{0:d} attributes.".\
                         format(self.DUT.hardware_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_key(self):
        """(TestRTKDesignElectric) set_attributes should return a 40 error code when passed a dict with a missing key."""
        self._attributes.pop('family_id')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute 'family_id' in " \
                               "attribute dictionary passed to " \
                               "RTKDesignElectric.set_attributes().")

        self._attributes['family_id'] = 0
