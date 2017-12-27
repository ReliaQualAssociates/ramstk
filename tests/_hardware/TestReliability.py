#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._hardware.TestReliability.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Reliability module algorithms and models."""

import sys
from os.path import dirname

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import Utilities as Utilities  # pylint: disable=import-error
from Configuration import Configuration  # pylint: disable=import-error
from hardware import dtmReliability  # pylint: disable=import-error
from dao import DAO  # pylint: disable=import-error
from dao import RTKReliability  # pylint: disable=import-error

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestReliabilityDataModel(unittest.TestCase):
    """Class for testing the Reliability data model class."""

    def setUp(self):
        """(TestReliability) Set up the test fixture for the Reliability class."""
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

        self.DUT = dtmReliability(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """(TestReliabilityDataModel) __init__ should return a Reliability model."""
        self.assertTrue(isinstance(self.DUT, dtmReliability))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))
        self.assertEqual(self.DUT._tag, 'Reliability')

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """(TestReliabilityDataModel) select_all() should return a Tree() object populated with RTKReliability instances on success."""
        _tree = self.DUT.select_all(2)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(2).data, RTKReliability))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestReliabilityDataModel) select() should return an instance of the RTKReliability data model on success."""
        self.DUT.select_all(2)
        _reliability = self.DUT.select(2)

        self.assertTrue(isinstance(_reliability, RTKReliability))
        self.assertEqual(_reliability.hardware_id, 2)
        self.assertEqual(_reliability.hazard_rate_percent, 0.0)

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestReliabilityDataModel) select() should return None when a non-existent Reliability ID is requested."""
        _design_electric = self.DUT.select(100)

        self.assertEqual(_design_electric, None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """(TestReliabilityDataModel) insert() should return False on success when inserting a Reliability record."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.insert(hardware_id=4)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestReliabilityDataModel) delete() should return a zero error code on success."""
        self.DUT.select_all(4)

        _error_code, _msg = self.DUT.delete(4)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestReliabilityDataModel) delete() should return a non-zero error code when passed a Reliability ID that doesn't exist."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'Reliability record ID 300.')

    @attr(all=True, unit=True)
    def test05a_update(self):
        """(TestReliabilityDataModel) update() should return a zero error code on success."""
        self.DUT.select_all(3)

        _design_electric = self.DUT.select(3)
        _design_electric.resistance = 0.9832

        _error_code, _msg = self.DUT.update(3)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test05b_update_non_existent_id(self):
        """(TestReliabilityDataModel) update() should return a non-zero error code when passed a Reliability ID that doesn't exist."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Reliability record ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """(TestReliabilityDataModel) update_all() should return a zero error code on success."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
