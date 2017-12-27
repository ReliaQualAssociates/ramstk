#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKHardware.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKHardware module algorithms and models."""

import sys
from os.path import dirname

from datetime import date

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from nose.plugins.attrib import attr

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from dao.RTKHardware import RTKHardware

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKHardware(unittest.TestCase):
    """Class for testing the RTKHardware class."""

    _attributes = {
        'revision_id': 1,
        'hardware_id': 1,
        'alt_part_num': '',
        'attachments': '',
        'cage_code': '',
        'category_id': 0,
        'comp_ref_des': '',
        'cost': 0.0,
        'cost_failure': 0.0,
        'cost_hour': 0.0,
        'cost_type_id': 0,
        'description': 'Description',
        'duty_cycle': 100.0,
        'figure_number': '',
        'lcn': '',
        'level': 0,
        'manufacturer_id': 0,
        'mission_time': 100.0,
        'name': '',
        'nsn': '',
        'page_number': '',
        'parent_id': 0,
        'part': 0,
        'part_number': '',
        'quantity': 1,
        'ref_des': 'S1',
        'remarks': '',
        'repairable': 0,
        'specification_number': '',
        'subcategory_id': 0,
        'tagged_part': 0,
        'total_part_count': 0,
        'total_power_dissipation': 0,
        'year_of_manufacture': date.today().year
    }

    def setUp(self):
        """(TestRTKHardware) Set up the test fixture for the RTKHardware class."""
        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKHardware).first()
        self.DUT.description = self._attributes['description']

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkhardware_create(self):
        """(TestRTKHardware) __init__ should create an RTKHardware model."""
        self.assertTrue(isinstance(self.DUT, RTKHardware))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_hardware')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.hardware_id, 1)
        self.assertEqual(self.DUT.alt_part_number, '')
        self.assertEqual(self.DUT.attachments, '')
        self.assertEqual(self.DUT.cage_code, '')
        self.assertEqual(self.DUT.comp_ref_des, '')
        self.assertEqual(self.DUT.category_id, 0)
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.cost_failure, 0.0)
        self.assertEqual(self.DUT.cost_hour, 0.0)
        self.assertEqual(self.DUT.cost_type_id, 0)
        self.assertEqual(self.DUT.description, 'Description')
        self.assertEqual(self.DUT.duty_cycle, 100.0)
        self.assertEqual(self.DUT.figure_number, '')
        self.assertEqual(self.DUT.lcn, '')
        self.assertEqual(self.DUT.level, 0)
        self.assertEqual(self.DUT.manufacturer_id, 0)
        self.assertEqual(self.DUT.mission_time, 100.0)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.nsn, '')
        self.assertEqual(self.DUT.page_number, '')
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.part, 0)
        self.assertEqual(self.DUT.part_number, '')
        self.assertEqual(self.DUT.quantity, 1)
        self.assertEqual(self.DUT.ref_des, 'S1')
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.repairable, 0)
        self.assertEqual(self.DUT.specification_number, '')
        self.assertEqual(self.DUT.subcategory_id, 0)
        self.assertEqual(self.DUT.tagged_part, 0)
        self.assertEqual(self.DUT.total_part_count, 0)
        self.assertEqual(self.DUT.total_power_dissipation, 0.0)
        self.assertEqual(self.DUT.year_of_manufacture, date.today().year)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """(TestRTKHardware) get_attributes should return a tuple of attribute values."""
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """(TestRTKHardware) set_attributes should return a zero error code on success."""
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKHardware {0:d} "
                         "attributes.".format(self.DUT.hardware_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_key(self):
        """(TestRTKHardware) set_attributes should return a 40 error code when passed a dict with a missing key."""
        self._attributes.pop('name')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute 'name' in "
                         "attribute dictionary passed to "
                         "RTKHardware.set_attributes().")
