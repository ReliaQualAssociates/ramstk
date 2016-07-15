#!/usr/bin/env python -O
"""
This is the test class for testing the FMEA class.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.integration.TestFMEA.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao

from analyses.fmea.FMEA import FMEA, ParentError

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2016 Andrew "weibullguy" Rowland'


class TestFMEAController(unittest.TestCase):
    """
    Class for testing the FMEA data controller class.
    """

    def setUp(self):

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = FMEA()
        self.DUT.dao = self._dao

        self._mode_id = None
        self._mechanism_id = None
        self._cause_id = None

    @attr(all=True, integration=True)
    def test0_request_function_fmea(self):
        """
        (TestFMEA) request_fmea for a Function should return False on success
        """

        self.assertFalse(self.DUT.request_fmea(None, 0))

    @attr(all=True, integration=True)
    def test1_request_hardware_fmea(self):
        """
        (TestFMEA) request_fmea for a Hardware should return False on success
        """

        self.assertFalse(self.DUT.request_fmea(0))

    @attr(all=True, integration=True)
    def test2_request_fmea_parent_problem(self):
        """
        (TestFMEA) __init__ raises ParentError for None, None or int, int input
        """

        self.assertRaises(ParentError, self.DUT.request_fmea, None, None)
        self.assertRaises(ParentError, self.DUT.request_fmea, 2, 10)

    @attr(all=True, integration=True)
    def test3_request_fmea_mode_no_mechanisms(self):
        """
        (TestFMEA) __init__ raises ParentError for Mode with no mechanisms
        """

        self.assertRaises(ParentError, self.DUT.request_fmea, 3, 10)

    @attr(all=True, integration=True)
    def test4_add_function_mode(self):
        """
        (TestFMEA) add_mode returns 0 on successful add to a function
        """

        self.DUT.request_fmea(None, 0)
        (_results, _error_code, _last_id) = self.DUT.add_mode(None, 0)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test5_add_hardware_mode(self):
        """
        (TestFMEA) add_mode returns 0 on successful add to a hardware item
        """

        self.DUT.request_fmea(0)
        (_results, _error_code, _last_id) = self.DUT.add_mode(0, None)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test6_delete_function_mode(self):
        """
        (TestFMEA) delete_mode returns 0 on successful delete from a function
        """

        self.DUT.request_fmea(None, 0)
        (_results, _error_code, _last_id) = self.DUT.add_mode(None, 0)

        self.assertEqual(self.DUT.delete_mode(_last_id, None, 0), (True, 0))

    @attr(all=True, integration=True)
    def test7_delete_hardware_mode(self):
        """
        (TestFMEA) delete_mode returns 0 on successful delete from a hardware item
        """

        self.DUT.request_fmea(0)
        (_results, _error_code, _last_id) = self.DUT.add_mode(0, None)

        self.assertEqual(self.DUT.delete_mode(_last_id, 0), (True, 0))

    @attr(all=True, integration=True)
    def test8_delete_non_existent_mode(self):
        """
        (TestFMEA) delete_mode returns 60 when trying to delete non-existant mode
        """

        self.DUT.request_fmea(None, 0)
        _n = len(self.DUT.dicFFMEA[0].dicModes)
        try:
            _n = self.DUT.dicFFMEA[0].dicModes.keys()[_n - 1]
        except IndexError:
            return
        _mode_id = self.DUT.dicFFMEA[0].dicModes[_n].mode_id

        self.assertEqual(self.DUT.delete_mode(_mode_id + 1, None, 0),
                         (True, 60))

        self.DUT.request_fmea(0)
        self.assertEqual(self.DUT.delete_mode(100, 0),
                         (True, 60))

    @attr(all=True, integration=True)
    def test9_save_mode(self):
        """
        (TestFMEA) _save_mode should return False on success
        """

        self.DUT.request_fmea(0, None)
        _n = max(self.DUT.dicDFMEA[0].dicModes.keys())
        _mode = self.DUT.dicDFMEA[0].dicModes[_n]
        _values = (0, 0, 0, 'Test Mode', 'Mission', 'Mission Phase', 'Local',
                   'Next', 'End', 'Detection Method', 'Other Indications',
                   'Isolation Method', 'Design Provisions', 'Operator Actions',
                   'Severity Class', 'Hazard Rate Source', 'Mode Probability',
                   1.0, 0.0, 0.0, 0.0, 0.0, 10, 10, 0, 0, 'Remarks')
        _mode.set_attributes(_values)

        self.assertFalse(self.DUT._save_mode(_mode))

    @attr(all=True, integration=True)
    def test10_add_mechanism(self):
        """
        (TestFMEA) add_mechanism should return False on success
        """

        self.DUT.request_fmea(0, None)
        (_results, _error_code, _mode_id) = self.DUT.add_mode(0, None)

        (_results,
         _error_code,
         _last_id) = self.DUT.add_mechanism(0, _mode_id)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test11_delete_mechanism(self):
        """
        (TestFMEA) delete_mechanism returns (True, 0) on success
        """

        self.DUT.request_fmea(0)
        _n = max(self.DUT.dicDFMEA[0].dicModes.keys())
        _mode_id = self.DUT.dicDFMEA[0].dicModes[_n].mode_id
        (_results,
         _error_code,
         _last_id) = self.DUT.add_mechanism(0, _mode_id)

        self.assertEqual(self.DUT.delete_mechanism(0, _mode_id, _last_id),
                         (True, 0))

    @attr(all=True, integration=True)
    def test12_save_mechanism(self):
        """
        (TestFMEA) _save_mechanism should return False on success
        """

        self.DUT.request_fmea(0)

        _n = max(self.DUT.dicDFMEA[0].dicModes.keys())
        _mode_id = self.DUT.dicDFMEA[0].dicModes[_n].mode_id
        _m = max(self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms.keys())
        _mechanism = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_m]

        _values = (10, 0, 'Mechanism Description', 5, 6, 180, 6, 5, 180, 0)
        _mechanism.set_attributes(_values)

        self.assertFalse(self.DUT._save_mechanism(_mechanism))

    @attr(all=True, integration=True)
    def test13_calculate_mechanism(self):
        """
        (TestFMEA) _calculate should return False on success and set rpn=100 and new rpn=80
        """

        self.DUT.request_fmea(0)

        _n = max(self.DUT.dicDFMEA[0].dicModes.keys())
        _mode_id = self.DUT.dicDFMEA[0].dicModes[_n].mode_id
        _m = max(self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms.keys())
        _mechanism = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_m]

        _values = (10, 0, 'Mechanism Description', 4, 5, 0, 4, 4, 0, 0)
        _mechanism.set_attributes(_values)

        self.assertFalse(_mechanism.calculate(5, 5))
        self.assertEqual(_mechanism.rpn, 100)
        self.assertEqual(_mechanism.rpn_new, 80)

    @attr(all=True, integration=True)
    def test14_add_cause(self):
        """
        (TestFMEA) add_cause should return False on success
        """

        self.DUT.request_fmea(0, None)
        (_results, _error_code, _mode_id) = self.DUT.add_mode(0, None)

        (_results, _error_code,
         _mechanism_id) = self.DUT.add_mechanism(0, _mode_id)

        (_results,
         _error_code,
         _last_id) = self.DUT.add_cause(0, _mode_id, _mechanism_id)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test15_delete_cause(self):
        """
        (TestFMEA) delete_cause returns (True, 0) on success
        """

        self.DUT.request_fmea(0)
        _n = max(self.DUT.dicDFMEA[0].dicModes.keys())
        _mode_id = self.DUT.dicDFMEA[0].dicModes[_n].mode_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_n].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_n].mechanism_id
        (_results,
         _error_code,
         _last_id) = self.DUT.add_cause(0, _mode_id, _mechanism_id)

        self.assertEqual(self.DUT.delete_cause(0, _mode_id, _mechanism_id,
                                               _last_id), (True, 0))

    @attr(all=True, integration=True)
    def test16_save_cause(self):
        """
        (TestFMEA) _save_cause should return False on success
        """

        self.DUT.request_fmea(0)
        _n = max(self.DUT.dicDFMEA[0].dicModes.keys())
        _mode_id = self.DUT.dicDFMEA[0].dicModes[_n].mode_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_n].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_n].mechanism_id

        (_results,
         _error_code,
         _last_id) = self.DUT.add_cause(0, _mode_id, _mechanism_id)
        _cause = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses[_last_id]

        _values = (10, 3, 2, 'Cause Description', 5, 6, 180, 6, 5, 180)
        _cause.set_attributes(_values)

        self.assertFalse(self.DUT._save_cause(_cause))

    @attr(all=True, integration=True)
    def test17_add_control(self):
        """
        (TestFMEA) add_control should return False on success
        """

        self.DUT.request_fmea(0, None)
        (_results, _error_code, _mode_id) = self.DUT.add_mode(0, None)

        (_results, _error_code,
         _mechanism_id) = self.DUT.add_mechanism(0, _mode_id)

        (_results,
         _error_code,
         _cause_id) = self.DUT.add_cause(0, _mode_id, _mechanism_id)

        (_results,
         _error_code,
         _last_id) = self.DUT.add_control(0, _mode_id, _mechanism_id,
                                          _cause_id)
        self.assertEqual(_error_code, 0)

    @attr(all=False, integration=False)
    def test18_delete_control(self):
        """
        (TestFMEA) delete_control returns (True, 0) on success
        """

        self.DUT.request_fmea(0)
        _n = max(self.DUT.dicDFMEA[0].dicModes.keys())
        _mode_id = self.DUT.dicDFMEA[0].dicModes[_n].mode_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses.keys())
        _cause_id = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses[_n].cause_id

        (_results,
         _error_code,
         _last_id) = self.DUT.add_control(0, _mode_id, _mechanism_id,
                                          _cause_id)

        self.assertEqual(self.DUT.delete_control(0, _mode_id, _mechanism_id,
                                                 _last_id), (True, 0))

    @attr(all=False, integration=False)
    def test19_save_control(self):
        """
        (TestFMEA) _save_control should return False on success
        """

        self.DUT.request_fmea(0)

        _n = max(self.DUT.dicDFMEA[0].dicModes.keys())
        _mode_id = self.DUT.dicDFMEA[0].dicModes[_n].mode_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_n].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses.keys())
        _cause_id = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses[_n].cause_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses[_cause_id].dicControls.keys())
        _control = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses[_cause_id].dicControls[_n]

        _values = (10, 3, 2, 1, 'Control Description', 1)
        _control.set_attributes(_values)

        self.assertFalse(self.DUT._save_control(_control))

    @attr(all=True, integration=True)
    def test20_add_action(self):
        """
        (TestFMEA) add_action should return False on success
        """

        self.DUT.request_fmea(0, None)
        _n = max(self.DUT.dicDFMEA[0].dicModes.keys())
        _mode_id = self.DUT.dicDFMEA[0].dicModes[_n].mode_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses.keys())
        _cause_id = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses[_n].cause_id

        (_results,
         _error_code,
         _last_id) = self.DUT.add_action(0, _mode_id, _mechanism_id, _cause_id)
        self.assertEqual(_error_code, 0)

    @attr(all=False, integration=False)
    def test21_delete_action(self):
        """
        (TestFMEA) delete_action returns (True, 0) on success
        """

        self.DUT.request_fmea(0)

        _n = max(self.DUT.dicDFMEA[0].dicModes.keys())
        _mode_id = self.DUT.dicDFMEA[0].dicModes[_n].mode_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_n].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses.keys())
        _cause_id = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses[_n].cause_id

        (_results,
         _error_code,
         _last_id) = self.DUT.add_action(0, _mode_id, _mechanism_id, _cause_id)

        self.assertEqual(self.DUT.delete_action(0, _mode_id, _mechanism_id,
                                                _cause_id, _last_id),
                         (True, 0))

    @attr(all=False, integration=True)
    def test22_save_action(self):
        """
        (TestFMEA) _save_action should return False on success
        """

        self.DUT.request_fmea(0)

        _n = max(self.DUT.dicDFMEA[0].dicModes.keys())
        _mode_id = self.DUT.dicDFMEA[0].dicModes[_n].mode_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_n].dicMechanisms.keys())
        _mechanism_id = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_n].mechanism_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses.keys())
        _cause_id = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses[_n].cause_id
        _n = max(self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses[_cause_id].dicActions.keys())
        _action = self.DUT.dicDFMEA[0].dicModes[_mode_id].dicMechanisms[_mechanism_id].dicCauses[_cause_id].dicActions[_n]

        _values = (10, 3, 2, 1, 'Action Recomended', 1, 11, 0, 0,
                   'Action Taken', 0, 0, 0, 0)
        _action.set_attributes(_values)

        self.assertFalse(self.DUT._save_action(_action))

    @attr(all=False, integration=True)
    def test23_copy_control(self):
        """
        (TestFMEA) _copy_control should return False on success
        """

        self.DUT.request_fmea(0)

        _ni = len(self.DUT.dicDFMEA.keys())

        self.assertFalse(self.DUT.copy_fmea(2, 0))

        _nf = len(self.DUT.dicDFMEA.keys())

        self.assertEqual(_ni + 1, _nf)

