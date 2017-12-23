#!/usr/bin/env python -O
"""
This is the test class for testing the Physics of Failure (PoF) class.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestPoF.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from analyses.pof.PhysicsOfFailure import PoF, ParentError

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestPoFController(unittest.TestCase):
    """
    Class for testing the PoF data controller class.
    """

    def setUp(self):

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = PoF()
        self.DUT._dao = self._dao

    @attr(all=True, integration=True)
    def test00_request_pof(self):
        """
        (TestPoF) request_pof should return False on success
        """

        self.assertFalse(self.DUT.request_pof(self._dao, 0))

    @attr(all=True, integration=True)
    def test01_request_pof_parent_problem(self):
        """
        (TestPoF) request_pof raises ParentError for None input
        """

        self.assertRaises(ParentError, self.DUT.request_pof, self._dao, None)

    @attr(all=True, integration=True)
    def test02_request_pof_parent_with_no_mechanisms(self):
        """
        (TestPoF) request_pof returns False for an assembly with no failure mechanisms
        """

        self.assertFalse(self.DUT.request_pof(self._dao, 10))

    @attr(all=True, integration=True)
    def test03_add_pof(self):
        """
        (TestPoF) add_pof returns False on success
        """

        self.assertFalse(self.DUT.add_pof(0))

    @attr(all=True, integration=False)
    def test04_add_mechanism(self):
        """
        (TestPoF) add_mechanism returns 0 on successful add
        """

        self.DUT.request_pof(self._dao, 0)
        (_results, _error_code, _last_id) = self.DUT.add_mechanism(0)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test05_delete_mechanism(self):
        """
        (TestPoF) delete_mechanism returns 0 on successful delete
        """

        self.DUT.request_pof(self._dao, 0)
        (_results, _error_code, _last_id) = self.DUT.add_mechanism(0)

        self.assertEqual(self.DUT.delete_mechanism(0, _last_id), (True, 0))

    @attr(all=True, integration=True)
    def test06_delete_non_existent_mechanism(self):
        """
        (TestPoF) delete_mechanism returns 60 when trying to delete non-existant mechanism
        """

        self.DUT.request_pof(self._dao, 0)

        self.assertEqual(self.DUT.delete_mechanism(0, 1000), (True, 60))

    @attr(all=True, integration=True)
    def test07_save_mechanism(self):
        """
        (TestPoF) _save_mechanism should return False on success
        """

        self.DUT.request_pof(self._dao, 0)

        _mechanism = self.DUT.dicPoF[0].dicMechanisms[1]
        _values = (0, 0, 'Test Mechanism')
        _mechanism.set_attributes(_values)

        self.assertFalse(self.DUT._save_mechanism(_mechanism))

    @attr(all=True, integration=True)
    def test08_add_load(self):
        """
        (TestPoF) add_load should return False on success
        """

        self.DUT.request_pof(self._dao, 0)

        (_results, _error_code, _last_id) = self.DUT.add_load(0, 4)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test09_delete_load(self):
        """
        (TestPoF) delete_load returns (True, 0) on success
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        (_results, _error_code, _last_id) = self.DUT.add_load(0, _mechanism_id)

        self.assertEqual(
            self.DUT.delete_load(0, _mechanism_id, _last_id), (True, 0))

    @attr(all=True, integration=True)
    def test10_delete_non_existent_load(self):
        """
        (TestPoF) delete_load returns (True, 60) when attempting to delete a non-existent load
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id

        self.assertEqual(
            self.DUT.delete_load(0, _mechanism_id, 1000), (True, 60))

    @attr(all=True, integration=True)
    def test11_save_load(self):
        """
        (TestPoF) _save_load should return False on success
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        _n = max(
            self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads.keys())
        _load = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[_n]
        _values = (10, 0, 'Load Description', 2, 5)
        _load.set_attributes(_values)

        self.assertFalse(self.DUT._save_load(_load))

    @attr(all=True, integration=True)
    def test12_add_stress(self):
        """
        (TestPoF) add_stress should return False on success
        """

        self.DUT.request_pof(self._dao, 0)

        (_results, _error_code, _last_id) = self.DUT.add_stress(0, 4, 5)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test13_delete_stress(self):
        """
        (TestPoF) delete_stress returns (True, 0) on success
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_n].dicLoads.keys())
        _load_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[
            _n].load_id
        (_results, _error_code, _last_id) = self.DUT.add_stress(
            0, _mechanism_id, _load_id)

        self.assertEqual(
            self.DUT.delete_stress(0, _mechanism_id, _load_id, _last_id),
            (True, 0))

    @attr(all=True, integration=True)
    def test14_delete_non_existent_stress(self):
        """
        (TestPoF) delete_stress returns (True, 60) when trying to delete a non-existent stress
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_n].dicLoads.keys())
        _load_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[
            _n].load_id

        self.assertEqual(
            self.DUT.delete_stress(0, _mechanism_id, _load_id, 1000),
            (True, 60))

    @attr(all=True, integration=True)
    def test15_save_stress(self):
        """
        (TestPoF) _save_stress should return False on success
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_n].dicLoads.keys())
        _load_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[
            _n].load_id

        (_results, _error_code, _last_id) = self.DUT.add_stress(
            0, _mechanism_id, _load_id)
        _stress = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[
            _load_id].dicStresses[_last_id]

        _values = (3, _last_id, 'Stress Description', 2, 3, 'Remarks')
        _stress.set_attributes(_values)

        self.assertFalse(self.DUT._save_stress(_stress))

    @attr(all=True, integration=True)
    def test16_add_method(self):
        """
        (TestPoF) add_method should return False on success
        """

        self.DUT.request_pof(self._dao, 0)

        (_results, _error_code, _last_id) = self.DUT.add_method(0, 1, 0, 0)
        self.assertEqual(_error_code, 0)

    @attr(all=False, integration=False)
    def test17_delete_method(self):
        """
        (TestPoF) delete_method returns (True, 0) on success
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_n].dicLoads.keys())
        _load_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[
            _n].load_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[
            _load_id].dicStresses.keys())
        _stress_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[
            _load_id].dicStresses[_n].stress_id

        (_results, _error_code, _last_id) = self.DUT.add_method(
            0, _mechanism_id, _load_id, _stress_id)

        self.assertEqual(
            self.DUT.delete_method(0, _mechanism_id, _load_id, _stress_id,
                                   _last_id), (True, 0))

    @attr(all=True, integration=True)
    def test19_delete_non_existent_method(self):
        """
        (TestPoF) delete_method returns (True, 60) when trying to delete a non-existent method
        """

        self.DUT.request_pof(self._dao, 0)
        _n = max(self.DUT.dicPoF[0].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicPoF[0].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_n].dicLoads.keys())
        _load_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[
            _n].load_id
        _n = max(self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[
            _load_id].dicStresses.keys())
        _stress_id = self.DUT.dicPoF[0].dicMechanisms[_mechanism_id].dicLoads[
            _load_id].dicStresses[_n].stress_id

        self.assertEqual(
            self.DUT.delete_method(0, _mechanism_id, _load_id, _stress_id,
                                   1000), (True, 60))

    @attr(all=False, integration=True)
    def test20_save_method(self):
        """
        (TestPoF) _save_method should return False on success
        """

        self.DUT.request_pof(self._dao, 0)

        _method = self.DUT.dicPoF[0].dicMechanisms[1].dicLoads[1].dicStresses[
            3].dicMethods[0]

        _values = (3, 17, 'Test Description', 'Test Boundary Conditions',
                   'Test Remarks')
        _method.set_attributes(_values)

        self.assertFalse(self.DUT._save_method(_method))

    @attr(all=False, integration=True)
    def test21_save_pof(self):
        """
        (TestPoF) _save_pof should return False on success
        """

        self.DUT.request_pof(self._dao, 0)

        self.assertFalse(self.DUT.save_pof(0))
