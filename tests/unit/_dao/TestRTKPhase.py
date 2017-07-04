#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKPhase.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKPhase module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKPhase import RTKPhase

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKPhase(unittest.TestCase):
    """
    Class for testing the RTKPhase class.
    """

    attributes = (1, 'Concept/Planning (PCP)', 'development')

    def setUp(self):
        """
        Sets up the test fixture for the RTKPhase class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKPhase).first()
        self.DUT.description = self.attributes[1]
        self.DUT.type = self.attributes[2]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKPhase_create(self):
        """
        (TestRTKPhase) __init__ should create an RTKPhase model
        """

        self.assertTrue(isinstance(self.DUT, RTKPhase))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_phase')
        self.assertEqual(self.DUT.phase_id, 1)
        self.assertEqual(self.DUT.description, 'Concept/Planning (PCP)')
        self.assertEqual(self.DUT.type, 'development')

    @attr(all=True, unit=True)
    def test01_RTKPhase_get_attributes(self):
        """
        (TestRTKPhase) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKPhase_set_attributes(self):
        """
        (TestRTKPhase) set_attributes should return a zero error code on success
        """

        _attributes = ('Requirements Analysis (SRA)', 'development')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKPhase {0:d} " \
                               "attributes.".format(self.DUT.phase_id))

    @attr(all=True, unit=True)
    def test02b_RTKPhases_set_attributes_to_few(self):
        """
        (TestRTKPhases) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Requirements Analysis (SRA)', )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKPhase.set_attributes().")