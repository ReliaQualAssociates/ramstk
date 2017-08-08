#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKMeasurement.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing the RTKMeasurement module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKMeasurement import RTKMeasurement

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKMeasurement(unittest.TestCase):
    """
    Class for testing the RTKMeasurement class.
    """

    attributes = (1, 'Contamination, Concentration')

    def setUp(self):
        """
        Sets up the test fixture for the RTKMeasurement class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKMeasurement).first()
        self.DUT.description = self.attributes[1]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKMeasurement_create(self):
        """
        (TestRTKMeasurement) __init__ should create an RTKMeasurement model
        """

        self.assertTrue(isinstance(self.DUT, RTKMeasurement))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_measurement')
        self.assertEqual(self.DUT.measurement_id, 1)
        self.assertEqual(self.DUT.description, 'Contamination, Concentration')

    @attr(all=True, unit=True)
    def test01_RTKMeasurement_get_attributes(self):
        """
        (TestRTKMeasurement) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKMeasurement_set_attributes(self):
        """
        (TestRTKMeasurement) set_attributes should return a zero error code on success
        """

        _attributes = ('Contamination, Particle Size', )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKMeasurement {0:d} " \
                               "attributes.".format(self.DUT.measurement_id))

    @attr(all=True, unit=True)
    def test02b_RTKMeasurement_set_attributes_to_few(self):
        """
        (TestRTKMeasurement) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ()

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKMeasurement.set_attributes().")
