#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKUser.py is part of The RTK Project

#
# All rights reserved.
"""
This is the test class for testing the RTKUser module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk",
)

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKGroup import RTKGroup

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKGroup(unittest.TestCase):
    """
    Class for testing the RTKGroup class.
    """

    attributes = (1, 'Engineering, Design', 'workgroup')

    def setUp(self):
        """
        Sets up the test fixture for the RTKUser class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKGroup).first()
        self.DUT.description = self.attributes[1]
        self.DUT.group_type = self.attributes[2]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkworkgroup_create(self):
        """
        (TestRTKGroup) __init__ should create an RTKGroup model
        """

        self.assertTrue(isinstance(self.DUT, RTKGroup))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_group')
        self.assertEqual(self.DUT.group_id, 1)
        self.assertEqual(self.DUT.description, 'Engineering, Design')
        self.assertEqual(self.DUT.group_type, 'workgroup')

    @attr(all=True, unit=True)
    def test01_rtkworkgroup_get_attributes(self):
        """
        (TestRTKGroup) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_rtkworkgroup_set_attributes(self):
        """
        (TestRTKGroup) set_attributes should return a zero error code on success
        """

        _attributes = ('Engineering, Reliability', 'workgroup')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKGroup {0:d} " \
                               "attributes.".format(    self.DUT.group_id))

    @attr(all=True, unit=True)
    def test02b_rtkworkgroup_set_attributes_to_few(self):
        """
        (TestRTKGroup) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Durability', )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKGroup.set_attributes().")
