#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._dao.TestRTKAction.py is part of The RTK Project
#
# All rights reserved.
"""
This is the test class for testing the RTKAction module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk",
)

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

    _attributes = {
        'mode_id': 1,
        'action_due_date': date.today() + timedelta(days=30),
        'action_approve_date': date.today() + timedelta(days=30),
        'action_status': u'0',
        'action_closed': 0,
        'action_taken': '',
        'action_close_date': date.today() + timedelta(days=30),
        'action_recommended': 'Recommended action for Failure Cause #1',
        'action_category': 0,
        'action_owner': u'0',
        'cause_id': 1,
        'action_id': 1,
        'action_approved': 0
    }

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
        self.assertEqual(self.DUT.action_recommended,
                         'Recommended action for Failure Cause #1')
        self.assertEqual(self.DUT.action_category, 0)
        self.assertEqual(self.DUT.action_owner, '0')
        self.assertEqual(
            self.DUT.action_due_date, date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.action_status, '0')
        self.assertEqual(self.DUT.action_taken, '')
        self.assertEqual(self.DUT.action_approved, 0)
        self.assertEqual(
            self.DUT.action_approve_date, date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.action_closed, 0)
        self.assertEqual(
            self.DUT.action_close_date, date.today() + timedelta(days=30))

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKAction) get_attributes should return a tuple of attribute values.
        """
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKAction) set_attributes should return a zero error code on success
        """
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKAction {0:d} " \
                               "attributes.".format(self.DUT.action_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_key(self):
        """
        (TestRTKAction) set_attributes should return a 40 error code when passed a dict with a missing key.
        """
        self._attributes.pop('action_taken')
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute 'action_taken' "
                         "in attribute dictionary passed to "
                         "RTKAction.set_attributes().")
