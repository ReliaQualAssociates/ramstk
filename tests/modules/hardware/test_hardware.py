# -*- coding: utf-8 -*-
#
#       tests.modules.hardware.test_hardware.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hardware module algorithms and models. """

from treelib import Tree

import pytest

from rtk.modules.hardware import dtmHardware
from rtk.dao import DAO
from rtk.dao import RTKHardware

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'


@pytest.mark.integration
def test_data_model_create(test_dao):
    """ __init__() should return a Hardware model. """
    DUT = dtmHardware(test_dao)

    assert isinstance(DUT, dtmHardware)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)
    assert DUT._tag == 'Hardware'


@pytest.mark.integration
def test_select_all(test_dao):
    """ select_all() should return a Tree() object populated with RTKHardware instances on success. """
    DUT = dtmHardware(test_dao)

    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKHardware)


@pytest.mark.integration
def test_select(test_dao):
    """ select() should return an instance of the RTKHardware data model on success. """
    DUT = dtmHardware(test_dao)
    DUT.select_all(1)

    _hardware = DUT.select(1)

    assert isinstance(_hardware, RTKHardware)
    assert _hardware.hardware_id == 1
    assert _hardware.cage_code == ''


@pytest.mark.integration
def test_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent Hardware ID is requested. """
    DUT = dtmHardware(test_dao)

    _hardware = DUT.select(100)

    assert _hardware is None


@pytest.mark.integration
def test_insert_sibling_assembly(test_dao):
    """ insert() should return False on success when inserting a sibling Hardware assembly. """
    DUT = dtmHardware(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(revision_id=1, parent_id=0, part=0)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Adding one or more items to the RTK Program '
                    'database.')


@pytest.mark.integration
def test_insert_child_assembly(test_dao):
    """ insert() should return False on success when inserting a child Hardware assembly. """
    DUT = dtmHardware(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(revision_id=1, parent_id=1, part=0)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Adding one or more items to the RTK Program '
                    'database.')


@pytest.mark.integration
def test_delete_assembly(test_dao):
    """ delete() should return a zero error code on success when deleting a Hardware assembly. """
    DUT = dtmHardware(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Deleting an item from the RTK Program '
                    'database.')


@pytest.mark.integration
def test_delete_assembly_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a Hardware assembly with an ID that doesn't exist. """
    DUT = dtmHardware(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ('  RTK ERROR: Attempted to delete non-existent Hardware '
                    'ID 300.')


@pytest.mark.integration
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmHardware(test_dao)
    DUT.select_all(1)

    _hardware = DUT.select(1)
    _hardware.availability_logistics = 0.9832

    _error_code, _msg = DUT.update(1)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a Hardware ID that doesn't exist. """
    DUT = dtmHardware(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ('RTK ERROR: Attempted to save non-existent Hardware ID '
                    '100.')


@pytest.mark.integration
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmHardware(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_make_composite_reference_designator(test_dao):
    """ make_composite_ref_des() should return False on success. """
    DUT = dtmHardware(test_dao)
    DUT.select_all(1)

    assert not DUT.make_composite_ref_des()
