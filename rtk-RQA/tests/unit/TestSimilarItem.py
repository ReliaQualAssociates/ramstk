#!/usr/bin/env python -O
"""
This is the test class for testing Similat Item module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestSimilarItem.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from analyses.similar_item.SimilarItem import Model, SimilarItem

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestSimilarItemModel(unittest.TestCase):
    """
    Class for testing the SimilarItem data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the SimilarItem class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestSimilarItem) __init__ should return a Similar Item model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.hardware_id, None)
        self.assertEqual(self.DUT.sia_id, None)
        self.assertEqual(self.DUT.from_quality, 0)
        self.assertEqual(self.DUT.to_quality, 0)
        self.assertEqual(self.DUT.from_environment, 0)
        self.assertEqual(self.DUT.to_environment, 0)
        self.assertEqual(self.DUT.from_temperature, 30.0)
        self.assertEqual(self.DUT.to_temperature, 30.0)
        self.assertEqual(self.DUT.change_desc_1, 'No changes')
        self.assertEqual(self.DUT.change_factor_1, 1.0)
        self.assertEqual(self.DUT.change_desc_2, 'No changes')
        self.assertEqual(self.DUT.change_factor_2, 1.0)
        self.assertEqual(self.DUT.change_desc_3, 'No changes')
        self.assertEqual(self.DUT.change_factor_3, 1.0)
        self.assertEqual(self.DUT.change_desc_4, 'No changes')
        self.assertEqual(self.DUT.change_factor_4, 1.0)
        self.assertEqual(self.DUT.change_desc_5, 'No changes')
        self.assertEqual(self.DUT.change_factor_5, 1.0)
        self.assertEqual(self.DUT.change_desc_6, 'No changes')
        self.assertEqual(self.DUT.change_factor_6, 1.0)
        self.assertEqual(self.DUT.change_desc_7, 'No changes')
        self.assertEqual(self.DUT.change_factor_7, 1.0)
        self.assertEqual(self.DUT.change_desc_8, 'No changes')
        self.assertEqual(self.DUT.change_factor_8, 1.0)
        self.assertEqual(self.DUT.change_desc_9, 'No changes')
        self.assertEqual(self.DUT.change_factor_9, 1.0)
        self.assertEqual(self.DUT.change_desc_10, 'No changes')
        self.assertEqual(self.DUT.change_factor_10, 1.0)
        self.assertEqual(self.DUT.function_1, '')
        self.assertEqual(self.DUT.function_2, '')
        self.assertEqual(self.DUT.function_3, '')
        self.assertEqual(self.DUT.function_4, '')
        self.assertEqual(self.DUT.function_5, '')
        self.assertEqual(self.DUT.result_1, 0.0)
        self.assertEqual(self.DUT.result_2, 0.0)
        self.assertEqual(self.DUT.result_3, 0.0)
        self.assertEqual(self.DUT.result_4, 0.0)
        self.assertEqual(self.DUT.result_5, 0.0)
        self.assertEqual(self.DUT.user_blob_1, None)
        self.assertEqual(self.DUT.user_blob_2, None)
        self.assertEqual(self.DUT.user_blob_3, None)
        self.assertEqual(self.DUT.user_blob_4, None)
        self.assertEqual(self.DUT.user_blob_5, None)
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
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.method, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestSimilarItem) set_attributes should return a 0 error code on success
        """

        _values = (0, 0, 0, 0, 0, 0, 30.0, 30.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0, '',
                   '', '', '', '', 0.0, 0.0, 0.0, 0.0, 0.0, 'User blob 1',
                   'User blob 2', 'User blob 3', 'User blob 4', 'User blob 5',
                   0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 1, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestSimilarItem) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 0, 0, 0, 0, 0, 30.0, 30.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0, '',
                   '', '', '', '', 0.0, 0.0, 0.0, 0.0, None, 'User blob 1',
                   'User blob 2', 'User blob 3', 'User blob 4', 'User blob 5',
                   0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 1, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestSimilarItem) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 0, 0, 0, 0, 0, 30.0, 30.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0, '',
                   '', '', '', '', 0.0, 0.0, 0.0, 0.0, 0.0, 'User blob 1',
                   'User blob 2', 'User blob 3', 'User blob 4', 'User blob 5',
                   0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestSimilarItem) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, 0, 0, 0, 0, 30.0, 30.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0, '',
                   '', '', '', '', 0.0, 0.0, 0.0, 0.0, 0.0, None, None,
                   None, None, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0,
                   0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestSimilarItem) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 0, 0, 0, 0, 0, 30.0, 30.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0,
                   'No changes', 1.0, 'No changes', 1.0, 'No changes', 1.0, '',
                   '', '', '', '', 0.0, 0.0, 0.0, 0.0, 0.0, 'User blob 1',
                   'User blob 2', 'User blob 3', 'User blob 4', 'User blob 5',
                   0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 1)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)

    @attr(all=True, unit=True)
    def test_topic_633(self):
        """
        (TestSimilarItem) topic_633 should return False on success.
        """

        self.DUT.from_environment = 1
        self.DUT.to_environment = 3
        self.DUT.from_quality = 4
        self.DUT.to_quality = 3
        self.DUT.from_temperature = 42.8
        self.DUT.to_temperature = 31.5

        self.assertFalse(self.DUT.topic_633(0.005))

        self.assertEqual(self.DUT.change_factor_1, 2.5)
        self.assertEqual(self.DUT.change_factor_2, 0.3)
        self.assertEqual(self.DUT.change_factor_3, 1.1)

        self.assertAlmostEqual(self.DUT.result_1, 0.00606060)

    @attr(all=True, unit=True)
    def test_user_defined(self):
        """
        (TestSimilarItem) user_defined should return False on success.
        """

        self.DUT.function_1 = 'hr * pi1 * pi2 * pi3 * pi4 * pi5 * pi6'
        self.DUT.function_2 = 'hr * pi4 * pi5 * pi6 * (uf1 / uf2)'

        self.DUT.change_factor_1 = 0.95
        self.DUT.change_factor_2 = 1.10
        self.DUT.change_factor_3 = 0.85
        self.DUT.change_factor_4 = 0.90
        self.DUT.change_factor_5 = 1.05
        self.DUT.change_factor_6 = 1.15
        self.DUT.user_float_1 = 3.5
        self.DUT.user_float_2 = 1.25

        self.assertFalse(self.DUT.user_defined(0.005))

        self.assertAlmostEqual(self.DUT.result_1, 0.00482652)
        self.assertAlmostEqual(self.DUT.result_2, 0.01521449)


class TestSimilarItemController(unittest.TestCase):
    """
    Class for testing the SimilarItem data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the SimilarItem class.
        """

        self.DUT = SimilarItem()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestSimilarItem) __init__ should create a SimilarItem data controller
        """

        self.assertTrue(isinstance(self.DUT, SimilarItem))
        self.assertEqual(self.DUT.dicSimilarItem, {})
        self.assertEqual(self.DUT.dao, None)
