#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRAMSTKIncidentDetail.py is part of The RAMSTK Project

#
# All rights reserved.
"""
This is the test class for testing the RAMSTKIncidentDetail module algorithms and
models.
"""

# Standard Library Imports
import sys
import unittest
from os.path import dirname

# Third Party Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# RAMSTK Package Imports
from dao.RAMSTKIncidentDetail import RAMSTKIncidentDetail
from nose.plugins.attrib import attr

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/ramstk",
)




__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'


class TestRAMSTKIncidentDetail(unittest.TestCase):
    """
    Class for testing the RAMSTKIncidentDetail class.
    """

    _attributes = (1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0.0, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RAMSTKIncidentDetail class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.ramstk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RAMSTKIncidentDetail).first()
        self.DUT.failure = self._attributes[4]

        session.commit()

    @attr(all=True, unit=True)
    def test00_ramstkincidentdetail_create(self):
        """
        (TestRAMSTKIncidentDetail) __Init__ should create an RAMSTKIncidentDetail model.
        """

        self.assertTrue(isinstance(self.DUT, RAMSTKIncidentDetail))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'ramstk_incident_detail')
        self.assertEqual(self.DUT.incident_id, 1)
        self.assertEqual(self.DUT.hardware_id, 0)
        self.assertEqual(self.DUT.age_at_incident, 0)
        self.assertEqual(self.DUT.failure, 1)
        self.assertEqual(self.DUT.suspension, 0)
        self.assertEqual(self.DUT.cnd_nff, 0)
        self.assertEqual(self.DUT.occ_fault, 0)
        self.assertEqual(self.DUT.initial_installation, 0)
        self.assertEqual(self.DUT.interval_censored, 0)
        self.assertEqual(self.DUT.use_op_time, 0)
        self.assertEqual(self.DUT.use_cal_time, 0)
        self.assertEqual(self.DUT.ttf, 0.0)
        self.assertEqual(self.DUT.mode_type_id, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRAMSTKIncidentDetail) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRAMSTKIncidentDetail) set_attributes should return a zero error code on success
        """

        _attributes = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RAMSTK SUCCESS: Updating RAMSTKIncidentDetail " \
                               "{0:d} attributes.".\
                         format(self.DUT.incident_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRAMSTKIncidentDetail) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0, 0, 0, 'zero', 0, 0, 0, 0, 0, 0.0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RAMSTK ERROR: Incorrect data type when " \
                               "converting one or more RAMSTKIncidentDetail " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRAMSTKIncidentDetail) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RAMSTK ERROR: Insufficient number of input " \
                               "values to RAMSTKIncidentDetail.set_attributes().")
