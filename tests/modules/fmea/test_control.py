# -*- coding: utf-8 -*-
#
#       rtk.tests.fmea.TestControl.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Control class."""

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import rtk.Utilities as Utilities
from rtk.Configuration import Configuration
from rtk.analyses.fmea import dtmControl
from rtk.dao import DAO
from rtk.dao import RTKControl

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "weibullguy" Rowland'


class TestControlDataModel(unittest.TestCase):
    """
    Class for testing the Control model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Control model class.
        """
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

        self.DUT = dtmControl(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestControlModel) __init__ should return instance of Control data model
        """
        self.assertTrue(isinstance(self.DUT, dtmControl))
        self.assertEqual(self.DUT.last_id, None)

    @attr(all=True, unit=True)
    def test01a_select_all_functional(self):
        """
        (TestControlModel): select_all() should return a Tree() object populated with RTKControl instances on success.
        """
        _tree = self.DUT.select_all(1, functional=True)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKControl))

    @attr(all=True, unit=True)
    def test01b_select_all_hardware(self):
        """
        (TestControlModel): select_all() should return a Tree() object populated with RTKControl instances on success.
        """
        _tree = self.DUT.select_all(1, functional=False)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKControl))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestControlModel): select() should return an instance of the RTKControl data model on success.
        """
        self.DUT.select_all(1, functional=False)
        _control = self.DUT.select(1)

        self.assertTrue(isinstance(_control, RTKControl))
        self.assertEqual(_control.control_id, 1)

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """
        (TestControlModel): select() should return None when a non-existent Control ID is requested.
        """
        self.DUT.select_all(1, functional=False)
        _control = self.DUT.select(100)

        self.assertEqual(_control, None)

    @attr(all=True, unit=True)
    def test03a_insert_functional_control(self):
        """
        (TestControlModel): insert() should return False on success when inserting a Control into a functional FMEA.
        """
        self.DUT.select_all(1, functional=True)

        _error_code, _msg = self.DUT.insert(mode_id=1, cause_id=-1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')

    @attr(all=True, unit=True)
    def test03b_insert_hardware_control(self):
        """
        (TestControlModel): insert() should return False on success when inserting a Control into a hardware FMEA.
        """
        self.DUT.select_all(1, functional=False)

        _error_code, _msg = self.DUT.insert(mode_id=-1, cause_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """
        (TestControlModel): delete() should return a zero error code on success.
        """
        self.DUT.select_all(1, functional=False)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """
        (TestControlModel): delete() should return a non-zero error code when passed a Control ID that doesn't exist.
        """
        self.DUT.select_all(1, functional=False)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'Control ID 300.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """
        (TestControlModel): update() should return a zero error code on success.
        """
        self.DUT.select_all(1, functional=False)

        _control = self.DUT.select(1)
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
        self.DUT.select_all(1, functional=False)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Control ID 100.')

    @attr(all=True, unit=True)
    def test_06a_update_all(self):
        """
        (TestControlModel): update_all() should return a zero error code on success.
        """
        self.DUT.select_all(1, functional=False)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
