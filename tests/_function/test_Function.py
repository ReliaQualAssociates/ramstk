# -*- coding: utf-8 -*-
#
#       tests.function.TestFunction.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test Class for Function data model and data controller."""

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree
import pandas as pd

import rtk.Utilities as Utilities
from rtk.Configuration import Configuration
from rtk.datamodels import RTKDataMatrix
from rtk.function import dtcFunction, dtmFunction
from rtk.dao import DAO
from rtk.dao import RTKFunction

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'


class TestFunctionDataModel(unittest.TestCase):
    """Class for testing the Function data model class."""

    def setUp(self):
        """Setup the test fixture for the Function class."""
        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {
            'host': 'localhost',
            'socket': 3306,
            'database': '/tmp/TestDB.rtk',
            'user': '',
            'password': ''
        }

        self.Configuration.DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
        self.Configuration.USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
            self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtmFunction(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """(TestFunctionModel) __init__ should return a Function model."""
        self.assertTrue(isinstance(self.DUT, dtmFunction))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """(TestFunctionModel): select_all() should return a Tree() object populated with RTKFunction instances on success."""
        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKFunction))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestFunctionModel): select() should return an instance of the RTKFunction data model on success."""
        self.DUT.select_all(1)
        _function = self.DUT.select(1)

        self.assertTrue(isinstance(_function, RTKFunction))
        self.assertEqual(_function.function_id, 1)
        self.assertEqual(_function.availability_logistics, 1.0)

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestFunctionModel): select() should return None when a non-existent Function ID is requested."""
        _function = self.DUT.select(100)

        self.assertEqual(_function, None)

    @attr(all=True, unit=True)
    def test03a_insert_sibling(self):
        """(TestFunctionModel): insert() should return False on success when inserting a sibling Function."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1, parent_id=0)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 4)

        self.DUT.delete(self.DUT.last_id)

    @attr(all=True, unit=True)
    def test03b_insert_child(self):
        """(TestFunctionModel): insert() should return False on success when inserting a child Function."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1, parent_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 4)

        self.DUT.delete(self.DUT.last_id)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestFunctionModel): delete() should return a zero error code on success."""
        self.DUT.select_all(1)
        self.DUT.insert(revision_id=1, parent_id=1)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestFunctionModel): delete() should return a non-zero error code when passed a Function ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'Function ID 300.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """(TestFunctionModel): update() should return a zero error code on success."""
        self.DUT.select_all(1)

        _function = self.DUT.tree.get_node(1).data
        _function.availability_logistics = 0.9832

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_update_non_existent_id(self):
        """(TestFunctionModel): update() should return a non-zero error code when passed a Function ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Function ID 100.')

    @attr(all=True, unit=True)
    def test_06a_update_all(self):
        """(TestFunctionModel): update_all() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test07a_calculate_mtbf(self):
        """(TestFunctionModel) calculate_mtbf should return a zero error code on success."""
        self.DUT.select_all(1)

        _function = self.DUT.select(1)
        _function.hazard_rate_logistics = 0.00000151
        _function.hazard_rate_mission = 0.000002

        _error_code, _msg = self.DUT.calculate_mtbf(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating MTBF metrics for '
                         'Function ID 1.')
        self.assertAlmostEqual(_function.mtbf_logistics, 662251.6556291)
        self.assertAlmostEqual(_function.mtbf_mission, 500000.0)

    @attr(all=True, unit=True)
    def test07b_calculate_mtbf_divide_by_zero(self):
        """(TestFunctionModel) calculate_mtbf should return a non-zero error code when attempting to divide by zero."""
        self.DUT.select_all(1)

        _function = self.DUT.select(1)
        _function.hazard_rate_mission = 0.0

        _error_code, _msg = self.DUT.calculate_mtbf(1)
        self.assertEqual(_error_code, 102)
        self.assertEqual(_msg, 'RTK ERROR: Zero Division Error when '
                         'calculating the mission MTBF for Function '
                         'ID 1.  Mission hazard rate: 0.000000.')

    @attr(all=True, unit=True)
    def test08a_calculate_availability(self):
        """(TestFunctionModel) calculate_availability should return False on success."""
        self.DUT.select_all(1)

        _function = self.DUT.tree.get_node(1).data
        _function.mpmt = 0.5
        _function.mcmt = 1.2
        _function.mttr = 5.8
        _function.mmt = 0.85
        _function.mtbf_logistics = 662251.6556291
        _function.mtbf_mission = 500000.0

        _error_code, _msg = self.DUT.calculate_availability(1)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating availability '
                         'metrics for Function ID 1.')
        self.assertAlmostEqual(_function.availability_logistics, 0.9999912)
        self.assertAlmostEqual(_function.availability_mission, 0.9999884)

    @attr(all=True, unit=True)
    def test08b_calculate_availability_divide_by_zero(self):
        """(TestFunctionModel) calculate_availability should return True when attempting to divide by zero."""
        self.DUT.select_all(1)

        _function = self.DUT.tree.get_node(1).data
        _function.mttr = 0.0
        _function.mtbf_logistics = 662251.6556291
        _function.mtbf_mission = 0.0

        _error_code, _msg = self.DUT.calculate_availability(1)
        self.assertEqual(_error_code, 102)
        self.assertEqual(_msg, 'RTK ERROR: Zero Division Error when '
                         'calculating the mission availability for '
                         'Function ID 1.  Mission MTBF: 0.000000 '
                         'MTTR: 0.000000.')


class TestFunctionDataController(unittest.TestCase):
    """Class for testing the Function Data Controller class."""

    def setUp(self):
        """Setup the test fixture for the Function Data Controller."""
        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {
            'host': 'localhost',
            'socket': 3306,
            'database': '/tmp/TestDB.rtk',
            'user': '',
            'password': ''
        }

        self.Configuration.RTK_DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG',
                                    '/tmp/RTK_debug.log')
        self.Configuration.RTK_USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO',
                                    '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
            self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtcFunction(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """(TestFunctionController) __init__ should return a Function Data Controller."""
        self.assertTrue(isinstance(self.DUT, dtcFunction))
        self.assertTrue(isinstance(self.DUT._dtm_data_model, dtmFunction))
        self.assertTrue(
            isinstance(self.DUT._dmx_fctn_hw_matrix, RTKDataMatrix))

    @attr(all=True, unit=True)
    def test01a_request_select_all(self):
        """(TestFunctionController) request_select_all() should return a Tree of RTKFunction models."""
        _tree = self.DUT.request_select_all(1)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKFunction))

    @attr(all=True, unit=True)
    def test01b_request_select_all_matrix(self):
        """(TestFunctionController) select_all_matrix() should return a tuple containing the matrix, column headings, and row headings."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'fnctn_hrdwr')

        self.assertTrue(isinstance(_matrix, pd.DataFrame))
        self.assertEqual(_column_hdrs, {1: u'S1', 2: u'S1:SS1', 3: u'S1:SS2'})
        self.assertEqual(_row_hdrs, {
            1: u'PRESS-001',
            2: u'FLOW-001',
            3: u'TEMP-001'
        })

    @attr(all=True, unit=True)
    def test02a_request_select(self):
        """(TestFunctionController) request_select() should return an RTKFunction model."""
        self.DUT.request_select_all(1)

        _function = self.DUT.request_select(1)

        self.assertTrue(isinstance(_function, RTKFunction))

    @attr(all=True, unit=True)
    def test02b_request_select_non_existent_id(self):
        """(TestFunctionController) request_select() should return None when requesting a Function that doesn't exist."""
        _function = self.DUT.request_select(100)

        self.assertEqual(_function, None)

    @attr(all=True, unit=True)
    def test03a_request_insert(self):
        """(TestFunctionController) request_insert() should return False on success."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_insert(revision_id=1, parent_id=0))

        self.DUT.request_delete(self.DUT.request_last_id())

    @attr(all=True, unit=True)
    def test03b_insert_matrix_row(self):
        """(TestFunctionController) request_insert_matrix() should return False on successfully inserting a row."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'fnctn_hrdwr')

        self.assertFalse(
            self.DUT.request_insert_matrix('fnctn_hrdwr', 4, 'Function Code'))
        self.assertEqual(self.DUT._dmx_fctn_hw_matrix.dic_row_hdrs[4],
                         'Function Code')

    @attr(all=True, unit=True)
    def test03c_insert_matrix_duplicate_row(self):
        """(TestFunctionController) request_insert_matrix() should return True when attempting to insert a duplicate row."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'fnctn_hrdwr')

        self.assertTrue(
            self.DUT.request_insert_matrix('fnctn_hrdwr', 2, 'Function Code'))

    @attr(all=True, unit=True)
    def test03d_insert_matrix_column(self):
        """(TestFunctionController) request_insert_matrix() should return False on successfully inserting a column."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'fnctn_hrdwr')

        self.assertFalse(
            self.DUT.request_insert_matrix(
                'fnctn_hrdwr', 4, 'S1:SS1:A1', row=False))
        self.assertEqual(self.DUT._dmx_fctn_hw_matrix.dic_column_hdrs[4],
                         'S1:SS1:A1')

    @attr(all=True, unit=True)
    def test04a_request_delete(self):
        """(TestFunctionController) request_delete() should return False on success."""
        self.DUT.request_select_all(1)
        self.DUT.request_insert(revision_id=1, parent_id=0)

        self.assertFalse(self.DUT.request_delete(self.DUT.request_last_id()))

    @attr(all=True, unit=True)
    def test04b_request_delete_non_existent_id(self):
        """(TestFunctionController) request_delete() should return True when attempting to delete a non-existent Function."""
        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=True)
    def test04c_request_delete_matrix_row(self):
        """(TestFunctionController) request_delete_matrix() should return False on successfully deleting a row."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'fnctn_hrdwr')
        self.DUT.request_insert_matrix('fnctn_hrdwr', 4, 'Function Code')

        self.assertFalse(self.DUT.request_delete_matrix('fnctn_hrdwr', 4))

    @attr(all=True, unit=True)
    def test04d_request_delete_matrix_non_existent_row(self):
        """(TestFunctionController) request_delete_matrix() should return True when attempting to delete a non-existent row."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'fnctn_hrdwr')

        self.assertTrue(self.DUT.request_delete_matrix('fnctn_hrdwr', 4))

    @attr(all=True, unit=True)
    def test04e_request_delete_matrix_column(self):
        """(TestFunctionController) request_delete_matrix() should return False on successfully deleting a column."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'fnctn_hrdwr')
        self.DUT.request_insert_matrix(
            'fnctn_hrdwr', 4, 'S1:SS1:A1', row=False)

        self.assertFalse(
            self.DUT.request_delete_matrix('fnctn_hrdwr', 4, row=False))

    @attr(all=True, unit=True)
    def test05a_request_update(self):
        """(TestFunctionController) request_update() should return False on success."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update(1))

    @attr(all=True, unit=True)
    def test05b_request_update_non_existent_id(self):
        """(TestFunctionController) request_update() should return True when attempting to save a non-existent Function."""
        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_update(100))

    @attr(all=True, unit=True)
    def test05c_request_update_matrix(self):
        """(TestFunctionController) request_update_matrix() should return False on success."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'fnctn_hrdwr')

        self.assertFalse(self.DUT.request_update_matrix(1, 'fnctn_hrdwr'))

    @attr(all=True, unit=True)
    def test05d_request_update_non_existent_matrix(self):
        """(TestFunctionController) request_update_matrix() should return True when attempting to update a non-existent matrix."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'fnctn_hrdwr')

        self.assertTrue(self.DUT.request_update_matrix(1, 'fnctn_sftwr'))

    @attr(all=True, unit=True)
    def test06a_request_update_all(self):
        """(TestFunctionController) request_update_all() should return False on success."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update_all())

    @attr(all=True, unit=True)
    def test07a_request_calculate_mtbf(self):
        """(TestFunctionController) request_calculate_mtbf() should return False on success."""
        self.DUT.request_select_all(1)

        _function = self.DUT.request_select(1)
        _function.hazard_rate_logistics = 0.00000151
        _function.hazard_rate_mission = 0.0000000152

        self.assertFalse(self.DUT.request_calculate_mtbf(1))

        self.assertAlmostEqual(_function.mtbf_logistics, 662251.6556291)
        self.assertAlmostEqual(_function.mtbf_mission, 65789473.6842105)

    @attr(all=True, unit=True)
    def test07b_request_calculate_availability(self):
        """(TestFunctionController) request_calculate_availability() should return False on success."""
        self.DUT.request_select_all(1)

        _function = self.DUT.request_select(1)
        _function.mpmt = 0.5
        _function.mcmt = 1.2
        _function.mttr = 5.8
        _function.mmt = 0.85
        _function.mtbf_logistics = 547885.1632698
        _function.mtbf_mission = 500000.0

        self.assertFalse(self.DUT.request_calculate_availability(1))

        self.assertAlmostEqual(_function.availability_logistics, 0.9999894)
        self.assertAlmostEqual(_function.availability_mission, 0.9999884)

    @attr(all=True, unit=True)
    def test08a_request_get_attributes(self):
        """(TestFunctionController) request_get_attributes() should return a dict of {attribute name:attribute value} pairs."""
        self.DUT.request_select_all(1)

        _attributes = self.DUT.request_get_attributes(1)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_attributes['name'], 'Function Name')

    @attr(all=True, unit=True)
    def test08b_request_set_attributes(self):
        """(TestFunctionController) request_set_attributes() should return a dict of {attribute name:attribute value} pairs."""
        _attributes = {
            'type_id': 0,
            'total_part_count': 0,
            'availability_mission': 1.0,
            'cost': 0.0,
            'hazard_rate_mission': 0.0,
            'mpmt': 0.0,
            'parent_id': 0,
            'mtbf_logistics': 0.0,
            'safety_critical': 0,
            'mmt': 0.0,
            'hazard_rate_logistics': 0.0,
            'remarks': '',
            'function_id': 1,
            'mtbf_mission': 0.0,
            'function_code': 'PRESS-001',
            'name': u'Function Name',
            'level': 0,
            'mttr': 0.0,
            'mcmt': 0.0,
            'function_id': 1,
            'availability_logistics': 1.0,
            'total_mode_count': 0
        }

        self.DUT.request_select_all(1)

        _error_code, _msg = self.DUT.request_set_attributes(1, _attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating RTKFunction 1 attributes.')

    @attr(all=True, unit=True)
    def test08c_request_last_id(self):
        """(TestFunctionController) request_last_id() should return the last Function ID used in the RTK Program database."""
        self.DUT.request_select_all(1)

        _last_id = self.DUT.request_last_id()

        self.assertEqual(_last_id, 3)
