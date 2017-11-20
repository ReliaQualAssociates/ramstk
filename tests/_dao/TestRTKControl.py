#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._dao.TestRTKControl.py is part of The RTK Project
#
# All rights reserved.
"""
This is the test class for testing the RTKControl module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKControl import RTKControl

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKControl(unittest.TestCase):
    """
    Class for testing the RTKControl class.
    """

    _attributes = {'cause_id': 1, 'mode_id': 1, 'description': 'Test Control', 'control_id': 1, 'type_id': 0}

    def setUp(self):
        """
        Sets up the test fixture for the RTKControl class.
        """
        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKControl).first()
        self.DUT.description = 'Test Control'

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkcontrol_create(self):
        """
        (TestRTKControl) __init__ should create an RTKControl model.
        """
        self.assertTrue(isinstance(self.DUT, RTKControl))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_control')
        self.assertEqual(self.DUT.mode_id, 1)
        self.assertEqual(self.DUT.cause_id, 1)
        self.assertEqual(self.DUT.control_id, 1)
        self.assertEqual(self.DUT.description, 'Test Control')
        self.assertEqual(self.DUT.type_id, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKControl) get_attributes should return a tuple of attribute values.
        """
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKControl) set_attributes should return a zero error code on success
        """
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKControl {0:d} " \
                               "attributes.".format(self.DUT.control_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_key(self):
        """
        (TestRTKControl) set_attributes should return a 40 error code when passed a dict with a missing key.
        """
        self._attributes.pop('type_id')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute 'type_id' in "
                               "attribute dictionary passed to "
                               "RTKControl.set_attributes().")


