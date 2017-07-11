#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKMission.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKMission module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKMission import RTKMission

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKMission(unittest.TestCase):
    """
    Class for testing the RTKMission class.
    """

    _attributes = (1, 1, 'Test Mission Description', 0.0, 'hours')
    
    def setUp(self):
        """
        Sets up the test fixture for the RTKMission class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKMission).first()
        self.DUT.description = self._attributes[2]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkmission_create(self):
        """
        (TestMission) DUT should create an RTKMission model
        """

        self.assertTrue(isinstance(self.DUT, RTKMission))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_mission')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.mission_id, 1)
        self.assertEqual(self.DUT.description, 'Test Mission Description')
        self.assertEqual(self.DUT.mission_time, 0.0)
        self.assertEqual(self.DUT.time_units, 'hours')

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKMission) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKMission) set_attributes should return a zero error code on success
        """

        _attributes = ('Test Mission Description', 0.0, 'hours')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKMission {0:d} " \
                               "attributes.".format(self.DUT.mission_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKMission) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('Test Mission Description', None, 'hours')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKMission " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKMission) set_attributes should return a zero error code when passed too few attributes
        """

        _attributes = ('Test Mission Description', 216.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to " \
                               "RTKMission.set_attributes().")

