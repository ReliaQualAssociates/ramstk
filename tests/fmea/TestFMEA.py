#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.fmea.TestFMEA.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This is the test class for testing the FMEA class.
"""

import unittest
from nose.plugins.attrib import attr

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from dao import DAO
from dao import RTKMode
from dao import RTKMechanism
from dao import RTKCause
from dao import RTKControl
from dao import RTKAction
from analyses.fmea.FMEA import Model, FMEA
from analyses.fmea.Mode import Model as Mode
from analyses.fmea.Mechanism import Model as Mechanism
from analyses.fmea.Cause import Model as Cause
from analyses.fmea.Control import Model as Control
from analyses.fmea.Action import Model as Action

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class Test00FMEAModel(unittest.TestCase):
    """
    Class for testing the FMEA model class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the FMEA model class.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {'host'    : 'localhost',
                                            'socket'  : 3306,
                                            'database': '/tmp/TestDB.rtk',
                                            'user'    : '',
                                            'password': ''}

        self.Configuration.DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
        self.Configuration.USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(bind=self.dao.engine, autoflush=False,
                                       expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)
        _mode = RTKMode()
        self.dao.db_add([_mode, ], self.session)
        _mechanism = RTKMechanism()
        _mechanism.mode_id = _mode.mode_id
        self.dao.db_add([_mechanism, ], self.session)
        _cause = RTKCause()
        _cause.mechanism_id = _mechanism.mechanism_id
        self.dao.db_add([_cause, ], self.session)
        _control = RTKControl()
        _control.mode_id = _mode.mode_id
        _control.cause_id = _cause.cause_id
        _action = RTKAction()
        _action.mode_id = _mode.mode_id
        _action.cause_id = _cause.cause_id
        self.dao.db_add([_control, ], self.session)
        self.dao.db_add([_action, ], self.session)

        self.DUT = Model(self.dao)

    @attr(all=True, unit=True)
    def test00_FMEA_create(self):
        """
        (TestFMEAModel) __init__ should return instance of FMEA data model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertTrue(isinstance(self.DUT._dtm_mode, Mode))
        self.assertTrue(isinstance(self.DUT._dtm_mechanism, Mechanism))
        self.assertTrue(isinstance(self.DUT._dtm_cause, Cause))
        self.assertTrue(isinstance(self.DUT._dtm_control, Control))
        self.assertTrue(isinstance(self.DUT._dtm_action, Action))

    @attr(all=True, unit=True)
    def test01a_select_all_functional(self):
        """
        (TestFMEAModel) select_all() should return a treelib Tree() on success when
        selecting a Functional FMEA
        """

        _tree = self.DUT.select_all(1, True)

        self.assertTrue(isinstance(_tree, Tree))

    @attr(all=True, unit=True)
    def test01b_select_all_hardware(self):
        """
        (TestFMEAModel) select_all() should return a treelib Tree() on success when
        selecting a Hardware FMEA
        """

        _tree = self.DUT.select_all(1)
        _tree.show()

        self.assertTrue(isinstance(_tree, Tree))

    @attr(all=True, unit=True)
    def test01c_select_all_non_existent_hardware_id(self):
        """
        (TestFMEAModel): select_all() should return an empty Tree() when passed
        a Hardware ID that doesn't exist.
        """

        _tree = self.DUT.select_all(100)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertEqual(_tree.get_node(0).tag, 'FMEA')
        self.assertEqual(_tree.get_node(1), None)

    @attr(all=True, unit=True)
    def test01d_select_all_non_existent_function_id(self):
        """
        (TestFMEAModel): select_all() should return an empty Tree() when passed
        a Function ID that doesn't exist.
        """

        _tree = self.DUT.select_all(100, True)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertEqual(_tree.get_node(0).tag, 'FMEA')
        self.assertEqual(_tree.get_node(1), None)

    @attr(all=True, unit=True)
    def test02a_select_mode(self):
        """
        (TestFMEAModel): select() should return an instance of RTKMode on success.
        """

        self.DUT.select_all(1)

        _entity = self.DUT.select('0.1')

        self.assertTrue(isinstance(_entity, RTKMode))
        self.assertEqual(_entity.description, 'Test Failure Mode #1')

    @attr(all=True, unit=True)
    def test02b_select_mechanism(self):
        """
        (TestFMEAModel): select() should return an instance of RTKMechanism on success.
        """

        self.DUT.select_all(1)

        _entity = self.DUT.select('0.1.1')

        self.assertTrue(isinstance(_entity, RTKMechanism))
        self.assertEqual(_entity.description, 'Test Failure Mechanism #1')

    @attr(all=True, unit=True)
    def test02c_select_cause(self):
        """
        (TestFMEAModel): select() should return an instance of RTKCause on success.
        """

        self.DUT.select_all(1)

        _entity = self.DUT.select('0.1.1.1')

        self.assertTrue(isinstance(_entity, RTKCause))
        self.assertEqual(_entity.description, 'Test Failure Cause #1')

    @attr(all=True, unit=True)
    def test02d_select_control(self):
        """
        (TestFMEAModel): select() should return an instance of RTKControl on success.
        """

        self.DUT.select_all(1)

        _entity = self.DUT.select('0.1.1.1.01')

        self.assertTrue(isinstance(_entity, RTKControl))
        self.assertEqual(_entity.description,
                         'Test Control for Failure Cause #1')

    @attr(all=True, unit=True)
    def test02e_select_action(self):
        """
        (TestFMEAModel): select() should return an instance of RTKAction on success.
        """

        self.DUT.select_all(1)

        _entity = self.DUT.select('0.1.1.1.1')

        self.assertTrue(isinstance(_entity, RTKAction))
        self.assertEqual(_entity.action_recommended,
                         'Recommended action for Failure Cause #1')

    @attr(all=True, unit=True)
    def test03a_insert_mode_functional(self):
        """
        (TestFMEAModel): insert() should return a zero error code on success when adding a new Mode to a Functional FMEA.
        """

        self.DUT.select_all(1, True)

        _error_code, _msg = self.DUT.insert(1, 0, 'mode')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK "
                         "Program database.")
        _node_id = '0.' + str(self.DUT._dtm_mode.last_id)

        _mode = self.DUT.select(_node_id)

        self.assertTrue(isinstance(_mode, RTKMode))
        self.assertEqual(_mode.function_id, 1)
        self.assertEqual(_mode.hardware_id, -1)

        _tree_mode = self.DUT.tree.get_node(_node_id)
        self.assertTrue(isinstance(_tree_mode.data, RTKMode))
        self.assertEqual(_mode, _tree_mode.data)

    @attr(all=True, unit=True)
    def test03b_insert_mode_hardware(self):
        """
        (TestFMEAModel): insert() should return a zero error code on success
        when adding a new Mode to a Hardware FMEA.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(1, 0, 'mode')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK "
                         "Program database.")
        _node_id = '0.' + str(self.DUT._dtm_mode.last_id)

        _mode = self.DUT.select(_node_id)

        self.assertTrue(isinstance(_mode, RTKMode))
        self.assertEqual(_mode.function_id, -1)
        self.assertEqual(_mode.hardware_id, 1)

        _tree_mode = self.DUT.tree.get_node(_node_id)
        self.assertTrue(isinstance(_tree_mode.data, RTKMode))
        self.assertEqual(_mode, _tree_mode.data)

    @attr(all=True, unit=True)
    def test03c_insert_mode_hardware_non_existant_level(self):
        """
        (TestFMEAModel): insert() should return a non-zero error code when
        trying to add a non-existant level.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(1, 0, 'juice')

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg,
                         'RTK ERROR: Attempted to add an item to the FMEA '
                         'with an undefined indenture level.  Level juice was '
                         'requested.  Must be one of mode, mechanism, cause, '
                         'control, or action.')

    @attr(all=True, unit=True)
    def test03d_insert_mechanism(self):
        """
        (TestFMEAModel): insert() should return a zero error code on success when adding a new Mechanism to a Hardware FMEA.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(1, '0.1', 'mechanism')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK "
                         "Program database.")
        _node_id = '0.1.' + str(self.DUT._dtm_mechanism.last_id)

        _mechanism = self.DUT.select(_node_id)

        self.assertTrue(isinstance(_mechanism, RTKMechanism))
        self.assertEqual(_mechanism.mode_id, 1)
        self.assertEqual(_mechanism.mechanism_id,
                         self.DUT._dtm_mechanism.last_id)

        _tree_mechanism = self.DUT.tree.get_node(_node_id)
        self.assertTrue(isinstance(_tree_mechanism.data, RTKMechanism))
        self.assertEqual(_mechanism, _tree_mechanism.data)

    @attr(all=True, unit=True)
    def test03e_insert_cause(self):
        """
        (TestFMEAModel): insert() should return a zero error code on success
        when adding a new Cause to a Hardware FMEA.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(1, '0.1.1', 'cause')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK "
                         "Program database.")
        _node_id = '0.1.1.' + str(self.DUT._dtm_cause.last_id)

        _cause = self.DUT.select(_node_id)

        self.assertTrue(isinstance(_cause, RTKCause))
        self.assertEqual(_cause.mechanism_id, 1)
        self.assertEqual(_cause.cause_id, self.DUT._dtm_cause.last_id)

        _tree_cause = self.DUT.tree.get_node(_node_id)
        self.assertTrue(isinstance(_tree_cause.data, RTKCause))
        self.assertEqual(_tree_cause.data, _cause)

    @attr(all=True, unit=True)
    def test03f_insert_control_functional(self):
        """
        (TestFMEAModel): insert() should return a zero error code on success when adding a new Control to a Functional FMEA.
        """

        self.DUT.select_all(1, True)

        _error_code, _msg = self.DUT.insert(1, '0.1', 'control')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK "
                         "Program database.")
        _node_id = '0.1.0' + str(self.DUT._dtm_control.last_id)

        _control = self.DUT.select(_node_id)

        self.assertTrue(isinstance(_control, RTKControl))
        self.assertEqual(_control.mode_id, 1)
        self.assertEqual(_control.cause_id, -1)

        _tree_control = self.DUT.tree.get_node(_node_id)
        self.assertTrue(isinstance(_tree_control.data, RTKControl))
        self.assertEqual(_control, _tree_control.data)

    @attr(all=True, unit=True)
    def test03g_insert_control_hardware(self):
        """
        (TestFMEAModel): insert() should return a zero error code on success when adding a new Control to a Hardware FMEA.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(2, '0.1.1.1', 'control')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK "
                         "Program database.")
        _node_id = '0.1.1.1.0' + str(self.DUT._dtm_control.last_id)

        _control = self.DUT.select(_node_id)

        self.assertTrue(isinstance(_control, RTKControl))
        self.assertEqual(_control.mode_id, -1)
        self.assertEqual(_control.cause_id, 2)

        _tree_control = self.DUT.tree.get_node(_node_id)
        self.assertTrue(isinstance(_tree_control.data, RTKControl))
        self.assertEqual(_control, _tree_control.data)

    @attr(all=True, unit=True)
    def test03h_insert_action_functional(self):
        """
        (TestFMEAModel): insert() should return a zero error code on success when adding a new Action to a Functional FMEA.
        """

        self.DUT.select_all(1, True)

        _error_code, _msg = self.DUT.insert(1, '0.1', 'action')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK "
                         "Program database.")
        _node_id = '0.1.' + str(self.DUT._dtm_action.last_id)

        _action = self.DUT.select(_node_id)

        self.assertTrue(isinstance(_action, RTKAction))
        self.assertEqual(_action.mode_id, 1)
        self.assertEqual(_action.cause_id, -1)

        _tree_action = self.DUT.tree.get_node(_node_id)
        self.assertTrue(isinstance(_tree_action.data, RTKAction))
        self.assertEqual(_action, _tree_action.data)

    @attr(all=True, unit=True)
    def test03i_insert_action_hardware(self):
        """
        (TestFMEAModel): insert() should return a zero error code on success when adding a new Action to a Hardware FMEA.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(1, '0.1.1.1', 'action')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK "
                         "Program database.")
        _node_id = '0.1.1.1.' + str(self.DUT._dtm_action.last_id)

        _action = self.DUT.select(_node_id)

        self.assertTrue(isinstance(_action, RTKAction))
        self.assertEqual(_action.mode_id, -1)
        self.assertEqual(_action.cause_id, 1)

        _tree_action = self.DUT.tree.get_node(_node_id)
        self.assertTrue(isinstance(_tree_action.data, RTKAction))
        self.assertEqual(_action, _tree_action.data)

    @attr(all=True, unit=True)
    def test03j_insert_non_existent_type(self):
        """
        (TestFMEAModel): insert() should return a 2005 error code when attempting to add something other than a Mode, Mechanism, Cause, Control, or Action.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(100, 0, 'scadamoosh')

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg,
                         "RTK ERROR: Attempted to add an item to the FMEA " \
                         "with an undefined indenture level.  Level " \
                         "scadamoosh was requested.  Must be one of "
                         "mode, mechanism, cause, control, or action.")

    @attr(all=True, unit=False)
    def test03k_insert_no_parent_in_tree(self):
        """
        (TestFMEAModel): insert() should return a 3002 error code when attempting to add something to a non-existant parent Node.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(100, 'mode_1', 'action')

        self.assertEqual(_error_code, 3002)
        self.assertEqual(_msg,
                         "RTK ERROR: Creating a new node in the Usage " \
                         "Profile Tree.")

    @attr(all=True, unit=True)
    def test04a_delete_control(self):
        """
        (TestFMEAModel): delete() should return a zero error code on success when removing a Control.
        """

        self.DUT.select_all(1)
        _node_id = '0.1.1.2.0' + str(self.DUT._dtm_control.last_id)

        _error_code, _msg = self.DUT.delete(_node_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Deleting an item from the RTK Program "
                         "database.")

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_node_id(self):
        """
        (TestFMEAModel): delete() should return a 2105 error code when attempting to remove a non-existant item from the FMEA.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete('scadamoosh_1')

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg,
                         "RTK ERROR: Attempted to delete a non-existent "
                         "entity with Node ID scadamoosh_1 from the FMEA.")

    @attr(all=True, unit=True)
    def test05a_update(self):
        """
        (TestFMEAModel): update() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update('0.1')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Updating the RTK Program database.")

    @attr(all=True, unit=True)
    def test05b_update_non_existent_node_id(self):
        """
        (TestFMEAModel): update() should return a 2106 error code when attempting to update a non-existent Node ID.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update('mode_1000')

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg,
                         "RTK ERROR: Attempted to save non-existent FMEA "
                         "entity with Node ID mode_1000.")

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """
        (TestFMEAModel): update_all() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test07a_calculate_criticality(self):
        """
        (TestFMEAModel) _calculate_criticality returns a zero error code on success
        """

        self.DUT.select_all(1)
        _mode = self.DUT.select('0.1')
        _mode.mode_ratio = 0.4
        _mode.mode_op_time = 100.0
        _mode.effect_probability = 1.0
        _mode = self.DUT.select('0.3')
        _mode.mode_ratio = 0.5
        _mode.mode_op_time = 100.0
        _mode.effect_probability = 1.0
        _error_code, _msg = self.DUT.calculate_criticality(0.00001)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating failure mode 3 '
                               'criticality.')
        self.assertEqual(_mode.mode_criticality, 0.0005)

        self.DUT.update('0.1')
        self.DUT.update('0.3')

    @attr(all=True, unit=True)
    def test08a_calculate_mechanism_rpn(self):
        """
        (TestFMEAModel) calculate_mechanism_rpn returns a zero error code on success
        """

        self.DUT.select_all(1)

        for _node in self.DUT.tree.children('0.1'):
            _mechanism = _node.data
            _attributes = list(_mechanism.get_attributes()[2:])
            _attributes[3] = 4
            _attributes[4] = 3
            _attributes[6] = 7
            _attributes[7] = 5
            _mechanism.set_attributes(_attributes)

        _error_code, _msg = \
        self.DUT.calculate_mechanism_rpn('0.1', 7, 4)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating failure mechanism '
                               '{0:d} RPN.'.\
                         format(self.DUT._dtm_mechanism.last_id))
        self.assertEqual(_mechanism.rpn, 196)
        self.assertEqual(_mechanism.rpn_new, 60)

    @attr(all=True, unit=True)
    def test09a_calculate_cause_rpn(self):
        """
        (TestFMEAModel) calculate_cause_rpn returns a zero error code on success
        """

        self.DUT.select_all(1)

        for _node in self.DUT.tree.children('0.1.1'):
            _cause = _node.data
            _attributes = list(_cause.get_attributes()[2:])
            _attributes[2] = 4
            _attributes[3] = 3
            _attributes[5] = 7
            _attributes[6] = 5
            _cause.set_attributes(_attributes)

        _error_code, _msg = \
        self.DUT.calculate_cause_rpn('0.1.1', 7, 4)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating failure cause '
                               '{0:d} RPN.'.\
                         format(self.DUT._dtm_cause.last_id))
        self.assertEqual(_cause.rpn, 196)
        self.assertEqual(_cause.rpn_new, 60)


class Test01FMEAController(unittest.TestCase):
    """
    Class for testing the FMEA data controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the FMEA Data Controller.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {'host'    : 'localhost',
                                            'socket'  : 3306,
                                            'database': '/tmp/TestDB.rtk',
                                            'user'    : '',
                                            'password': ''}

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

        self.dao.RTK_SESSION.configure(bind=self.dao.engine, autoflush=False,
                                       expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)
        self.dao.db_add([RTKMode(), ], self.session)
        self.dao.db_add([RTKMechanism(), ], self.session)
        self.dao.db_add([RTKCause(), ], self.session)
        self.dao.db_add([RTKControl(), ], self.session)
        self.dao.db_add([RTKAction(), ], self.session)

        self.DUT = FMEA(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_create_controller(self):
        """
        (TestFMEAController) __init__ should return instance of FMEA data controller
        """

        self.assertTrue(isinstance(self.DUT, FMEA))
        self.assertTrue(isinstance(self.DUT._dtm_fmea, Model))

    @attr(all=True, unit=True)
    def test01a_request_select_all_hardware(self):
        """
        (TestFMEAController) request_select_all() should return a treelib
        Tree() with the hardware FMEA.
        """

        self.assertTrue(isinstance(self.DUT.request_select_all(1), Tree))

    @attr(all=True, unit=True)
    def test01b_request_select_all_function(self):
        """
        (TestFMEAController) request_select_all() should return a treelib
        Tree() with the functional FMEA.
        """

        self.assertTrue(isinstance(self.DUT.request_select_all(1, True), Tree))

    @attr(all=True, unit=True)
    def test03a_request_insert_mode_functional(self):
        """
        (TestFMEAController) request_insert() should return False on success
        when adding a mode to a functional FMEA.
        """

        self.DUT.request_select_all(1, True)
        self.assertFalse(self.DUT.request_insert(1, 0, 'mode'))

    @attr(all=True, unit=True)
    def test_03b_request_insert_mode_hardware(self):
        """
        (TestFMEAController) request_insert() should return False on success
        when addin a mode to a hardware FMEA.
        """

        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_insert(1, 0, 'mode'))

    @attr(all=True, unit=True)
    def test03c_insert_mechanism(self):
        """
        (TestFMEAController): request_insert() should return a False on success
        when adding a new Mechanism to a Hardware FMEA.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_insert(1, '0.1', 'mechanism'))

    @attr(all=True, unit=True)
    def test04a_request_delete_control(self):
        """
        (TestFMEAController): request_delete() should return False on success
        when removing a Control.
        """

        self.DUT.request_select_all(1)
        _node_id = '0.1.1.1.0' + str(self.DUT._dtm_fmea._dtm_control.last_id)

        self.assertFalse(self.DUT.request_delete(_node_id))

    @attr(all=True, unit=True)
    def test05a_update_all(self):
        """
        (TestFMEAController): request_update_all() should return a zero error code on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update_all())

