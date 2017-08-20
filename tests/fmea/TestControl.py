#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.fmea.TestControl.py is part of The RTK Project
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
"""
This is the test class for testing the Control class.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from analyses.fmea.Control import Model, Control
from dao import DAO
from dao import RTKControl

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2015 Andrew "weibullguy" Rowland'


class Test00ControlModel(unittest.TestCase):
    """
    Class for testing the Control model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Control model class.
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
        self.dao.db_add([RTKControl(), ], self.session)
        self.dao.db_add([RTKControl(), ], self.session)

        self.DUT = Model(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestControlModel) __init__ should return instance of Control data model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT.last_id, None)

    @attr(all=True, unit=True)
    def test01a_select_all_functional(self):
        """
        (TestControlModel): select_all() should return a Tree() object populated with RTKControl instances on success.
        """

        _tree = self.DUT.select_all(1, True)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKControl))

    @attr(all=True, unit=True)
    def test01b_select_all_hardware(self):
        """
        (TestControlModel): select_all() should return a Tree() object populated with RTKControl instances on success.
        """

        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKControl))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestControlModel): select() should return an instance of the RTKControl data model on success.
        """

        self.DUT.select_all(1)
        _control = self.DUT.select(1)

        self.assertTrue(isinstance(_control, RTKControl))
        self.assertEqual(_control.control_id, 1)

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """
        (TestControlModel): select() should return None when a non-existent Control ID is requested.
        """

        self.DUT.select_all(1)
        _control = self.DUT.select(100)

        self.assertEqual(_control, None)

    @attr(all=True, unit=True)
    def test03a_insert_functional_control(self):
        """
        (TestControlModel): insert() should return False on success when inserting a Control into a functional FMEA.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(mode_id=1, cause_id=-1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')

    @attr(all=True, unit=True)
    def test03b_insert_hardware_control(self):
        """
        (TestControlModel): insert() should return False on success when inserting a Control into a hardware FMEA.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(mode_id=-1, cause_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """
        (TestControlModel): delete() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                               'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """
        (TestControlModel): delete() should return a non-zero error code when passed a Control ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to delete non-existent '
                               'Control ID 300.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """
        (TestControlModel): update() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _control = self.DUT.tree.get_node(1).data
        _control.description = 'Functional FMEA control.'

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_update_non_existent_id(self):
        """
        (TestControlModel): update() should return a non-zero error code when passed a Control ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                               'Control ID 100.')

    @attr(all=True, unit=True)
    def test_06a_update_all(self):
        """
        (TestControlModel): update_all() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')


class Test01ControlController(unittest.TestCase):
    """
    Class for testing the Control Data Controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Control Data Controller.
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
        self.dao.db_add([RTKControl(), ], self.session)
        self.dao.db_add([RTKControl(), ], self.session)

        self.DUT = Control(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestControlController) __init__ should return a Control Data Controller
        """

        self.assertTrue(isinstance(self.DUT, Control))
        self.assertTrue(isinstance(self.DUT._dtm_control, Model))

    @attr(all=True, unit=True)
    def test01_request_select_all(self):
        """
        (TestControlController) request_select_all() should return a Tree of RTKControl models.
        """

        _tree = self.DUT.request_select_all(1)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKControl))

    @attr(all=True, unit=True)
    def test02a_request_select(self):
        """
        (TestControlController) request_select() should return an RTKControl model.
        """

        self.DUT.request_select_all(1)

        _control = self.DUT.request_select(1)

        self.assertTrue(isinstance(_control, RTKControl))

    @attr(all=True, unit=True)
    def test02b_request_select_non_existent_id(self):
        """
        (TestControlController) request_select() should return None when requesting a Control that doesn't exist.
        """

        _control = self.DUT.request_select(100)

        self.assertEqual(_control, None)

    @attr(all=True, unit=True)
    def test03a_request_insert_functional(self):
        """
        (TestControlController) request_insert() should return False on success.
        """

        self.DUT.request_select_all(1, True)

        self.assertFalse(self.DUT.request_insert(mode_id=1,
                                                 cause_id=-1))

    @attr(all=True, unit=True)
    def test03a_request_insert_hardware(self):
        """
        (TestControlController) request_insert() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_insert(mode_id=-1,
                                                 cause_id=1))

    @attr(all=True, unit=True)
    def test04a_request_delete(self):
        """
        (TestControlController) request_delete() should return False on success.
        """

        self.DUT.request_select_all(1, True)
        self.DUT.request_insert(mode_id=1, cause_id=-1)

        self.assertFalse(self.DUT.request_delete(
                self.DUT._dtm_control.last_id))

    @attr(all=True, unit=True)
    def test04a_request_delete_non_existent_id(self):
        """
        (TestControlController) request_delete() should return True when attempting to delete a non-existent Control.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=True)
    def test05a_request_update(self):
        """
        (TestControlController) request_update() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update(1))

    @attr(all=True, unit=True)
    def test05b_request_update_non_existent_id(self):
        """
        (TestControlController) request_update() should return True when attempting to save a non-existent Mode.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_update(100))

    @attr(all=True, unit=True)
    def test06a_request_update_all(self):
        """
        (TestControlController) request_update_all() should return False on success.
        """

        self.DUT.request_select_all(1)

        _error_code, _msg = self.DUT.request_update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
