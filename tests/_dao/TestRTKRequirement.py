#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._dao.TestRTKRequirement.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKRequirement module algorithms and models."""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk",
)

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKRequirement import RTKRequirement

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKRequirement(unittest.TestCase):
    """Class for testing the RTKRequirement class."""

    _attributes = {
        'owner': u'',
        'priority': 0,
        'parent_id': 0,
        'requirement_code': 'REL-0001',
        'q_complete_4': 0,
        'requirement_type': u'',
        'q_complete_5': 0,
        'validated_date': date.today(),
        'revision_id': 1,
        'requirement_id': 1,
        'q_consistent_8': 0,
        'q_consistent_7': 0,
        'q_consistent_6': 0,
        'q_consistent_5': 0,
        'q_consistent_4': 0,
        'q_consistent_3': 0,
        'q_consistent_2': 0,
        'q_consistent_1': 0,
        'q_clarity_3': 0,
        'specification': u'',
        'q_complete_0': 0,
        'q_complete_1': 0,
        'q_complete_2': 0,
        'q_complete_3': 0,
        'page_number': u'',
        'figure_number': u'',
        'q_complete_6': 0,
        'q_complete_7': 0,
        'q_complete_8': 0,
        'q_complete_9': 0,
        'q_consistent_0': 0,
        'q_clarity_6': 0,
        'q_clarity_7': 0,
        'q_clarity_4': 0,
        'q_clarity_5': 0,
        'q_clarity_2': 0,
        'description': 'REL-0001',
        'q_clarity_0': 0,
        'q_clarity_1': 0,
        'q_verifiable_4': 0,
        'derived': 0,
        'q_verifiable_0': 0,
        'q_verifiable_1': 0,
        'q_clarity_8': 0,
        'q_verifiable_3': 0,
        'q_verifiable_2': 0,
        'validated': 0,
        'q_verifiable_5': 0
    }

    def setUp(self):
        """(TestRTKRequirement) Set up the test fixture for the RTKRequirement class."""
        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKRequirement).first()
        self.DUT.description = self._attributes['description']
        self.DUT.requirement_code = self._attributes['requirement_code']

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkrequirement_create(self):
        """(TestRTKRequirement) __init__ should create an RTKRequirement model."""
        self.assertTrue(isinstance(self.DUT, RTKRequirement))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_requirement')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.requirement_id, 1)
        self.assertEqual(self.DUT.derived, 0)
        self.assertEqual(self.DUT.description, 'REL-0001')
        self.assertEqual(self.DUT.figure_number, '')
        self.assertEqual(self.DUT.owner, '')
        self.assertEqual(self.DUT.page_number, '')
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.priority, 0)
        self.assertEqual(self.DUT.requirement_code, 'REL-0001')
        self.assertEqual(self.DUT.specification, '')
        self.assertEqual(self.DUT.requirement_type, '')
        self.assertEqual(self.DUT.validated, 0)
        self.assertEqual(self.DUT.validated_date, date.today())
        self.assertEqual(self.DUT.q_clarity_0, 0)
        self.assertEqual(self.DUT.q_clarity_1, 0)
        self.assertEqual(self.DUT.q_clarity_2, 0)
        self.assertEqual(self.DUT.q_clarity_3, 0)
        self.assertEqual(self.DUT.q_clarity_4, 0)
        self.assertEqual(self.DUT.q_clarity_5, 0)
        self.assertEqual(self.DUT.q_clarity_6, 0)
        self.assertEqual(self.DUT.q_clarity_7, 0)
        self.assertEqual(self.DUT.q_clarity_8, 0)
        self.assertEqual(self.DUT.q_complete_0, 0)
        self.assertEqual(self.DUT.q_complete_1, 0)
        self.assertEqual(self.DUT.q_complete_2, 0)
        self.assertEqual(self.DUT.q_complete_3, 0)
        self.assertEqual(self.DUT.q_complete_4, 0)
        self.assertEqual(self.DUT.q_complete_5, 0)
        self.assertEqual(self.DUT.q_complete_6, 0)
        self.assertEqual(self.DUT.q_complete_7, 0)
        self.assertEqual(self.DUT.q_complete_8, 0)
        self.assertEqual(self.DUT.q_complete_9, 0)
        self.assertEqual(self.DUT.q_consistent_0, 0)
        self.assertEqual(self.DUT.q_consistent_1, 0)
        self.assertEqual(self.DUT.q_consistent_2, 0)
        self.assertEqual(self.DUT.q_consistent_3, 0)
        self.assertEqual(self.DUT.q_consistent_4, 0)
        self.assertEqual(self.DUT.q_consistent_5, 0)
        self.assertEqual(self.DUT.q_consistent_6, 0)
        self.assertEqual(self.DUT.q_consistent_7, 0)
        self.assertEqual(self.DUT.q_consistent_8, 0)
        self.assertEqual(self.DUT.q_verifiable_0, 0)
        self.assertEqual(self.DUT.q_verifiable_1, 0)
        self.assertEqual(self.DUT.q_verifiable_2, 0)
        self.assertEqual(self.DUT.q_verifiable_3, 0)
        self.assertEqual(self.DUT.q_verifiable_4, 0)
        self.assertEqual(self.DUT.q_verifiable_5, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """(TestRTKRequirement) get_attributes should return a tuple of attribute values."""
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """(TestRTKRequirement) set_attributes should return a zero error code on success."""
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKRequirement {0:d} "
                         "attributes.".format(self.DUT.requirement_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_key(self):
        """(TestRTKRequirement) set_attributes() should return a 40 error code when passed a dict with a missing key."""
        self._attributes.pop('q_clarity_1')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute 'q_clarity_1' "
                         "in attribute dictionary passed to "
                         "RTKMechanism.set_attributes().")

        self._attributes['q_clarity_1'] = 0

    @attr(all=True, unit=True)
    def test03a_create_code(self):
        """(TestRTKRequirement) create_code should return False on success."""
        self.assertFalse(self.DUT.create_code('PERF'))
        self.assertEqual(self.DUT.requirement_code, 'PERF-0001')
