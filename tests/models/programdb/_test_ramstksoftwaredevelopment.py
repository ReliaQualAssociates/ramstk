#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRAMSTKSoftwareDevelopment.py is part of The RAMSTK
#       Project

#
# All rights reserved.
"""
This is the test class for testing the RAMSTKSoftwareDevelopment module algorithms
and models.
"""

# Standard Library Imports
import sys
import unittest
from os.path import dirname

# Third Party Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# RAMSTK Package Imports
from dao.RAMSTKSoftwareDevelopment import RAMSTKSoftwareDevelopment
from nose.plugins.attrib import attr

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/ramstk",
)




__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'


class TestRAMSTKSoftwareDevelopment(unittest.TestCase):
    """
    Class for testing the RAMSTKSoftwareDevelopment class.
    """

    _attributes = (1, 1, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RAMSTKSoftwareDevelopment class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.ramstk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RAMSTKSoftwareDevelopment).first()

        session.commit()

    @attr(all=True, unit=True)
    def test00_ramstksoftware_create(self):
        """
        (TestRAMSTKSoftwareDevelopment) __init__ should create an RAMSTKSoftwareDevelopment model.
        """

        self.assertTrue(isinstance(self.DUT, RAMSTKSoftwareDevelopment))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'ramstk_software_development')
        self.assertEqual(self.DUT.software_id, 1)
        self.assertEqual(self.DUT.question_id, 1)
        self.assertEqual(self.DUT.answer, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRAMSTKSoftwareDevelopment) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRAMSTKSoftwareDevelopment) set_attributes should return a zero error code on success
        """

        _attributes = (0, )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RAMSTK SUCCESS: Updating " \
                               "RAMSTKSoftwareDevelopment {0:d} " \
                               "attributes.".format(self.DUT.software_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRAMSTKSoftwareDevelopment) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('one', )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RAMSTK ERROR: Incorrect data type when " \
                               "converting one or more " \
                               "RAMSTKSoftwareDevelopment attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRAMSTKSoftwareDevelopment) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ()

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RAMSTK ERROR: Insufficient number of input " \
                               "values to " \
                               "RAMSTKSoftwareDevelopment.set_attributes().")
