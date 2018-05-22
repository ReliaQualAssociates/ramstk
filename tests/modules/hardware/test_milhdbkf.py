#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.modules.hardware.test_milhdbkf.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing MilHdbkF module algorithms and models. """

from treelib import Tree

import pytest

from rtk.modules.hardware import dtmMilHdbkF
from rtk.dao import DAO, RTKMilHdbkF

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
def test_data_model_create(test_dao):
    """ __init__() should return a MilHdbkF model. """
    DUT = dtmMilHdbkF(test_dao)

    assert isinstance(DUT, dtmMilHdbkF)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)
    assert DUT._tag == 'MilHdbkF'


@pytest.mark.integration
def test_select_all(test_dao):
    """ select_all() should return a Tree() object populated with RTKMilHdbkF instances on success. """
    DUT = dtmMilHdbkF(test_dao)

    _tree = DUT.select_all(2)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(2).data, RTKMilHdbkF)


@pytest.mark.integration
def test_select(test_dao):
    """ select() should return an instance of the RTKMilHdbkF data model on success. """
    DUT = dtmMilHdbkF(test_dao)
    DUT.select_all(2)

    _mil_hdbk_f = DUT.select(2)

    assert isinstance(_mil_hdbk_f, RTKMilHdbkF)
    assert _mil_hdbk_f.hardware_id == 2
    assert _mil_hdbk_f.piA == 0.0


@pytest.mark.integration
def test_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent MilHdbkF ID is requested. """
    DUT = dtmMilHdbkF(test_dao)

    _design_electric = DUT.select(100)

    assert _design_electric is None


@pytest.mark.integration
def test_insert(test_dao):
    """ insert() should return False on success when inserting a MilHdbkF record. """
    DUT = dtmMilHdbkF(test_dao)
    DUT.select_all(3)

    _error_code, _msg = DUT.insert(hardware_id=9)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Adding one or more items to the RTK Program '
                    'database.')


@pytest.mark.integration
def test_delete(test_dao):
    """ delete() should return a zero error code on success. """
    DUT = dtmMilHdbkF(test_dao)
    DUT.select_all(4)

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Deleting an item from the RTK Program '
                    'database.')


@pytest.mark.integration
def test_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a MilHdbkF ID that doesn't exist. """
    DUT = dtmMilHdbkF(test_dao)
    DUT.select_all(3)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ('  RTK ERROR: Attempted to delete non-existent MilHdbkF '
                    'record ID 300.')


@pytest.mark.integration
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmMilHdbkF(test_dao)
    DUT.select_all(3)

    _design_electric = DUT.select(3)
    _design_electric.piV = 0.9832

    _error_code, _msg = DUT.update(3)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a MilHdbkF ID that doesn't exist. """
    DUT = dtmMilHdbkF(test_dao)
    DUT.select_all(3)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ('RTK ERROR: Attempted to save non-existent MilHdbkF '
                    'record ID 100.')


@pytest.mark.integration
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmMilHdbkF(test_dao)
    DUT.select_all(3)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')
