#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKDesignMechanic.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKDesignMechanic module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKDesignMechanic import RTKDesignMechanic

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKDesignMechanic(unittest.TestCase):
    """
    Class for testing the RTKDesignMechanic class.
    """

    _attributes = (1, 0.0, 0, 0, 0.0, 0, 0.0, 0.04, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0,
                   0, 0, 0.0, 0.0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKDesignMechanic class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKDesignMechanic).first()
        self.DUT.deflection = 0.04

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkdesignmechanic_create(self):
        """
        (TestRTKDesignMechanic) __init__ should create an RTKDesignMechanic model.
        """

        self.assertTrue(isinstance(self.DUT, RTKDesignMechanic))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_design_mechanic')
        self.assertEqual(self.DUT.hardware_id, 1)
        self.assertEqual(self.DUT.altitude_operating, 0.0)
        self.assertEqual(self.DUT.application_id, 0)
        self.assertEqual(self.DUT.balance_id, 0)
        self.assertEqual(self.DUT.clearance, 0.0)
        self.assertEqual(self.DUT.casing_id, 0)
        self.assertEqual(self.DUT.contact_pressure, 0.0)
        self.assertEqual(self.DUT.deflection, 0.04)
        self.assertEqual(self.DUT.diameter_coil, 0.0)
        self.assertEqual(self.DUT.diameter_inner, 0.0)
        self.assertEqual(self.DUT.diameter_outer, 0.0)
        self.assertEqual(self.DUT.diameter_wire, 0.0)
        self.assertEqual(self.DUT.filter_size, 0.0)
        self.assertEqual(self.DUT.flow_design, 0.0)
        self.assertEqual(self.DUT.flow_operating, 0.0)
        self.assertEqual(self.DUT.frequency_operating, 0.0)
        self.assertEqual(self.DUT.friction, 0.0)
        self.assertEqual(self.DUT.impact_id, 0)
        self.assertEqual(self.DUT.leakage_allowable, 0.0)
        self.assertEqual(self.DUT.length, 0.0)
        self.assertEqual(self.DUT.length_compressed, 0.0)
        self.assertEqual(self.DUT.length_relaxed, 0.0)
        self.assertEqual(self.DUT.load_design, 0.0)
        self.assertEqual(self.DUT.load_id, 0)
        self.assertEqual(self.DUT.load_operating, 0.0)
        self.assertEqual(self.DUT.lubrication_id, 0)
        self.assertEqual(self.DUT.manufacturing_id, 0)
        self.assertEqual(self.DUT.material_id, 0)
        self.assertEqual(self.DUT.meyer_hardness, 0.0)
        self.assertEqual(self.DUT.misalignment_angle, 0.0)
        self.assertEqual(self.DUT.n_ten, 0)
        self.assertEqual(self.DUT.n_cycles, 0)
        self.assertEqual(self.DUT.n_elements, 0)
        self.assertEqual(self.DUT.offset, 0.0)
        self.assertEqual(self.DUT.particle_size, 0.0)
        self.assertEqual(self.DUT.pressure_contact, 0.0)
        self.assertEqual(self.DUT.pressure_delta, 0.0)
        self.assertEqual(self.DUT.pressure_downstream, 0.0)
        self.assertEqual(self.DUT.pressure_rated, 0.0)
        self.assertEqual(self.DUT.pressure_upstream, 0.0)
        self.assertEqual(self.DUT.rpm_design, 0.0)
        self.assertEqual(self.DUT.rpm_operating, 0.0)
        self.assertEqual(self.DUT.service_id, 0)
        self.assertEqual(self.DUT.spring_index, 0.0)
        self.assertEqual(self.DUT.surface_finish, 0.0)
        self.assertEqual(self.DUT.technology_id, 0)
        self.assertEqual(self.DUT.thickness, 0.0)
        self.assertEqual(self.DUT.torque_id, 0)
        self.assertEqual(self.DUT.type_id, 0)
        self.assertEqual(self.DUT.viscosity_design, 0.0)
        self.assertEqual(self.DUT.viscosity_dynamic, 0.0)
        self.assertEqual(self.DUT.water_per_cent, 0.0)
        self.assertEqual(self.DUT.width_minimum, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKDesignMechanic) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKDesignMechanic) set_attributes should return a zero error code on success
        """

        _attributes = (0.0, 0, 0, 0.0, 0, 0.0, 0.04, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0,
                       0, 0, 0, 0.0, 0.0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0, 0, 0.0, 0.0,
                       0.0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKDesignMechanic {0:d} " \
                               "attributes.".format(self.DUT.hardware_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKDesignMechanic) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0.0, 0, 0, 0.0, 0, 0.0, 0.04, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0,
                       0, 0, 0, 0.0, 0.0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 'zero', 0.0, 0.0, 0, 0.0, 0, 0, 0.0,
                       0.0, 0.0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKDesignMechanic " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKDesignMechanic) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0.0, 0, 0, 0.0, 0, 0.0, 0.04, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0,
                       0, 0, 0, 0.0, 0.0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0, 0, 0.0, 0.0,
                       0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKDesignMechanic.set_attributes().")
