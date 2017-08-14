#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKStatus.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing the RTKStatus module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKStatus import RTKStatus

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKStatus(unittest.TestCase):
    """
    Class for testing the RTKStatus class.
    """

    attributes = (1, 'Initiated',
                  'Incident has been initiated.', 'incident')

    def setUp(self):
        """
        Sets up the test fixture for the RTKStatus class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKStatus).first()
        self.DUT.name = self.attributes[1]
        self.DUT.description = self.attributes[2]
        self.DUT.type = self.attributes[3]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKStatus_create(self):
        """
        (TestRTKStatus) __init__ should create an RTKStatus model
        """

        self.assertTrue(isinstance(self.DUT, RTKStatus))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_status')
        self.assertEqual(self.DUT.status_id, 1)
        self.assertEqual(self.DUT.name, 'Initiated')
        self.assertEqual(self.DUT.description, 'Incident has been initiated.')
        self.assertEqual(self.DUT.type, 'incident')

    @attr(all=True, unit=True)
    def test01_RTKStatus_get_attributes(self):
        """
        (TestRTKStatus) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKStatus_set_attributes(self):
        """
        (TestRTKStatus) set_attributes should return a zero error code on success
        """

        _attributes = ('Reviewed', 'Incident has been reviewed.', 'inicident')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKStatus {0:d} " \
                               "attributes.".format(self.DUT.status_id))

    @attr(all=True, unit=True)
    def test02b_RTKStatus_set_attributes_to_few(self):
        """
        (TestRTKStatus) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Reviewed', 'Incident has been reviewed.')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKStatus.set_attributes().")
