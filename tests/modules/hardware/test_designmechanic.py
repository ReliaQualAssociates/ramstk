# -*- coding: utf-8 -*-
#
#       tests.modules.hardware.test_designmechanic.py is part of The RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing DesignMechanic module algorithms and models. """

from treelib import Tree

import pytest

from rtk.modules.hardware import dtmDesignMechanic
from rtk.dao import DAO
from rtk.dao import RTKDesignMechanic

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'


@pytest.mark.integration
def test_data_model_create(test_dao):
    """ __init__() should return a DesignMechanic model. """
    DUT = dtmDesignMechanic(test_dao)

    assert isinstance(DUT, dtmDesignMechanic)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)
    assert DUT._tag == 'DesignMechanic'


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a Tree() object populated with RTKDesignMechanic instances on success. """
    DUT = dtmDesignMechanic(test_dao)

    _tree = DUT.do_select_all(hardware_id=2)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(2).data, RTKDesignMechanic)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RTKDesignMechanic data model on success. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.do_select_all(hardware_id=2)

    _design_mechanic = DUT.do_select(2)

    assert isinstance(_design_mechanic, RTKDesignMechanic)
    assert _design_mechanic.hardware_id == 2
    assert _design_mechanic.lubrication_id == 0


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent DesignMechanic ID is requested. """
    DUT = dtmDesignMechanic(test_dao)

    _design_electric = DUT.do_select(100)

    assert _design_electric is None


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return False on success when inserting a DesignMechanic record. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.do_select_all(hardware_id=3)

    _error_code, _msg = DUT.do_insert(hardware_id=90)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Adding one or more items to the RTK Program '
                    'database.')


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.do_select_all(hardware_id=4)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Deleting an item from the RTK Program '
                    'database.')


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a DesignMechanic ID that doesn't exist. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.do_select_all(hardware_id=3)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == ('  RTK ERROR: Attempted to delete non-existent '
                    'DesignMechanic record ID 300.')


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.do_select_all(hardware_id=3)

    _design_electric = DUT.do_select(3)
    _design_electric.resistance = 0.9832

    _error_code, _msg = DUT.do_update(3)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a DesignMechanic ID that doesn't exist. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.do_select_all(hardware_id=3)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2006
    assert _msg == ('RTK ERROR: Attempted to save non-existent DesignMechanic '
                    'record ID 100.')


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmDesignMechanic(test_dao)
    DUT.do_select_all(hardware_id=3)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating all records in the mechanical "
                    "design table.")
