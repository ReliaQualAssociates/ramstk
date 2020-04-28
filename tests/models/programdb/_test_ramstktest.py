#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRAMSTKTest.py is part of The RAMSTK Project

#
# All rights reserved.
"""
This is the test class for testing the RAMSTKTest module algorithms and
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
from dao.RAMSTKTest import RAMSTKTest
from nose.plugins.attrib import attr

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/ramstk",
)




__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'


class TestRAMSTKTest(unittest.TestCase):
    """
    Class for testing the RAMSTKTest class.
    """

    _attributes = (1, 1, 0, '', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 'Test Test Description', 0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 1, '', 0, 75.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RAMSTKTest class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.ramstk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RAMSTKTest).first()
        self.DUT.description = self._attributes[17]

        session.commit()

    @attr(all=True, unit=True)
    def test00_ramstktest_create(self):
        """
        (TestRAMSTKTest) __init__ should create an RAMSTKTest model.
        """

        self.assertTrue(isinstance(self.DUT, RAMSTKTest))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'ramstk_test')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.test_id, 1)
        self.assertEqual(self.DUT.assess_model_id, 0)
        self.assertEqual(self.DUT.attachment, '')
        self.assertEqual(self.DUT.avg_fef, 0.0)
        self.assertEqual(self.DUT.avg_growth, 0.0)
        self.assertEqual(self.DUT.avg_ms, 0.0)
        self.assertEqual(self.DUT.chi_square, 0.0)
        self.assertEqual(self.DUT.confidence, 0.0)
        self.assertEqual(self.DUT.consumer_risk, 0.0)
        self.assertEqual(self.DUT.cramer_vonmises, 0.0)
        self.assertEqual(self.DUT.cum_failures, 0)
        self.assertEqual(self.DUT.cum_mean, 0.0)
        self.assertEqual(self.DUT.cum_mean_ll, 0.0)
        self.assertEqual(self.DUT.cum_mean_se, 0.0)
        self.assertEqual(self.DUT.cum_mean_ul, 0.0)
        self.assertEqual(self.DUT.cum_time, 0.0)
        self.assertEqual(self.DUT.description, 'Test Test Description')
        self.assertEqual(self.DUT.grouped, 0)
        self.assertEqual(self.DUT.group_interval, 0.0)
        self.assertEqual(self.DUT.inst_mean, 0.0)
        self.assertEqual(self.DUT.inst_mean_ll, 0.0)
        self.assertEqual(self.DUT.inst_mean_se, 0.0)
        self.assertEqual(self.DUT.inst_mean_ul, 0.0)
        self.assertEqual(self.DUT.mg, 0.0)
        self.assertEqual(self.DUT.mgp, 0.0)
        self.assertEqual(self.DUT.n_phases, 1)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.plan_model_id, 0)
        self.assertEqual(self.DUT.prob, 75.0)
        self.assertEqual(self.DUT.producer_risk, 0.0)
        self.assertEqual(self.DUT.scale, 0.0)
        self.assertEqual(self.DUT.scale_ll, 0.0)
        self.assertEqual(self.DUT.scale_se, 0.0)
        self.assertEqual(self.DUT.scale_ul, 0.0)
        self.assertEqual(self.DUT.shape, 0.0)
        self.assertEqual(self.DUT.shape_ll, 0.0)
        self.assertEqual(self.DUT.shape_se, 0.0)
        self.assertEqual(self.DUT.shape_ul, 0.0)
        self.assertEqual(self.DUT.tr, 0.0)
        self.assertEqual(self.DUT.ttt, 0.0)
        self.assertEqual(self.DUT.ttff, 0.0)
        self.assertEqual(self.DUT.type_id, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRAMSTKTest) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRAMSTKTest) set_attributes should return a zero error code on success
        """

        _attributes = (0, '', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 'Test Test Description', 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1, '', 0, 75.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RAMSTK SUCCESS: Updating RAMSTKTest {0:d} " \
                               "attributes.".format(self.DUT.test_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRAMSTKTest) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0, '', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 'Test Test Description', 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1, '', 0, 75.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'None', 0.0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RAMSTK ERROR: Incorrect data type when " \
                               "converting one or more RAMSTKTest " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRAMSTKTest) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0, '', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 'Test Test Description', 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 1, '', 0, 75.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RAMSTK ERROR: Insufficient number of input " \
                               "values to RAMSTKTest.set_attributes().")
