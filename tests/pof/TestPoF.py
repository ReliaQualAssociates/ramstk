#!/usr/bin/env python -O
"""
This is the test class for testing the Physics of Failure (PoF) class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.pof.TestPoF.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao

from analyses.pof.PhysicsOfFailure import *


class TestPoFModel(unittest.TestCase):
    """
    Class for testing the Physics of Failure model class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the PoF model class.
        """

        self.DUT = Model(0)

    @attr(all=True, unit=True)
    def test_PoF_create(self):
        """
        (TestPoF) __init__ should return instance of PoF data model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT.dicMechanisms, {})
        self.assertEqual(self.DUT.assembly_id, 0)

    @attr(all=True, unit=True)
    def test_PoF_create_parent_problem(self):
        """
        (TestPoF) __init__ raises ParentError for None input
        """

        self.assertRaises(ParentError, Model, None)


class TestPoFController(unittest.TestCase):
    """
    Class for testing the PoF data controller class.
    """

    def setUp(self):

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = PoF()
        self.DUT._dao = self._dao

    @attr(all=True, unit=True)
    def test_create_controller(self):
        """
        (TestPoF) __init__ should return instance of PoF data controller
        """

        self.assertEqual(self.DUT.dicPoF, {})

    @attr(all=True, integration=True)
    def test_request_pof(self):
        """
        (TestPoF) request_pof should return False on success
        """

        self.assertFalse(self.DUT.request_pof(self._dao, 0))

    @attr(all=True, integration=True)
    def test_request_pof_parent_problem(self):
        """
        (TestPoF) request_pof raises ParentError for None input
        """

        self.assertRaises(ParentError, self.DUT.request_pof, self._dao,
                          None)

    @attr(all=True, integration=True)
    def test_request_pof_parent_with_no_mechanisms(self):
        """
        (TestPoF) request_pof returns False for an assembly with no failure mechanisms
        """

        self.assertFalse(self.DUT.request_pof(self._dao, 10))

    @attr(all=True, integration=True)
    def test_add_pof(self):
        """
        (TestPoF) add_pof returns False on success
        """

        self.assertFalse(self.DUT.add_pof(0))

    @attr(all=True, integration=True)
    def test_add_mechanism(self):
        """
        (TestPoF) add_mechanism returns 0 on successful add
        """

        self.DUT.request_pof(self._dao, 0)
        (_results, _error_code, _last_id) = self.DUT.add_mechanism(0)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_delete_mechanism(self):
        """
        (TestPoF) delete_mechanism returns 0 on successful delete
        """

        self.DUT.request_pof(self._dao, 0)
        (_results, _error_code, _last_id) = self.DUT.add_mechanism(0)

        self.assertEqual(self.DUT.delete_mechanism(0, _last_id), (True, 0))

    @attr(all=True, integration=True)
    def test_delete_non_existent_mechanism(self):
        """
        (TestPoF) delete_mechanism returns 60 when trying to delete non-existant mechanism
        """

        self.DUT.request_pof(self._dao, 0)

        self.assertEqual(self.DUT.delete_mechanism(0, 1000),
                         (True, 60))

    @attr(all=True, integration=True)
    def test_save_mechanism(self):
        """
        (TestPoF) _save_mechanism should return False on success
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism = self.DUT.dicPoF[0].dicMechanisms[_n]
        _values = (0, 0, 'Test Mechanism')
        _mechanism.set_attributes(_values)

        self.assertFalse(self.DUT._save_mechanism(_mechanism))

    @attr(all=True, integration=True)
    def test_add_load(self):
        """
        (TestPoF) add_load should return False on success
        """

        self.DUT.request_pof(self._dao, 0)
        (_results, _error_code, _mechanism_id) = self.DUT.add_mechanism(0)

        (_results, _error_code, _last_id) = self.DUT.add_load(0, _mechanism_id)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_delete_load(self):
        """
        (TestPoF) delete_load returns (True, 0) on success
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        (_results, _error_code, _last_id) = self.DUT.add_load(0, _mechanism_id)

        self.assertEqual(self.DUT.delete_load(0, _mechanism_id, _last_id),
                         (True, 0))

    @attr(all=True, integration=True)
    def test_delete_non_existent_load(self):
        """
        (TestPoF) delete_load returns (True, 60) when attempting to delete a non-existent load
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id

        self.assertEqual(self.DUT.delete_load(0, _mechanism_id, 1000),
                         (True, 60))

    @attr(all=True, integration=True)
    def test_save_load(self):
        """
        (TestPoF) _save_load should return False on success
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads.keys())
        _load = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[_n]
        _values = (10, 0, 'Load Description', 2, 5)
        _load.set_attributes(_values)

        self.assertFalse(self.DUT._save_load(_load))

    @attr(all=True, integration=True)
    def test_add_stress(self):
        """
        (TestPoF) add_stress should return False on success
        """

        self.DUT.request_pof(self._dao, 0)
        (_results, _error_code, _mechanism_id) = self.DUT.add_mechanism(0)

        (_results, _error_code, _load_id) = self.DUT.add_load(0, _mechanism_id)

        (_results,
         _error_code,
         _last_id) = self.DUT.add_stress(0, _mechanism_id, _load_id)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_delete_stress(self):
        """
        (TestPoF) delete_stress returns (True, 0) on success
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_n].dicLoads.keys())
        _load_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[_n].load_id
        (_results,
         _error_code,
         _last_id) = self.DUT.add_stress(0, _mechanism_id, _load_id)

        self.assertEqual(self.DUT.delete_stress(0, _mechanism_id, _load_id,
                                                _last_id), (True, 0))

    @attr(all=True, integration=True)
    def test_delete_non_existent_stress(self):
        """
        (TestPoF) delete_stress returns (True, 60) when trying to delete a non-existent stress
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_n].dicLoads.keys())
        _load_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[_n].load_id

        self.assertEqual(self.DUT.delete_stress(0, _mechanism_id, _load_id,
                                                1000), (True, 60))

    @attr(all=True, integration=True)
    def test_save_stress(self):
        """
        (TestPoF) _save_stress should return False on success
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_n].dicLoads.keys())
        _load_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[_n].load_id

        (_results,
         _error_code,
         _last_id) = self.DUT.add_stress(0, _mechanism_id, _load_id)
        _stress = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[_load_id].dicStresses[_last_id]

        _values = (3, _last_id, 'Stress Description', 2, 3, 'Remarks')
        _stress.set_attributes(_values)

        self.assertFalse(self.DUT._save_stress(_stress))

    @attr(all=True, integration=True)
    def test_add_method(self):
        """
        (TestPoF) add_method should return False on success
        """

        self.DUT.request_pof(self._dao, 0)

        (_results, _error_code,
         _last_id) = self.DUT.add_method(0, 630, 83, 3)
        self.assertEqual(_error_code, 0)

    @attr(all=False, integration=False)
    def test_delete_method(self):
        """
        (TestPoF) delete_method returns (True, 0) on success
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_n].dicLoads.keys())
        _load_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[_n].load_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[_load_id].dicStresses.keys())
        _stress_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[_load_id].dicStresses[_n].stress_id

        (_results,
         _error_code,
         _last_id) = self.DUT.add_method(0, _mechanism_id,
                                         _load_id, _stress_id)

        self.assertEqual(self.DUT.delete_method(0, _mechanism_id, _load_id,
                                                _stress_id, _last_id),
                         (True, 0))

    @attr(all=True, integration=True)
    def test_delete_non_existent_method(self):
        """
        (TestPoF) delete_method returns (True, 60) when trying to delete a non-existent method
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_n].dicLoads.keys())
        _load_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[_n].load_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[_load_id].dicStresses.keys())
        _stress_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[_load_id].dicStresses[_n].stress_id

        self.assertEqual(self.DUT.delete_method(0, _mechanism_id, _load_id,
                                                _stress_id, 1000),
                         (True, 60))

    @attr(all=False, integration=True)
    def test_save_method(self):
        """
        (TestPoF) _save_method should return False on success
        """

        self.DUT.request_pof(self._dao, 0)

        _method = self.DUT.dicPoF[0].dicMechanisms[630].dicLoads[83].dicStresses[3].dicMethods[17]

        _values = (3, 17, 'Test Description', 'Test Boundary Conditions',
                   'Test Remarks')
        _method.set_attributes(_values)

        self.assertFalse(self.DUT._save_method(_method))

    @attr(all=False, integration=True)
    def test_save_pof(self):
        """
        (TestPoF) _save_pof should return False on success
        """

        self.DUT.request_pof(self._dao, 0)

        self.assertFalse(self.DUT.save_pof(0))
