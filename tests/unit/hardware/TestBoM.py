#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestBoM.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing Hardware BoM module algorithms and models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from treelib import Tree
from hardware.BoM import Model, BoM
import hardware.component.capacitor.variable.Variable as Variable

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "weibullguy" Rowland'


class TestBoMController(unittest.TestCase):
    """
    Class for testing the BoM data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the BoM class.
        """

        self.DUT = Model()                  # Hardware BoM type.
        self.CUT = BoM()

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)
        self.DUT.dao = self._dao

    @attr(all=True, static=True)
    def test00a_model_create(self):
        """
        (TestBoM) __init__ should create a BoM data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        # Verify class attributes are properly initialized.
        self.assertTrue(isinstance(self.DUT.dicHardware[100][101],
                                   Variable.AirTrimmer))

        self.assertEqual(self.DUT.bom_type, 0)
        self.assertEqual(self.DUT.dao, self._dao)
        self.assertEqual(self.DUT.hazard_rate_system, 0.0)
        self.assertEqual(self.DUT.revision_id, None)
        self.assertTrue(isinstance(self.DUT.tree, Tree))

    @attr(all=True, static=True)
    def test00b_controller_create(self):
        """
        (TestBoM) __init__ should create a BoM data controller
        """

        self.assertTrue(isinstance(self.CUT, BoM))

        self.assertEqual(self.CUT.dicBoM, {})

    @attr(all=False, static=False)
    def test01_build_function_bom(self):
        """
        (TestBoM) build_bom should return a 0 error code on success when building the Function BoM.
        """

        _error_code = self.DUT.build_bom(0)

        self.assertEqual(_error_code, 0)
        #self.assertEqual(self.DUT.tree.depth(), 3)

    @attr(all=False, static=False)
    def test02_build_requirement_bom(self):
        """
        (TestBoM) build_bom should return a 0 error code on success when building the Requirement BoM.
        """

        _error_code = self.DUT.build_bom(0)

        self.assertEqual(_error_code, 0)
        #self.assertEqual(self.DUT.tree.depth(), 3)

    @attr(all=True, static=True)
    def test03_build_hardware_bom(self):
        """
        (TestBoM) build_bom should return a 0 error code on success when building the Hardware BoM.
        """

        self.DUT.bom_type = 2

        _error_code = self.DUT.build_bom(0)

        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.tree.depth(), 3)

    @attr(all=False, static=False)
    def test04_build_software_bom(self):
        """
        (TestBoM) build_bom should return a 0 error code on success when building the Software BoM.
        """

        _error_code = self.DUT.build_bom(0)

        self.assertEqual(_error_code, 0)
        #self.assertEqual(self.DUT.tree.depth(), 3)

    @attr(all=True, static=True)
    def test05_save_bom(self):
        """
        (TestBoM) save_bom should return a 0 error code on success
        """

        _error_code = self.DUT.save_bom()

        self.assertEqual(_error_code, 10)
        #self.assertEqual(self.DUT.tree.depth(), 3)

    @attr(all=True, dynamic=True)
    def test06_request_bom(self):
        """
        (TestBoM) request_bom should return a 0 error code on success when building the Software BoM.
        """

        _error_code = self.CUT.request_bom(0, 2, self._dao)

        self.assertEqual(_error_code, 0)
        # self.assertEqual(self.DUT.tree.depth(), 3)