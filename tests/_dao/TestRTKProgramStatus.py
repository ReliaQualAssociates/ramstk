#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKProgramStatus.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKProgramStatus module algorithms and models."""

from datetime import date, timedelta

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from nose.plugins.attrib import attr

from rtk.dao.RTKProgramStatus import RTKProgramStatus

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKProgramStatus(unittest.TestCase):
    """Class for testing the RTKProgramStatus database table."""

    _attributes = {
        'cost_remaining': 100.0,
        'date_status': date.today(),
        'time_remaining': 0.0,
        'revision_id': 1,
        'status_id': 1
    }

    def setUp(self):
        """Set up the test fixture for the RTKProgramStatus class."""
        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKProgramStatus).first()
        self.DUT.cost_remaining = self._attributes['cost_remaining']

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkvalidation_create(self):
        """(TestRTKProgramStatus) __init__ should create an RTKProgramStatus model."""
        self.assertTrue(isinstance(self.DUT, RTKProgramStatus))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_program_status')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.status_id, 1)
        self.assertEqual(self.DUT.cost_remaining, 100.0)
        self.assertEqual(self.DUT.date_status, date.today())
        self.assertEqual(self.DUT.time_remaining, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """(TestRTKProgramStatus) get_attributes should return a dict of attribute values."""
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """(TestRTKProgramStatus) set_attributes should return a zero error code on success."""
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKProgramStatus {0:d} "
                         "attributes.".format(self.DUT.revision_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_key(self):
        """(TestRTKProgramStatus) set_attributes should return a 40 error code when passed a dict with a missing key."""
        self._attributes.pop('time_remaining')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute 'time_remaining' "
                         "in attribute dictionary passed to "
                         "RTKProgramStatus.set_attributes().")

        self._attributes['time_remaining'] = 0.0
