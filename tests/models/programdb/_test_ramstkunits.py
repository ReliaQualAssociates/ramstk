#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRAMSTKUnit.py is part of The RAMSTK Project

#
# All rights reserved.
"""
This is the test class for testing the RAMSTKUnit module algorithms and
models.
"""

# Standard Library Imports
import sys
import unittest
from os.path import dirname

# Third Party Imports
from nose.plugins.attrib import attr
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# RAMSTK Package Imports
from dao.RAMSTKUnit import RAMSTKUnit

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/ramstk",
)




__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'


class TestRAMSTKUnit(unittest.TestCase):
    """
    Class for testing the RAMSTKUnit class.
    """

    attributes = (1, 'lbf', 'Pounds Force', 'measurement')

    def setUp(self):
        """
        Sets up the test fixture for the RAMSTKUnit class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.ramstk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RAMSTKUnit).first()
        self.DUT.code = self.attributes[1]
        self.DUT.description = self.attributes[2]
        self.DUT.unit_type = self.attributes[3]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RAMSTKUnit_create(self):
        """
        (TestRAMSTKUnit) __init__ should create an RAMSTKUnit model
        """

        self.assertTrue(isinstance(self.DUT, RAMSTKUnit))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'ramstk_unit')
        self.assertEqual(self.DUT.unit_id, 1)
        self.assertEqual(self.DUT.description, 'Pounds Force')
        self.assertEqual(self.DUT.code, 'lbf')
        self.assertEqual(self.DUT.unit_type, 'measurement')

    @attr(all=True, unit=True)
    def test01_RAMSTKUnit_get_attributes(self):
        """
        (TestRAMSTKUnit) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RAMSTKUnit_set_attributes(self):
        """
        (TestRAMSTKUnit) set_attributes should return a zero error code on success
        """

        _attributes = ('N', 'Newtons', 'measurement')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RAMSTK SUCCESS: Updating RAMSTKUnit {0:d} " \
                               "attributes.".format(self.DUT.unit_id))

    @attr(all=True, unit=True)
    def test02b_RAMSTKUnits_set_attributes_to_few(self):
        """
        (TestRAMSTKUnits) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (
            'N',
            'Newtons',
        )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RAMSTK ERROR: Insufficient number of input " \
                               "values to RAMSTKUnit.set_attributes().")
