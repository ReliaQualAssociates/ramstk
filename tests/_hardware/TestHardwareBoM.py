#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._hardware.TestHardwareBoM.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hardware BoM module algorithms and models."""

import sys
from os.path import dirname

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk", )

import Utilities as Utilities  # pylint: disable=E0401, wrong-import-position
# pylint: disable=E0401, wrong-import-position
from Configuration import Configuration
# pylint: disable=E0401, wrong-import-position
from hardware import dtmHardware, dtmDesignElectric, dtmDesignMechanic, \
    dtmMilHdbkF, dtmNSWC, dtmReliability, \
    dtmHardwareBoM
from dao import DAO  # pylint: disable=E0401, wrong-import-position
# pylint: disable=E0401, wrong-import-position
from dao import RTKHardware, RTKDesignElectric, RTKDesignMechanic, \
    RTKMilHdbkF, RTKNSWC, RTKReliability

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestHardwareBoMDataModel(unittest.TestCase):
    """Class for testing the Hardware BoM data model class."""

    def setUp(self):
        """(TestHardwareBoMDataModel) Set up the test fixture for the Hardware BoM class."""
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

        self.DUT = dtmHardwareBoM(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """(TestHardwareBoMDataModel) __init__ should return a Hardware BoM model."""
        self.assertTrue(isinstance(self.DUT, dtmHardwareBoM))
        self.assertTrue(isinstance(self.DUT.dtm_hardware, dtmHardware))
        self.assertTrue(
            isinstance(self.DUT.dtm_design_electric, dtmDesignElectric))
        self.assertTrue(
            isinstance(self.DUT.dtm_design_mechanic, dtmDesignMechanic))
        self.assertTrue(isinstance(self.DUT.dtm_mil_hdbk_f, dtmMilHdbkF))
        self.assertTrue(isinstance(self.DUT.dtm_nswc, dtmNSWC))
        self.assertTrue(isinstance(self.DUT.dtm_reliability, dtmReliability))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))
        # pylint: disable=protected-access
        self.assertEqual(self.DUT._tag, 'HardwareBoM')

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """(TestHardwareBoMDataModel) select_all() should return a Tree() object populated with RTKHardware instances on success."""
        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, dict))
        self.assertTrue(
            isinstance(_tree.get_node(1).data['general'], RTKHardware))
        self.assertTrue(
            isinstance(
                _tree.get_node(1).data['electrical_design'],
                RTKDesignElectric))
        self.assertTrue(
            isinstance(
                _tree.get_node(1).data['mechanical_design'],
                RTKDesignMechanic))
        self.assertTrue(
            isinstance(_tree.get_node(1).data['mil_hdbk_f'], RTKMilHdbkF))
        self.assertTrue(isinstance(_tree.get_node(3).data['nswc'], RTKNSWC))
        self.assertTrue(
            isinstance(_tree.get_node(1).data['reliability'], RTKReliability))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestHardwareBoMDataModel) select() should return an instance of the RTKHardware data model on success."""
        self.DUT.select_all(1)
        _hardware = self.DUT.select(1)

        self.assertTrue(isinstance(_hardware, dict))
        self.assertTrue(isinstance(_hardware['general'], RTKHardware))
        self.assertTrue(
            isinstance(_hardware['electrical_design'], RTKDesignElectric))
        self.assertTrue(
            isinstance(_hardware['mechanical_design'], RTKDesignMechanic))
        self.assertTrue(isinstance(_hardware['mil_hdbk_f'], RTKMilHdbkF))
        self.assertTrue(isinstance(_hardware['nswc'], RTKNSWC))
        self.assertTrue(isinstance(_hardware['reliability'], RTKReliability))
        self.assertEqual(_hardware['general'].comp_ref_des, 'S1')
        self.assertEqual(_hardware['general'].cage_code, '')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestHardwareBoMDataModel) select() should return None when a non-existent Hardware ID is requested."""
        _hardware = self.DUT.select(100)

        self.assertEqual(_hardware, None)

    @attr(all=True, unit=True)
    def test03a_insert_sibling(self):
        """(TestHardwareBoMDataModel) insert() should return a zero error code on success when inserting a sibling Hardware."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1, parent_id=0)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.dtm_hardware.last_id, 4)

    @attr(all=True, unit=True)
    def test03b_insert_child(self):
        """(TestHardwareBoMDataModel) insert() should return a zero error code on success when inserting a child Hardware."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1, parent_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.dtm_hardware.last_id, 5)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestHardwareBoMDataModel) delete() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(self.DUT.dtm_hardware.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestHardwareBoMDataModel) delete() should return a non-zero error code when passed a Hardware ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to delete non-existent '
                         'Hardware BoM record ID 300.')

    @attr(all=True, unit=True)
    def test05a_update(self):
        """(TestHardwareBoMDataModel) update() should return a zero error code on success."""
        self.DUT.select_all(1)

        _hardware = self.DUT.tree.get_node(1).data
        _hardware['general'].cost = 0.9832

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test05b_update_non_existent_id(self):
        """(TestHardwareBoMDataModel) update() should return a non-zero error code when passed a Hardware ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Hardware BoM ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """(TestHardwareBoMDataModel) update_all() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
