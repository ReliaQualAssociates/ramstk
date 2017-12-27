# -*- coding: utf-8 -*-
#
#       tests.unit.TestFMEAMechanism.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This is the test class for testing the FMEA failure Mechanism class.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from analyses.fmea import dtmMechanism
from dao import DAO
from dao import RTKMechanism

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "Weibullguy" Rowland'


class TestMechanismDataModel(unittest.TestCase):
    """
    Class for testing the Mechanism model class.
    """

    def setUp(self):
        """
        Setups the test fixture for the Mechanism model class.
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

        self.DUT = dtmMechanism(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestMechanismModel) __init__ should return instance of Mechanism data model
        """

        self.assertTrue(isinstance(self.DUT, dtmMechanism))
        self.assertEqual(self.DUT.last_id, None)

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """
        (TestMechanismModel) select_all() should return a Tree() object populated
        with RTKMechanism instances on success
        """

        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKMechanism))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestMechanismModel) select() should return an instance of the RTKMechanism
        data model on success
        """

        self.DUT.select_all(1)
        _mechanism = self.DUT.select(1)

        self.assertTrue(isinstance(_mechanism, RTKMechanism))
        self.assertEqual(_mechanism.mechanism_id, 1)
        self.assertEqual(_mechanism.description, 'Test Failure Mechanism #1')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """
        (TestMechanismModel) select() should return None when a non-existent
        Mechanism ID is requested
        """

        _mechanism = self.DUT.select(300)

        self.assertEqual(_mechanism, None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """
        (TestMechanismModel) insert() should return a zero error code on success
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(mode_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """
        (TestMechanismModel) delete() should return a zero error code on success
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """
        (TestMechanismModel) delete() should return a non-zero error code when
        passed a Mechanism ID that doesn't exist
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'Mechanism ID 300.')

    @attr(all=True, unit=True)
    def test05a_update(self):
        """
        (TestMechanismModel) update() should return a zero error code on success
        """

        self.DUT.select_all(1)

        _mechanism = self.DUT.tree.get_node(1).data
        _mechanism.pof_include = 1

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Updating the RTK Program '
                         'database.')

    @attr(all=True, unit=True)
    def test05b_update_non_existent_id(self):
        """
        (TestMechanismModel) update() should return a non-zero error code when
        passed a Mechanism ID that doesn't exist
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Mechanism ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """
        (TestMechanismModel) update_all() should return a zero error code on
        success
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Updating the RTK Program '
                         'database.')
