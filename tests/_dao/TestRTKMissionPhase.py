#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKMissionPhase.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKPhase module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKMissionPhase import RTKMissionPhase

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKPhase(unittest.TestCase):
    """
    Class for testing the RTKPhase class.
    """

    _attributes = (1, 1, 'Test Mission Phase', '', 0.0, 100.0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKPhase class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKMissionPhase).first()
        self.DUT.description = self._attributes[2]
        self.DUT.name = self._attributes[3]
        self.DUT.phase_end = self._attributes[5]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKPhase_create(self):
        """
        (TestRTKPhase) __init__ should create an RTKPhase model
        """

        self.assertTrue(isinstance(self.DUT, RTKMissionPhase))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_mission_phase')
        self.assertEqual(self.DUT.mission_id, 1)
        self.assertEqual(self.DUT.phase_id, 1)
        self.assertEqual(self.DUT.description, 'Test Mission Phase')
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.phase_start, 0.0)
        self.assertEqual(self.DUT.phase_end, 100.0)

    @attr(all=True, unit=True)
    def test01_RTKPhase_get_attributes(self):
        """
        (TestRTKPhase) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_RTKPhase_set_attributes(self):
        """
        (TestRTKPhase) set_attributes should return a zero error code on success
        """

        _attributes = ('Test Mission Phase', 'Test', 0.0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKMissionPhase {0:d} " \
                               "attributes.".format(self.DUT.phase_id))

    @attr(all=True, unit=True)
    def test02b_RTKPhases_set_attributes_wrong_type(self):
        """
        (TestRTKPhases) set_attributes should return a 10 error code when passed the wrong data type
        """

        _attributes = ('Test Mission Phase', 'Test', 0.0, 'None')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKMissionPhase " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_RTKPhases_set_attributes_to_few(self):
        """
        (TestRTKPhases) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Test Mission Phase', 'Test', 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKMissionPhase.set_attributes().")
