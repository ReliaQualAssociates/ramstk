#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKLoadHistory.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing the RTKLoadHistory module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKLoadHistory import RTKLoadHistory

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKLoadHistory(unittest.TestCase):
    """
    Class for testing the RTKLoadHistory class.
    """

    attributes = (1, 'Cycle Counts')

    def setUp(self):
        """
        Sets up the test fixture for the RTKLoadHistory class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKLoadHistory).first()
        self.DUT.description = self.attributes[1]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKLoadHistory_create(self):
        """
        (TestRTKLoadHistory) __init__ should create an RTKLoadHistory model
        """

        self.assertTrue(isinstance(self.DUT, RTKLoadHistory))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_load_history')
        self.assertEqual(self.DUT.history_id, 1)
        self.assertEqual(self.DUT.description, 'Cycle Counts')

    @attr(all=True, unit=True)
    def test01_RTKLoadHistory_get_attributes(self):
        """
        (TestRTKLoadHistory) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKLoadHistory_set_attributes(self):
        """
        (TestRTKLoadHistory) set_attributes should return a zero error code on success
        """

        _attributes = ('Histogram, Bivariate', )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKLoadHistory {0:d} " \
                               "attributes.".format(self.DUT.history_id))

    @attr(all=True, unit=True)
    def test02b_RTKLoadHistory_set_attributes_to_few(self):
        """
        (TestRTKLoadHistory) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ()

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKLoadHistory.set_attributes().")
