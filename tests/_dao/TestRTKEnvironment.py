#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKEnvironment.py is part of The RTK Project

#
# All rights reserved.
"""
This is the test class for testing the RTKEnvironment module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKEnvironment import RTKEnvironment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKEnvironment(unittest.TestCase):
    """
    Class for testing the RTKEnvironment class.
    """

    _attributes = {
        'environment_id': 1,
        'low_dwell_time': 0.0,
        'minimum': 0.0,
        'ramp_rate': 0.0,
        'high_dwell_time': 0.0,
        'name': 'Test Environmental Condition',
        'maximum': 0.0,
        'units': u'Units',
        'variance': 0.0,
        'phase_id': 1,
        'mean': 0.0
    }

    def setUp(self):
        """
        Sets up the test fixture for the RTKEnvironment class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKEnvironment).first()
        self.DUT.name = 'Test Environmental Condition'

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkenvironment_create(self):
        """
        (TestRTKEnvironment) DUT should create an RTKEnvironment model.
        """

        self.assertTrue(isinstance(self.DUT, RTKEnvironment))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_environment')
        self.assertEqual(self.DUT.phase_id, 1)
        self.assertEqual(self.DUT.environment_id, 1)
        self.assertEqual(self.DUT.name, 'Test Environmental Condition')
        self.assertEqual(self.DUT.units, 'Units')
        self.assertEqual(self.DUT.minimum, 0.0)
        self.assertEqual(self.DUT.maximum, 0.0)
        self.assertEqual(self.DUT.mean, 0.0)
        self.assertEqual(self.DUT.variance, 0.0)
        self.assertEqual(self.DUT.ramp_rate, 0.0)
        self.assertEqual(self.DUT.low_dwell_time, 0.0)
        self.assertEqual(self.DUT.high_dwell_time, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKEnvironment) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKEnvironment) set_attributes should return a zero error code on success
        """

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKEnvironment {0:d} " \
                               "attributes.".format(self.DUT.environment_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_key(self):
        """
        (TestRTKEnvironment) set_attributes should return a 10 error code when passed a dict with a missing key
        """
        self._attributes.pop('variance')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg,
                         "RTK ERROR: Missing attribute 'variance' in " \
                         "attribute dictionary passed to " \
                         "RTKEnvironment.set_attributes().")
