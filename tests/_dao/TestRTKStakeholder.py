#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._dao.TestRTKStakeholder.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKStakeholder module algorithms and models."""

import sys
from os.path import dirname

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from dao.RTKStakeholder import RTKStakeholder

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKStakeholder(unittest.TestCase):
    """Class for testing the RTKStakeholder class."""

    _attributes = {
        'user_float_1': 0.0,
        'priority': 1,
        'group': u'',
        'description': 'Stakeholder Input',
        'planned_rank': 1,
        'stakeholder': u'',
        'improvement': 0.0,
        'customer_rank': 1,
        'user_float_5': 0.0,
        'user_float_4': 0.0,
        'user_float_3': 0.0,
        'user_float_2': 0.0,
        'stakeholder_id': 1,
        'overall_weight': 0.0,
        'revision_id': 1,
        'requirement_id': 0
    }

    def setUp(self):
        """Set up the test fixture for the RTKStakeholder class."""
        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKStakeholder).first()
        self.DUT.description = self._attributes['description']

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkstakeholder_create(self):
        """(TestRTKStakeholder) __init__ should create an RTKStakeholder model."""
        self.assertTrue(isinstance(self.DUT, RTKStakeholder))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_stakeholder')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.stakeholder_id, 1)
        self.assertEqual(self.DUT.customer_rank, 1)
        self.assertEqual(self.DUT.description, 'Stakeholder Input')
        self.assertEqual(self.DUT.group, '')
        self.assertEqual(self.DUT.improvement, 0.0)
        self.assertEqual(self.DUT.overall_weight, 0.0)
        self.assertEqual(self.DUT.planned_rank, 1)
        self.assertEqual(self.DUT.priority, 1)
        self.assertEqual(self.DUT.requirement_id, 0)
        self.assertEqual(self.DUT.stakeholder, '')
        self.assertEqual(self.DUT.user_float_1, 0.0)
        self.assertEqual(self.DUT.user_float_2, 0.0)
        self.assertEqual(self.DUT.user_float_3, 0.0)
        self.assertEqual(self.DUT.user_float_4, 0.0)
        self.assertEqual(self.DUT.user_float_5, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """(TestRTKStakeholder) get_attributes should return a tuple of attribute values."""
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """(TestRTKStakeholder) set_attributes should return a zero error code on success."""
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKStakeholder {0:d} "
                         "attributes.".format(self.DUT.stakeholder_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_key(self):
        """(TestRTKStakeholder) set_attributes should return a 40 error code when passed a dict with a missing key."""
        self._attributes.pop('user_float_1')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute 'user_float_1' "
                         "in attribute dictionary passed to "
                         "RTKStakeholder.set_attributes().")

        self._attributes['user_float_1'] = 0.0
