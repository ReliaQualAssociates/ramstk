#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKSimilarItem.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKSimilarItem module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKSimilarItem import RTKSimilarItem

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKSimilarItem(unittest.TestCase):
    """
    Class for testing the RTKSimilarItem class.
    """

    _attributes =(1, 'Test Change Description 1', '', '', '', '', '', '', '',
                  '', '', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0,
                  0, '', '', '', '', '', 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  30.0, 30.0, '', '', '', '', '', 0.0, 0.0, 0.0, 0.0, 0.0, 0,
                  0, 0, 0, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKSimilarItem class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKSimilarItem).first()
        self.DUT.change_description_1 = self._attributes[1]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtksimilaritem_create(self):
        """
        (TestRTKSimilarItem) __init__ should create an RTKSimilarItem model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSimilarItem))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_similar_item')
        self.assertEqual(self.DUT.hardware_id, 1)
        self.assertEqual(self.DUT.change_description_1,
                         'Test Change Description 1')
        self.assertEqual(self.DUT.change_description_2, '')
        self.assertEqual(self.DUT.change_description_3, '')
        self.assertEqual(self.DUT.change_description_4, '')
        self.assertEqual(self.DUT.change_description_5, '')
        self.assertEqual(self.DUT.change_description_6, '')
        self.assertEqual(self.DUT.change_description_7, '')
        self.assertEqual(self.DUT.change_description_8, '')
        self.assertEqual(self.DUT.change_description_9, '')
        self.assertEqual(self.DUT.change_description_10, '')
        self.assertEqual(self.DUT.change_factor_1, 1.0)
        self.assertEqual(self.DUT.change_factor_2, 1.0)
        self.assertEqual(self.DUT.change_factor_3, 1.0)
        self.assertEqual(self.DUT.change_factor_4, 1.0)
        self.assertEqual(self.DUT.change_factor_5, 1.0)
        self.assertEqual(self.DUT.change_factor_6, 1.0)
        self.assertEqual(self.DUT.change_factor_7, 1.0)
        self.assertEqual(self.DUT.change_factor_8, 1.0)
        self.assertEqual(self.DUT.change_factor_9, 1.0)
        self.assertEqual(self.DUT.change_factor_10, 1.0)
        self.assertEqual(self.DUT.environment_from_id, 0)
        self.assertEqual(self.DUT.environment_to_id, 0)
        self.assertEqual(self.DUT.function_1, '')
        self.assertEqual(self.DUT.function_2, '')
        self.assertEqual(self.DUT.function_3, '')
        self.assertEqual(self.DUT.function_4, '')
        self.assertEqual(self.DUT.function_5, '')
        self.assertEqual(self.DUT.method_id, 0)
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.quality_from_id, 0)
        self.assertEqual(self.DUT.quality_to_id, 0)
        self.assertEqual(self.DUT.result_1, 0.0)
        self.assertEqual(self.DUT.result_2, 0.0)
        self.assertEqual(self.DUT.result_3, 0.0)
        self.assertEqual(self.DUT.result_4, 0.0)
        self.assertEqual(self.DUT.result_5, 0.0)
        self.assertEqual(self.DUT.temperature_from, 30.0)
        self.assertEqual(self.DUT.temperature_to, 30.0)
        self.assertEqual(self.DUT.user_blob_1, '')
        self.assertEqual(self.DUT.user_blob_2, '')
        self.assertEqual(self.DUT.user_blob_3, '')
        self.assertEqual(self.DUT.user_blob_4, '')
        self.assertEqual(self.DUT.user_blob_5, '')
        self.assertEqual(self.DUT.user_float_1, 0.0)
        self.assertEqual(self.DUT.user_float_2, 0.0)
        self.assertEqual(self.DUT.user_float_3, 0.0)
        self.assertEqual(self.DUT.user_float_4, 0.0)
        self.assertEqual(self.DUT.user_float_5, 0.0)
        self.assertEqual(self.DUT.user_int_1, 0)
        self.assertEqual(self.DUT.user_int_2, 0)
        self.assertEqual(self.DUT.user_int_3, 0)
        self.assertEqual(self.DUT.user_int_4, 0)
        self.assertEqual(self.DUT.user_int_5, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKSimilarItem) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKSimilarItem) set_attributes should return a zero error code on success
        """

        _attributes = ('Test Change Description 1', '', '', '', '', '', '', '',
                       '', '', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       1.0, 0, 0, '', '', '', '', '', 0, 0, 0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 30.0, 30.0, '', '', '', '', '', 0.0, 0.0,
                       0.0, 0.0, 0.0, 0, 0, 0, 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKSimilarItem {0:d} " \
                               "attributes.".format(self.DUT.hardware_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKSimilarItem) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('Test Change Description 1', '', '', '', '', '', '', '',
                       '', '', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       1.0, 0, 0, '', '', '', '', '', 0, 0, 0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 30.0, 'None', '', '', '', '', '', 0.0,
                       0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKSimilarItem " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKSimilarItem) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Test Change Description 1', '', '', '', '', '', '', '',
                       '', '', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       1.0, 0, 0, '', '', '', '', '', 0, 0, 0, 0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 30.0, 30.0, '', '', '', '', '', 0.0, 0.0,
                       0.0, 0.0, 0.0, 0, 0, 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKSimilarItem.set_attributes().")
