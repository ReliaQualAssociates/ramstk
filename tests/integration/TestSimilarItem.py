#!/usr/bin/env python -O
"""
This is the test class for testing Similar Item module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestSimilarItem.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from analyses.similar_item.SimilarItem import SimilarItem

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestSimilarItemController(unittest.TestCase):
    """
    Class for testing the SimilarItem data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the SimilarItem class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = SimilarItem()

    @attr(all=True, integration=True)
    def test_request_similar_item(self):
        """
        (TestSimilarItem) request_similar_item should return 0 on success
        """

        self.assertEqual(self.DUT.request_similar_item(self._dao)[1], 0)

    @attr(all=True, integration=True)
    def test_add_similar_item(self):
        """
        (TestSimilarItem) add_similar_item should return (True, 0) on success
        """

        self.assertEqual(self.DUT.request_similar_item(self._dao)[1], 0)
        (_results,
         _error_code) = self.DUT.add_similar_item(4)

        self.assertTrue(isinstance(self.DUT.dicSimilarItem[self.DUT._last_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_calculate_topic_633(self):
        """
        (TestSimilarItem) calculate should return 0 on success when performing a Topic 6.3.3 analysis
        """

        self.DUT.request_similar_item(self._dao)
        self.DUT.dicSimilarItem[2].from_environment = 1
        self.DUT.dicSimilarItem[2].to_environment = 3
        self.DUT.dicSimilarItem[2].from_quality = 4
        self.DUT.dicSimilarItem[2].to_quality = 3
        self.DUT.dicSimilarItem[2].from_temperature = 42.8
        self.DUT.dicSimilarItem[2].to_temperature = 31.5

        self.assertFalse(self.DUT.calculate(2, 0.005, 1))

        self.assertEqual(self.DUT.dicSimilarItem[2].change_factor_1, 2.5)
        self.assertEqual(self.DUT.dicSimilarItem[2].change_factor_2, 0.3)
        self.assertEqual(self.DUT.dicSimilarItem[2].change_factor_3, 1.1)

        self.assertAlmostEqual(self.DUT.dicSimilarItem[2].result_1, 0.00606060)

    @attr(all=True, integration=True)
    def test_calculate_user_defined(self):
        """
        (TestSimilarItem) calculate should return 0 on success when performing a user-defined analysis
        """

        self.DUT.request_similar_item(self._dao)

        self.DUT.dicSimilarItem[2].function_1 = 'hr * pi1 * pi2 * pi3 * pi4 * pi5 * pi6'
        self.DUT.dicSimilarItem[2].function_2 = 'hr * pi4 * pi5 * pi6 * (uf1 / uf2)'

        self.DUT.dicSimilarItem[2].change_factor_1 = 0.95
        self.DUT.dicSimilarItem[2].change_factor_2 = 1.10
        self.DUT.dicSimilarItem[2].change_factor_3 = 0.85
        self.DUT.dicSimilarItem[2].change_factor_4 = 0.90
        self.DUT.dicSimilarItem[2].change_factor_5 = 1.05
        self.DUT.dicSimilarItem[2].change_factor_6 = 1.15
        self.DUT.dicSimilarItem[2].user_float_1 = 3.5
        self.DUT.dicSimilarItem[2].user_float_2 = 1.25

        self.assertFalse(self.DUT.calculate(2, 0.005, 2))

        self.assertAlmostEqual(self.DUT.dicSimilarItem[2].result_1, 0.00482652)
        self.assertAlmostEqual(self.DUT.dicSimilarItem[2].result_2, 0.01521449)

    @attr(all=True, integration=True)
    def test_save_similar_item(self):
        """
        (TestSimilarItem) save_similar_item returns (True, 0) on success
        """

        self.DUT.request_similar_item(self._dao)
        self.assertEqual(self.DUT.save_similar_item(2), (True, 0))

    @attr(all=True, integration=True)
    def test_save_all_similar_item(self):
        """
        (TestSimilarItem) save_all_similar_item returns False on success
        """

        self.DUT.request_similar_item(self._dao)
        self.assertFalse(self.DUT.save_all_similar_item())
