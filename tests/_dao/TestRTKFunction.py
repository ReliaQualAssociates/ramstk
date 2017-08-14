#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKFunction.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKFunction module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKFunction import RTKFunction

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKFunction(unittest.TestCase):
    """
    Class for testing the RTKFunction class.
    """

    _attributes =(1, 1, 0.0, 0.0, 0.0, 'Test Function Code', 0.0, 0.0, 0, 0.0,
                  0.0, 0.0, 0.0, 0.0, 0.0, 'Function Name', 0, '', 0, 0, 0, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKFunction class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKFunction).first()
        self.DUT.function_code = self._attributes[5]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkfunction_create(self):
        """
        (TestRTKFunction) __init__ should create an RTKFunction model.
        """

        self.assertTrue(isinstance(self.DUT, RTKFunction))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_function')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.function_id, 1)
        self.assertEqual(self.DUT.availability_logistics, 0.0)
        self.assertEqual(self.DUT.availability_mission, 0.0)
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.function_code, 'Test Function Code')
        self.assertEqual(self.DUT.hazard_rate_logistics, 0.0)
        self.assertEqual(self.DUT.hazard_rate_mission, 0.0)
        self.assertEqual(self.DUT.level, 0)
        self.assertEqual(self.DUT.mmt, 0.0)
        self.assertEqual(self.DUT.mcmt, 0.0)
        self.assertEqual(self.DUT.mpmt, 0.0)
        self.assertEqual(self.DUT.mtbf_logistics, 0.0)
        self.assertEqual(self.DUT.mtbf_mission, 0.0)
        self.assertEqual(self.DUT.mttr, 0.0)
        self.assertEqual(self.DUT.name, 'Function Name')
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.safety_critical, 0)
        self.assertEqual(self.DUT.total_mode_count, 0)
        self.assertEqual(self.DUT.total_part_count, 0)
        self.assertEqual(self.DUT.type_id, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKFunction) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKFunction) set_attributes should return a zero error code on success
        """

        _attributes = (0.0, 0.0, 0.0, 'Test Function Code', 0.0, 0.0, 0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 'Function Name', 0, '', 0, 0,
                       0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKFunction {0:d} " \
                               "attributes.".format(self.DUT.function_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKFunction) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0.0, 'zero.zero', 0.0, 'Test Function Code', 0.0, 0.0,
                       0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'Function Name', 0, '',
                       0, 0, 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKFunction " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKFunction) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0.0, 0.0, 0.0, 'Test Function Code', 0.0, 0.0, 0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 'Function Name', 0, '', 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKFunction.set_attributes().")

    @attr(all=True, unit=True)
    def test03a_calculate_reliability(self):
        """
        (TestRTKFunction) calculate_reliability should return False on success.
        """

        self.DUT.hazard_rate_logistics = 0.00000151
        self.DUT.hazard_rate_mission = 0.000002

        self.assertFalse(self.DUT.calculate_reliability())
        self.assertAlmostEqual(self.DUT.mtbf_logistics, 662251.6556291)
        self.assertAlmostEqual(self.DUT.mtbf_mission, 500000.0)

    @attr(all=True, unit=True)
    def test03b_calculate_reliability_divide_by_zero(self):
        """
        (TestRTKFunction) calculate_reliability should return True when attempting to divide by zero.
        """

        self.DUT.hazard_rate_mission = 0.0

        self.assertTrue(self.DUT.calculate_reliability())

    @attr(all=True, unit=True)
    def test02a_calculate_availability(self):
        """
        (TestRTKFunction) calculate_availability should return False on success.
        """

        self.DUT.mpmt = 0.5
        self.DUT.mcmt = 1.2
        self.DUT.mttr = 5.8
        self.DUT.mmt = 0.85
        self.DUT.mtbf_logistics = 662251.6556291
        self.DUT.mtbf_mission = 500000.0

        self.assertFalse(self.DUT.calculate_availability())
        self.assertAlmostEqual(self.DUT.availability_logistics, 0.9999912)
        self.assertAlmostEqual(self.DUT.availability_mission, 0.9999884)

    @attr(all=True, unit=True)
    def test02b_calculate_availability_divide_by_zero(self):
        """
        (TestRTKFunction) calculate_availability should return True when attempting to divide by zero.
        """

        self.DUT.mttr = 0.0
        self.DUT.mtbf_logistics = 662251.6556291
        self.DUT.mtbf_mission = 0.0

        self.assertTrue(self.DUT.calculate_availability())
