#!/usr/bin/env python -O
"""
This is the test class for testing Incident Component module algorithms and
models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestIncidentComponent.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from incident.component.Component import Component

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestIncidentComponentController(unittest.TestCase):
    """
    Class for testing the Incident Component data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Incident Component class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Component()

    @attr(all=True, integration=True)
    def test_request_components(self):
        """
        (TestIncidentComponent) request_components should return 0 on success
        """

        self.assertEqual(self.DUT.request_components(self._dao, 1)[1], 0)

    @attr(all=True, integration=True)
    def test_add_component(self):
        """
        (TestIncidentComponent) add_component should return 0 on success
        """

        self.assertEqual(self.DUT.request_components(self._dao, 1)[1], 0)
        self.assertEqual(self.DUT.add_component(1, 3)[1], 0)

    @attr(all=True, integration=True)
    def test_delete_component(self):
        """
        (TestIncidentComponent) delete_component should return 0 on success
        """

        self.assertEqual(self.DUT.request_components(self._dao, 1)[1], 0)
        _component = self.DUT.dicComponents[max(self.DUT.dicComponents.keys())]
        self.assertEqual(self.DUT.delete_component(_component.incident_id,
                                                   _component.component_id)[1],
                                                   0)

    @attr(all=True, integration=True)
    def test_save_component(self):
        """
        (TestIncidentComponent) save_component returns 0 on success
        """

        self.assertEqual(self.DUT.request_components(self._dao, 1)[1], 0)
        _component = self.DUT.dicComponents[min(self.DUT.dicComponents.keys())]
        _component.lstRelevant = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                                  1, 0, 0, 0, 0]
        _component.lstChargeable = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        (_results,
         _error_code) = self.DUT.save_component(_component.component_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_all_components(self):
        """
        (TestIncidentComponent) save_all_components returns 0 on success
        """

        self.assertEqual(self.DUT.request_components(self._dao, 1)[1], 0)
        self.assertFalse(self.DUT.save_all_components())
