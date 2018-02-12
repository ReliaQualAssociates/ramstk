#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKFailureDefinition.py is part of The RTK Project

#
# All rights reserved.
"""Test class for testing the RTKFailureDefinition module algorithms and models."""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from rtk.dao.RTKFailureDefinition import RTKFailureDefinition

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKFailureDefinition(unittest.TestCase):
    """
    Class for testing the RTKFailureDefinition class.
    """

    _attributes = {
        'revision_id': 1,
        'definition_id': 1,
        'definition': 'Test Failure Definition'
    }

    def setUp(self):
        """
        Sets up the test fixture for the RTKFailureDefinition class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKFailureDefinition).first()
        self.DUT.definition = self._attributes['definition']

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkfailuredefinition_create(self):
        """(TestRTKFailureDefinition) __init__ should create an RTKFailureDefinition model."""
        self.assertTrue(isinstance(self.DUT, RTKFailureDefinition))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_failure_definition')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.definition_id, 1)
        self.assertEqual(self.DUT.definition, 'Test Failure Definition')

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """(TestRTKFailureDefinition) get_attributes should return a tuple of attribute values."""
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """(TestRTKFailureDefinition) set_attributes should return a zero error code on success."""
        self._attributes['definition'] = 'Failure Def.'

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKFailureDefinition " \
                               "{0:d} attributes.".\
                               format(self.DUT.definition_id))

        self._attributes['definition'] = 'Failure Definition'

    @attr(all=True, unit=True)
    def test02c_set_attributes_missing_key(self):
        """(TestRTKFailureDefinition) set_attributes should return a 40 error code when passed too few attributes."""
        self._attributes.pop('definition')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(
            _msg,
            "RTK ERROR: Missing attribute 'definition' in attribute " \
            "dictionary passed to RTKFailureDefinition.set_attributes()."
        )
