#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKHazards.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKHazard module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.DAO import DAO
from dao.RTKHazards import RTKHazards

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKHazards(unittest.TestCase):
    """
    Class for testing the RTKHazard class.
    """

    attributes = (1, 'Acceleration/Gravity', 'Falls')

    def setUp(self):
        """
        Sets up the test fixture for the RTKHazard class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKHazards).first()
        self.DUT.category = self.attributes[1]
        self.DUT.subcategory = self.attributes[2]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKHazards_create(self):
        """
        (TestRTKHazards) __init__ should create an RTKHazard model
        """

        self.assertTrue(isinstance(self.DUT, RTKHazards))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_hazards')
        self.assertEqual(self.DUT.hazard_id, 1)
        self.assertEqual(self.DUT.category, 'Acceleration/Gravity')
        self.assertEqual(self.DUT.subcategory, 'Falls')

    @attr(all=True, unit=True)
    def test01_RTKHazards_get_attributes(self):
        """
        (TestRTKHazards) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKHazards_set_attributes(self):
        """
        (TestRTKHazards) set_attributes should return a zero error code on success
        """

        _attributes = ('Common Causes', 'Faulty Calibration')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKHazard {0:d} " \
                               "attributes.".format(self.DUT.hazard_id))

    @attr(all=True, unit=True)
    def test02b_RTKHazards_set_attributes_to_few(self):
        """
        (TestRTKHazards) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Common Causes', )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKHazard.set_attributes().")
