#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKAction.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKAction module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKAction import RTKAction

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKAction(unittest.TestCase):
    """
    Class for testing the RTKAction class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKAction class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKAction).first()
        self.DUT.cause_id = 1

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkaction_create(self):
        """
        (TestRTKAction) DUT should create an RTKAction model.
        """

        self.assertTrue(isinstance(self.DUT, RTKAction))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_action')
        self.assertEqual(self.DUT.mode_id, 1)
        self.assertEqual(self.DUT.cause_id, 1)
        self.assertEqual(self.DUT.action_id, 1)
        self.assertEqual(self.DUT.action_recommended, '')
        self.assertEqual(self.DUT.action_category, 0)
        self.assertEqual(self.DUT.action_owner, '0')
        self.assertEqual(self.DUT.action_due_date,
                         date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.action_status, '0')
        self.assertEqual(self.DUT.action_taken, '')
        self.assertEqual(self.DUT.action_approved, 0)
        self.assertEqual(self.DUT.action_approve_date,
                         date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.action_closed, 0)
        self.assertEqual(self.DUT.action_close_date,
                         date.today() + timedelta(days=30))

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKAction) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (1, 1, 1, '', 0, '0',
                          date.today() + timedelta(days=30),
                          '0', '', 0, date.today() + timedelta(days=30), 0,
                          date.today() + timedelta(days=30)))

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKAction) set_attributes should return a zero error code on success
        """

        _attributes = ('', 0, 0, date.today() + timedelta(days=30), 0, '', 0,
                       date.today() + timedelta(days=30), 0,
                       date.today() + timedelta(days=30))

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKAction {0:d} " \
                               "attributes.".format(self.DUT.action_id))

    @attr(all=True, unit=True)
    def test05b_set_attributes_wrong_type(self):
        """
        (TestRTKAction) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('', 0, 0, date.today() + timedelta(days=30), 0, '', 0,
                       date.today() + timedelta(days=30), 'None',
                       date.today() + timedelta(days=30))

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKAction " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test05c_set_attributes_too_few_passed(self):
        """
        (TestRTKAction) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('', 0, 0, date.today() + timedelta(days=30), 0, '', 0,
                       date.today() + timedelta(days=30), 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKAction.set_attributes().")
