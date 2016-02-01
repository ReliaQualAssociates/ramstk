#!/usr/bin/env python -O
"""
This is the test class for testing Incident Component module algorithms and
models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestIncidentComponent.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from incident.component.Component import Model, Component

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestIncidentComponentModel(unittest.TestCase):
    """
    Class for testing the IncidentComponent data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the IncidentComponent class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestIncidentComponent) __init__ should return an IncidentComponent model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.lstRelevant, [-1, -1, -1, -1, -1, -1, -1, -1,
                                                -1, -1, -1, -1, -1, -1, -1, -1,
                                                -1, -1, -1, -1])
        self.assertEqual(self.DUT.lstChargeable, [-1, -1, -1, -1, -1, -1, -1,
                                                  -1, -1, -1])
        self.assertEqual(self.DUT.incident_id, None)
        self.assertEqual(self.DUT.component_id, None)
        self.assertEqual(self.DUT.age_at_incident, 0.0)
        self.assertEqual(self.DUT.failure, 0)
        self.assertEqual(self.DUT.suspension, 0)
        self.assertEqual(self.DUT.cnd_nff, 0)
        self.assertEqual(self.DUT.occ_fault, 0)
        self.assertEqual(self.DUT.initial_installation, 0)
        self.assertEqual(self.DUT.interval_censored, 0)
        self.assertEqual(self.DUT.use_op_time, 0)
        self.assertEqual(self.DUT.use_cal_time, 0)
        self.assertEqual(self.DUT.ttf, 0.0)
        self.assertEqual(self.DUT.mode_type, 0)
        self.assertEqual(self.DUT.relevant, -1)
        self.assertEqual(self.DUT.chargeable, -1)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestIncidentComponent) set_attributes should return a 0 error code on success
        """

        _values = (1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestIncidentComponent) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, None, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestIncidentComponent) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestIncidentComponent) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (None, None, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, -1,
                          -1, [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                              -1, -1, -1, -1, -1, -1, -1, -1],
                             [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestIncidentComponent) get_attributes(set_attributes(values)) == values
        """

        _values = (1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0)
        _results = (1, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0,
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        self.DUT.set_attributes(_values)
        self.assertEqual(self.DUT.get_attributes(), _results)


class TestIncidentComponentController(unittest.TestCase):
    """
    Class for testing the Incident Component data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Incident Component class.
        """

        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Component()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestIncidentComponent) __init__ should create a Incident Component data controller
        """

        self.assertTrue(isinstance(self.DUT, Component))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicComponents, {})

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
