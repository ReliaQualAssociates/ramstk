#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKMatrix.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKMatrix module algorithms and models."""

import unittest
import sys

from os.path import dirname

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from nose.plugins.attrib import attr

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from dao.RTKMatrix import RTKMatrix  # pylint: disable=import-error

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKMatrix(unittest.TestCase):
    """Class for testing the RTKMatrix class."""

    _attributes = {
        'revision_id': 1,
        'matrix_id': 1,
        'column_id': 0,
        'column_item_id': 1,
        'matrix_type': 'fnctn_hrdwr',
        'parent_id': 0,
        'row_id': 0,
        'row_item_id': 1,
        'value': 10.0
    }

    def setUp(self):
        """Set up the test fixture for the RTKMatrix class."""
        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKMatrix).first()
        self.DUT.value = self._attributes['value']

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkmatrix_create(self):
        """(TestRTKMatrix) __init__ should create an RTKMatrix model."""
        self.assertTrue(isinstance(self.DUT, RTKMatrix))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_matrix')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.matrix_id, 1)
        self.assertEqual(self.DUT.column_id, 0)
        self.assertEqual(self.DUT.column_item_id, 1)
        self.assertEqual(self.DUT.matrix_type, 'fnctn_hrdwr')
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.row_id, 0)
        self.assertEqual(self.DUT.row_item_id, 1)
        self.assertEqual(self.DUT.value, 10.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """(TestRTKMatrix) get_attributes should return a tuple of attribute values."""
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """(TestRTKMatrix) set_attributes should return a zero error code on success."""
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKMatrix {0:d} "
                         "attributes.".format(self.DUT.matrix_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_mission_key(self):
        """(TestRTKMatrix) set_attributes should return a 40 error code when passed a dict with a missing key."""
        self._attributes.pop('matrix_type')
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(
            _msg, "RTK ERROR: Missing attribute 'matrix_type' in attribute "
            "dictionary passed to RTKMatrix.set_attributes().")
